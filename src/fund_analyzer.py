# -*- coding: utf-8 -*-
"""
===================================
基金趋势分析器 - 基于稳健投资理念
===================================

投资理念核心原则：
1. 稳健策略 - 不追高，追求长期稳健收益
2. 趋势为王 - 顺势而为，中长期趋势向上
3. 回调买入 - 优选回调至均线附近时介入
4. 严格止损 - 设定合理止损位，控制风险

分析维度：
1. 净值趋势：基于均线系统判断趋势
2. 收益表现：近期收益率、历史业绩
3. 回调幅度：当前净值与均线的距离
4. 基金经理：稳定性和历史业绩
"""

import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple
from enum import Enum

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class TrendStatus(Enum):
    """趋势状态枚举"""
    STRONG_BULL = "强势上涨"
    BULL = "稳健上涨"
    WEAK_BULL = "弱势上涨"
    CONSOLIDATION = "震荡整理"
    WEAK_BEAR = "弱势下跌"
    BEAR = "持续下跌"
    STRONG_BEAR = "强势下跌"


class BuySignal(Enum):
    """投资建议枚举"""
    STRONG_BUY = "强烈推荐"
    BUY = "适合买入"
    HOLD = "继续持有"
    WAIT = "观望等待"
    SELL = "考虑卖出"
    STRONG_SELL = "强烈卖出"


@dataclass
class FundAnalysisResult:
    """基金分析结果"""
    code: str
    name: str = ""
    
    # 趋势分析
    trend_status: TrendStatus = TrendStatus.CONSOLIDATION
    trend_strength: float = 0.0
    ma5: float = 0.0
    ma10: float = 0.0
    ma20: float = 0.0
    ma60: float = 0.0
    current_nav: float = 0.0
    
    # 回调分析
    pullback_from_ma5: float = 0.0  # 距离5日均线
    pullback_from_ma20: float = 0.0  # 距离20日均线
    pullback_status: str = ""
    
    # 收益分析
    week_1_return: float = 0.0
    month_1_return: float = 0.0
    month_3_return: float = 0.0
    month_6_return: float = 0.0
    year_1_return: float = 0.0
    
    # 投资建议
    buy_signal: BuySignal = BuySignal.WAIT
    signal_score: int = 0
    signal_reasons: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    
    # 操作建议
    entry_timing: str = ""  # 买入时机
    stop_loss: str = ""  # 止损建议
    target_return: str = ""  # 目标收益
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'code': self.code,
            'name': self.name,
            'trend_status': self.trend_status.value,
            'trend_strength': self.trend_strength,
            'ma5': self.ma5,
            'ma10': self.ma10,
            'ma20': self.ma20,
            'ma60': self.ma60,
            'current_nav': self.current_nav,
            'pullback_from_ma5': self.pullback_from_ma5,
            'pullback_from_ma20': self.pullback_from_ma20,
            'pullback_status': self.pullback_status,
            'week_1_return': self.week_1_return,
            'month_1_return': self.month_1_return,
            'month_3_return': self.month_3_return,
            'month_6_return': self.month_6_return,
            'year_1_return': self.year_1_return,
            'buy_signal': self.buy_signal.value,
            'signal_score': self.signal_score,
            'signal_reasons': self.signal_reasons,
            'risk_factors': self.risk_factors,
            'entry_timing': self.entry_timing,
            'stop_loss': self.stop_loss,
            'target_return': self.target_return,
        }


