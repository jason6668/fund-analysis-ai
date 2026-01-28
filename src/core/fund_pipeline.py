# -*- coding: utf-8 -*-
"""
===================================
基金分析核心流水线
===================================

职责：
1. 管理整个基金分析流程
2. 协调数据获取、分析、通知等模块
"""

import logging
import concurrent.futures
from typing import List, Optional, Dict, Any

from src.config import Config
from src.notification import NotificationService
from data_provider.fund_fetcher import FundDataFetcher
from src.fund_analyzer import FundTrendAnalyzer, FundAnalysisResult, BuySignal

logger = logging.getLogger(__name__)

class FundAnalysisPipeline:
    """基金分析主流程调度器"""
    
    def __init__(
        self,
        config: Optional[Config] = None,
        max_workers: Optional[int] = None
    ):
        self.config = config or Config.get_instance()
        self.max_workers = max_workers or self.config.max_workers
        self.fetcher = FundDataFetcher()
        self.analyzer = FundTrendAnalyzer()
        self.notifier = NotificationService(self.config)
        
    def process_single_fund(self, code: str) -> Optional[FundAnalysisResult]:
        """处理单只基金"""
        try:
            logger.info(f"开始分析基金: {code}")
            
            # 1. 获取基本信息（验证代码有效性）
            info = self.fetcher.get_fund_info(code)
            if not info:
                logger.error(f"基金 {code} 不存在或无法获取信息")
                return None
                
            name = info.get('name', code)
            logger.info(f"获取到基金信息: {name}({code})")
            
            # 2. 获取净值数据
            nav_df = self.fetcher.get_fund_nav(code, days=120)
            if nav_df is None or nav_df.empty:
                logger.warning(f"基金 {name}({code}) 净值数据为空")
                return None
                
            # 3. 获取业绩数据
            performance = self.fetcher.get_fund_performance(code)
            
            # 4. 执行分析
            result = self.analyzer.analyze(
                df=nav_df,
                code=code,
                name=name,
                performance=performance
            )
            
            # 5. 单只推送（如果启用）
            if self.config.single_stock_notify:
                self._send_single_notification(result)
                
            return result
            
        except Exception as e:
            logger.exception(f"分析基金 {code} 时发生错误: {e}")
            return None

    def run(
        self, 
        fund_codes: Optional[List[str]] = None,
        dry_run: bool = False,
        send_notification: bool = True
    ) -> List[FundAnalysisResult]:
        """运行分析流程"""
        
        # 1. 确定基金列表
        if not fund_codes:
            fund_codes = self.config.stock_list  # 这里复用配置中的列表，虽然变量名叫stock_list
            
        if not fund_codes:
            logger.warning("没有需要分析的基金")
            return []
            
        logger.info(f"开始分析任务，共 {len(fund_codes)} 只基金")
        
        results = []
        
        # 2. 并发执行分析
        if dry_run:
            logger.info("Dry run 模式，跳过实际分析")
            return []
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_code = {
                executor.submit(self.process_single_fund, code): code 
                for code in fund_codes
            }
            
            for future in concurrent.futures.as_completed(future_to_code):
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    logger.error(f"任务执行异常: {e}")
                    
        # 3. 汇总推送
        if send_notification and results and not self.config.single_stock_notify:
            self._send_summary_notification(results)
            
        return results

    def _send_single_notification(self, result: FundAnalysisResult):
        """发送单只基金通知"""
        content = self.analyzer.format_analysis(result)
        title = f"基金分析: {result.name}"
        self.notifier.send(content, title)

    def _send_summary_notification(self, results: List[FundAnalysisResult]):
        """发送汇总通知"""
        if not results:
            return
            
        # 统计信息
        total = len(results)
        buy = sum(1 for r in results if r.buy_signal in [BuySignal.BUY, BuySignal.STRONG_BUY])
        wait = sum(1 for r in results if r.buy_signal in [BuySignal.WAIT, BuySignal.HOLD])
        sell = sum(1 for r in results if r.buy_signal in [BuySignal.SELL, BuySignal.STRONG_SELL])
        
        # 构建消息头
        msg = [
            f"📊 {self.config.today_date_str if hasattr(self.config, 'today_date_str') else ''} 决策仪表盘",
            f"{total}只基金 | 🟢买入:{buy} 🟡观望:{wait} 🔴卖出:{sell}",
            ""
        ]
        
        # 按评分排序，优先展示推荐的
        sorted_results = sorted(results, key=lambda x: x.signal_score, reverse=True)
        
        for res in sorted_results:
            # 格式化每只基金的简报
            msg.append(self.analyzer.format_analysis(res))
            msg.append("---") # 分隔符
            
        full_content = "\n".join(msg)
        
        # 发送
        self.notifier.send(full_content, title="基金投资决策日报")
