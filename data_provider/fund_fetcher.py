# -*- coding: utf-8 -*-
"""
===================================
基金数据获取器 - 使用 AkShare
===================================

功能：
1. 获取基金净值数据
2. 获取基金持仓信息
3. 获取基金经理信息
4. 获取基金基本信息
"""

import logging
from typing import Optional, Dict, Any, List
import pandas as pd
from datetime import datetime, timedelta

try:
    import akshare as ak
except ImportError:
    ak = None

logger = logging.getLogger(__name__)


class FundDataFetcher:
    """基金数据获取器"""
    
    def __init__(self):
        """初始化基金数据获取器"""
        if ak is None:
            logger.warning("AkShare 未安装，请运行: pip install akshare")
            
    def get_fund_info(self, fund_code: str) -> Optional[Dict[str, Any]]:
        """
        获取基金基本信息
        
        Args:
            fund_code: 基金代码（6位数字）
            
        Returns:
            基金基本信息字典
        """
        try:
            if ak is None:
                logger.error("AkShare 未安装")
                return None
                
            # 获取基金基本信息
            df = ak.fund_em_fund_name()
            fund_info = df[df['基金代码'] == fund_code]
            
            if fund_info.empty:
                logger.warning(f"未找到基金 {fund_code} 的信息")
                return None
                
            info = fund_info.iloc[0].to_dict()
            
            return {
                'code': fund_code,
                'name': info.get('基金简称', ''),
                'type': info.get('基金类型', ''),
                'company': info.get('基金公司', ''),
                'manager': info.get('基金经理', ''),
            }
            
        except Exception as e:
            logger.error(f"获取基金 {fund_code} 信息失败: {e}")
            return None
    
    def get_fund_nav(self, fund_code: str, days: int = 120) -> Optional[pd.DataFrame]:
        """
        获取基金净值数据
        
        Args:
            fund_code: 基金代码
            days: 获取多少天的数据
            
        Returns:
            包含净值数据的 DataFrame
        """
        try:
            if ak is None:
                logger.error("AkShare 未安装")
                return None
                
            # 获取基金净值数据
            df = ak.fund_em_open_fund_info(fund=fund_code, indicator="单位净值走势")
            
            if df is None or df.empty:
                logger.warning(f"未找到基金 {fund_code} 的净值数据")
                return None
            
            # 重命名列
            df = df.rename(columns={
                '净值日期': 'date',
                '单位净值': 'nav',
                '日增长率': 'change_pct'
            })
            
            # 转换数据类型
            df['date'] = pd.to_datetime(df['date'])
            df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
            df['change_pct'] = pd.to_numeric(df['change_pct'], errors='coerce')
            
            # 按日期排序
            df = df.sort_values('date', ascending=True)
            
            # 只保留最近的数据
            if len(df) > days:
                df = df.tail(days)
            
            # 添加技术指标需要的列
            df['close'] = df['nav']  # 用净值作为收盘价
            df['volume'] = 0  # 基金没有成交量，填充0
            
            return df.reset_index(drop=True)
            
        except Exception as e:
            logger.error(f"获取基金 {fund_code} 净值数据失败: {e}")
            return None
    
    def get_fund_performance(self, fund_code: str) -> Optional[Dict[str, Any]]:
        """
        获取基金业绩数据
        
        Args:
            fund_code: 基金代码
            
        Returns:
            业绩数据字典
        """
        try:
            if ak is None:
                logger.error("AkShare 未安装")
                return None
            
            # 获取基金阶段涨幅
            df = ak.fund_em_open_fund_info(fund=fund_code, indicator="阶段涨幅")
            
            if df is None or df.empty:
                logger.warning(f"未找到基金 {fund_code} 的业绩数据")
                return None
            
            performance = {}
            for _, row in df.iterrows():
                period = row.get('指标', '')
                value = row.get('涨幅', 0)
                
                # 转换为数值
                try:
                    value = float(str(value).replace('%', ''))
                except:
                    value = 0
                    
                if '近1周' in period:
                    performance['week_1'] = value
                elif '近1月' in period:
                    performance['month_1'] = value
                elif '近3月' in period:
                    performance['month_3'] = value
                elif '近6月' in period:
                    performance['month_6'] = value
                elif '近1年' in period:
                    performance['year_1'] = value
                elif '近3年' in period:
                    performance['year_3'] = value
                    
            return performance
            
        except Exception as e:
            logger.error(f"获取基金 {fund_code} 业绩数据失败: {e}")
            return None
    
    def get_fund_holdings(self, fund_code: str) -> Optional[List[Dict[str, Any]]]:
        """
        获取基金持仓信息
        
        Args:
            fund_code: 基金代码
            
        Returns:
            持仓列表
        """
        try:
            if ak is None:
                logger.error("AkShare 未安装")
                return None
            
            # 获取基金持仓
            df = ak.fund_em_open_fund_info(fund=fund_code, indicator="基金持仓")
            
            if df is None or df.empty:
                logger.warning(f"未找到基金 {fund_code} 的持仓数据")
                return None
            
            holdings = []
            for _, row in df.iterrows():
                holdings.append({
                    'stock_code': row.get('股票代码', ''),
                    'stock_name': row.get('股票名称', ''),
                    'ratio': row.get('持仓占比', 0),
                })
                
            return holdings[:10]  # 返回前10大持仓
            
        except Exception as e:
            logger.error(f"获取基金 {fund_code} 持仓数据失败: {e}")
            return None
    
    def get_realtime_data(self, fund_code: str) -> Optional[Dict[str, Any]]:
        """
        获取基金实时数据
        
        Args:
            fund_code: 基金代码
            
        Returns:
            实时数据字典
        """
        try:
            if ak is None:
                logger.error("AkShare 未安装")
                return None
            
            # 获取基金实时数据
            df = ak.fund_em_open_fund_info(fund=fund_code, indicator="实时估值")
            
            if df is None or df.empty:
                # 如果没有实时数据，返回基本信息
                info = self.get_fund_info(fund_code)
                if info:
                    return {
                        'code': fund_code,
                        'name': info.get('name', ''),
                        'current': 0,
                        'change': 0,
                        'change_pct': 0,
                    }
                return None
            
            latest = df.iloc[-1]
            
            return {
                'code': fund_code,
                'name': latest.get('基金名称', ''),
                'current': float(latest.get('估算净值', 0)),
                'change': 0,
                'change_pct': float(latest.get('估算增长率', 0)),
            }
            
        except Exception as e:
            logger.error(f"获取基金 {fund_code} 实时数据失败: {e}")
            return None


# 为了兼容性，创建一个包装类
class FundFetcher(FundDataFetcher):
    """基金数据获取器（兼容性别名）"""
    pass


if __name__ == "__main__":
    # 测试代码
    logging.basicConfig(level=logging.INFO)
    
    fetcher = FundDataFetcher()
    
    # 测试易方达蓝筹精选
    test_code = "005827"
    
    print(f"\n=== 测试基金代码: {test_code} ===\n")
    
    # 1. 基本信息
    info = fetcher.get_fund_info(test_code)
    print(f"基金信息: {info}")
    
    # 2. 净值数据
    nav_df = fetcher.get_fund_nav(test_code, days=30)
    if nav_df is not None:
        print(f"\n净值数据 (最近5天):\n{nav_df.tail()}")
    
    # 3. 业绩数据
    performance = fetcher.get_fund_performance(test_code)
    print(f"\n业绩数据: {performance}")
    
    # 4. 持仓信息
    holdings = fetcher.get_fund_holdings(test_code)
    if holdings:
        print(f"\n前3大持仓: {holdings[:3]}")
    
    # 5. 实时数据
    realtime = fetcher.get_realtime_data(test_code)
    print(f"\n实时数据: {realtime}")