class FundTrendAnalyzer:
    """
    基金趋势分析器
    
    基于稳健投资理念实现：
    1. 趋势判断 - MA5>MA10>MA20 上升趋势
    2. 回调检测 - 不追高，回调时介入
    3. 收益评估 - 历史业绩和近期表现
    4. 风险控制 - 识别风险因素
    """
    
    # 警戒阈值
    CHASE_HIGH_THRESHOLD = 10.0  # 短期涨幅超过10%视为追高
    PULLBACK_BUY_THRESHOLD = -3.0  # 回调3%以内为买入区域
    STRONG_PULLBACK_THRESHOLD = -8.0  # 回调超过8%为大幅回调
    
    def __init__(self):
        """初始化分析器"""
        logger.info("初始化基金趋势分析器")
    
    def analyze(self, df: pd.DataFrame, code: str, name: str = "", 
                performance: Optional[Dict[str, float]] = None) -> FundAnalysisResult:
        """
        分析基金趋势
        
        Args:
            df: 包含净值数据的 DataFrame (必须有 date, nav 列)
            code: 基金代码
            name: 基金名称
            performance: 业绩数据字典
            
        Returns:
            FundAnalysisResult 分析结果
        """
        if df is None or df.empty:
            logger.warning(f"基金 {code} 数据为空")
            return FundAnalysisResult(code=code, name=name)
        
        # 确保数据按日期排序
        df = df.sort_values('date', ascending=True).copy()
        
        # 初始化结果
        result = FundAnalysisResult(code=code, name=name)
        
        # 计算均线
        self._calculate_mas(df)
        
        # 分析趋势
        self._analyze_trend(df, result)
        
        # 分析回调
        self._analyze_pullback(df, result)
        
        # 添加收益数据
        if performance:
            result.week_1_return = performance.get('week_1', 0)
            result.month_1_return = performance.get('month_1', 0)
            result.month_3_return = performance.get('month_3', 0)
            result.month_6_return = performance.get('month_6', 0)
            result.year_1_return = performance.get('year_1', 0)
        
        # 生成投资建议
        self._generate_signal(result)
        
        # 生成操作建议
        self._generate_operation_advice(result)
        
        return result
    
    def _calculate_mas(self, df: pd.DataFrame) -> None:
        """计算均线"""
        df['MA5'] = df['nav'].rolling(window=5, min_periods=1).mean()
        df['MA10'] = df['nav'].rolling(window=10, min_periods=1).mean()
        df['MA20'] = df['nav'].rolling(window=20, min_periods=1).mean()
        df['MA60'] = df['nav'].rolling(window=60, min_periods=1).mean()
    
    def _analyze_trend(self, df: pd.DataFrame, result: FundAnalysisResult) -> None:
        """
        分析趋势状态
        
        核心逻辑：判断均线排列和趋势强度
        """
        latest = df.iloc[-1]
        
        result.current_nav = latest['nav']
        result.ma5 = latest.get('MA5', 0)
        result.ma10 = latest.get('MA10', 0)
        result.ma20 = latest.get('MA20', 0)
        result.ma60 = latest.get('MA60', 0)
        
        # 判断均线排列
        if result.ma5 > result.ma10 > result.ma20:
            # 上升趋势
            if result.current_nav > result.ma5:
                result.trend_status = TrendStatus.STRONG_BULL
                result.trend_strength = 3.0
            else:
                result.trend_status = TrendStatus.BULL
                result.trend_strength = 2.0
        elif result.ma5 > result.ma10:
            # 弱上升趋势
            result.trend_status = TrendStatus.WEAK_BULL
            result.trend_strength = 1.0
        elif result.ma5 < result.ma10 < result.ma20:
            # 下降趋势
            if result.current_nav < result.ma5:
                result.trend_status = TrendStatus.STRONG_BEAR
                result.trend_strength = -3.0
            else:
                result.trend_status = TrendStatus.BEAR
                result.trend_strength = -2.0
        elif result.ma5 < result.ma10:
            # 弱下降趋势
            result.trend_status = TrendStatus.WEAK_BEAR
            result.trend_strength = -1.0
        else:
            # 震荡整理
            result.trend_status = TrendStatus.CONSOLIDATION
            result.trend_strength = 0.0
    
    def _analyze_pullback(self, df: pd.DataFrame, result: FundAnalysisResult) -> None:
        """
        分析回调幅度
        
        回调幅度 = (当前净值 - 均线) / 均线 * 100%
        
        稳健策略：回调时介入，不追高
        """
        if result.ma5 > 0:
            result.pullback_from_ma5 = (result.current_nav - result.ma5) / result.ma5 * 100
        
        if result.ma20 > 0:
            result.pullback_from_ma20 = (result.current_nav - result.ma20) / result.ma20 * 100
        
        # 判断回调状态
        if result.pullback_from_ma5 > self.CHASE_HIGH_THRESHOLD:
            result.pullback_status = "严重偏离均线，追高风险"
        elif result.pullback_from_ma5 > 5.0:
            result.pullback_status = "偏离均线，建议等待回调"
        elif result.pullback_from_ma5 > 0:
            result.pullback_status = "接近均线，可以关注"
        elif result.pullback_from_ma5 > self.PULLBACK_BUY_THRESHOLD:
            result.pullback_status = "回调至均线附近，买入时机"
        else:
            result.pullback_status = "大幅回调，关注支撑"
    
    def _generate_signal(self, result: FundAnalysisResult) -> None:
        """
        生成投资建议
        
        评分机制：
        - 趋势：上升趋势 +2分，震荡 0分，下降趋势 -2分
        - 回调：回调时机 +2分，接近均线 +1分，追高 -2分
        - 收益：年收益>20% +2分，>10% +1分，<0 -2分
        """
        score = 0
        reasons = []
        risks = []
        
        # 1. 趋势分析
        if result.trend_status in [TrendStatus.STRONG_BULL, TrendStatus.BULL]:
            score += 2
            reasons.append(f"✅ 趋势向上（{result.trend_status.value}）")
        elif result.trend_status == TrendStatus.WEAK_BULL:
            score += 1
            reasons.append(f"⚠️ 弱势上涨")
        elif result.trend_status in [TrendStatus.BEAR, TrendStatus.STRONG_BEAR]:
            score -= 2
            risks.append(f"❌ 趋势向下（{result.trend_status.value}）")
        else:
            reasons.append(f"⚠️ 震荡整理")
        
        # 2. 回调分析
        if self.PULLBACK_BUY_THRESHOLD <= result.pullback_from_ma5 <= 0:
            score += 2
            reasons.append(f"✅ 回调至买入区域（距MA5: {result.pullback_from_ma5:.1f}%）")
        elif 0 < result.pullback_from_ma5 <= 3:
            score += 1
            reasons.append(f"✅ 接近均线支撑")
        elif result.pullback_from_ma5 > self.CHASE_HIGH_THRESHOLD:
            score -= 2
            risks.append(f"❌ 严禁追高（距MA5: +{result.pullback_from_ma5:.1f}%）")
        elif result.pullback_from_ma5 > 5:
            score -= 1
            risks.append(f"⚠️ 偏离均线，建议等待")
        
        # 3. 收益分析
        if result.year_1_return > 20:
            score += 2
            reasons.append(f"✅ 年度收益优秀（{result.year_1_return:.1f}%）")
        elif result.year_1_return > 10:
            score += 1
            reasons.append(f"✅ 年度收益良好（{result.year_1_return:.1f}%）")
        elif result.year_1_return < 0:
            score -= 1
            risks.append(f"⚠️ 年度收益为负（{result.year_1_return:.1f}%）")
        
        # 4. 短期收益分析（防止追高）
        if result.month_1_return > 15:
            score -= 1
            risks.append(f"⚠️ 近1月涨幅过大（{result.month_1_return:.1f}%），存在回调风险")
        
        result.signal_score = score
        result.signal_reasons = reasons
        result.risk_factors = risks
        
        # 生成最终建议
        if score >= 4:
            result.buy_signal = BuySignal.STRONG_BUY
        elif score >= 2:
            result.buy_signal = BuySignal.BUY
        elif score >= 0:
            result.buy_signal = BuySignal.HOLD
        elif score >= -2:
            result.buy_signal = BuySignal.WAIT
        elif score >= -4:
            result.buy_signal = BuySignal.SELL
        else:
            result.buy_signal = BuySignal.STRONG_SELL
    
    def _generate_operation_advice(self, result: FundAnalysisResult) -> None:
        """生成操作建议"""
        
        # 买入时机
        if result.buy_signal in [BuySignal.STRONG_BUY, BuySignal.BUY]:
            if result.pullback_from_ma5 < 0:
                result.entry_timing = "当前位置可以买入，回调后加仓"
            else:
                result.entry_timing = f"建议等待回调至MA5（{result.ma5:.3f}）附近买入"
        elif result.buy_signal == BuySignal.HOLD:
            result.entry_timing = "持有观望，等待更好时机"
        else:
            result.entry_timing = "暂不建议买入"
        
        # 止损建议
        if result.ma20 > 0:
            stop_loss_nav = result.ma20 * 0.92  # MA20下方8%
            result.stop_loss = f"跌破{stop_loss_nav:.3f}（MA20下方8%）考虑止损"
        
        # 目标收益
        if result.buy_signal in [BuySignal.STRONG_BUY, BuySignal.BUY]:
            if result.year_1_return > 15:
                result.target_return = "目标收益 +15% ~ +25%"
            else:
                result.target_return = "目标收益 +10% ~ +15%"
        else:
            result.target_return = "暂不设定目标"
    
    def format_analysis(self, result: FundAnalysisResult) -> str:
        """
        格式化分析结果为文本
        
        Args:
            result: 分析结果
            
        Returns:
            格式化的分析文本
        """
        signal_emoji = {
            BuySignal.STRONG_BUY: "🟢",
            BuySignal.BUY: "🟢",
            BuySignal.HOLD: "🟡",
            BuySignal.WAIT: "🟡",
            BuySignal.SELL: "🔴",
            BuySignal.STRONG_SELL: "🔴",
        }
        
        emoji = signal_emoji.get(result.buy_signal, "⚪")
        
        lines = [
            f"{emoji} {result.buy_signal.value} | {result.name}({result.code})",
            f"",
            f"📊 净值趋势",
            f"  当前净值: {result.current_nav:.3f}",
            f"  趋势状态: {result.trend_status.value}",
            f"  MA5: {result.ma5:.3f} | MA20: {result.ma20:.3f} | MA60: {result.ma60:.3f}",
            f"  距离MA5: {result.pullback_from_ma5:+.1f}% | {result.pullback_status}",
            f"",
            f"📈 收益表现",
            f"  近1周: {result.week_1_return:+.1f}% | 近1月: {result.month_1_return:+.1f}%",
            f"  近3月: {result.month_3_return:+.1f}% | 近6月: {result.month_6_return:+.1f}%",
            f"  近1年: {result.year_1_return:+.1f}%",
            f"",
            f"💡 投资建议（评分: {result.signal_score}）",
        ]
        
        for reason in result.signal_reasons:
            lines.append(f"  {reason}")
        
        if result.risk_factors:
            lines.append(f"")
            lines.append(f"⚠️ 风险提示")
            for risk in result.risk_factors:
                lines.append(f"  {risk}")
        
        lines.extend([
            f"",
            f"🎯 操作建议",
            f"  买入时机: {result.entry_timing}",
            f"  止损建议: {result.stop_loss}",
            f"  目标收益: {result.target_return}",
        ])
        
        return "\n".join(lines)


if __name__ == "__main__":
    # 测试代码
    logging.basicConfig(level=logging.INFO)
    
    # 模拟净值数据
    dates = pd.date_range(end='2024-01-20', periods=120)
    navs = [1.0 + i * 0.005 + np.random.randn() * 0.01 for i in range(120)]
    
    df = pd.DataFrame({
        'date': dates,
        'nav': navs,
    })
    
    # 模拟业绩数据
    performance = {
        'week_1': 2.5,
        'month_1': 5.8,
        'month_3': 12.3,
        'month_6': 18.6,
        'year_1': 28.5,
    }
    
    analyzer = FundTrendAnalyzer()
    result = analyzer.analyze(df, '005827', '易方达蓝筹精选', performance)
    
    print(analyzer.format_analysis(result))
