#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基金分析模块测试脚本
"""

import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

def test_fund_fetcher():
    """测试基金数据获取"""
    print("\n" + "="*60)
    print("测试基金数据获取模块")
    print("="*60 + "\n")
    
    try:
        from data_provider.fund_fetcher import FundDataFetcher
        
        fetcher = FundDataFetcher()
        
        # 测试基金代码
        test_code = "000001"  # 华夏成长
        
        print(f"🔍 正在获取基金 {test_code} 的数据...\n")
        
        # 1. 基金基本信息
        print("1️⃣ 基金基本信息")
        info = fetcher.get_fund_info(test_code)
        if info:
            print(f"   代码: {info.get('code', 'N/A')}")
            print(f"   名称: {info.get('name', 'N/A')}")
            print(f"   类型: {info.get('type', 'N/A')}")
            print(f"   公司: {info.get('company', 'N/A')}")
        else:
            print("   ⚠️ 未获取到基金信息")
        
        # 2. 净值数据
        print("\n2️⃣ 基金净值数据（最近5天）")
        nav_df = fetcher.get_fund_nav(test_code, days=30)
        if nav_df is not None and not nav_df.empty:
            print(nav_df.tail().to_string())
        else:
            print("   ⚠️ 未获取到净值数据")
        
        # 3. 业绩数据
        print("\n3️⃣ 基金业绩数据")
        performance = fetcher.get_fund_performance(test_code)
        if performance:
            for key, value in performance.items():
                print(f"   {key}: {value:+.2f}%")
        else:
            print("   ⚠️ 未获取到业绩数据")
        
        print("\n✅ 基金数据获取测试完成！\n")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_fund_analyzer():
    """测试基金分析器"""
    print("\n" + "="*60)
    print("测试基金分析模块")
    print("="*60 + "\n")
    
    try:
        from src.fund_analyzer import FundTrendAnalyzer
        from data_provider.fund_fetcher import FundDataFetcher
        
        # 获取数据
        fetcher = FundDataFetcher()
        test_code = "000001"
        
        print(f"🔍 正在分析基金 {test_code}...\n")
        
        # 获取净值数据
        nav_df = fetcher.get_fund_nav(test_code, days=120)
        if nav_df is None or nav_df.empty:
            print("❌ 无法获取净值数据，跳过分析测试")
            return False
        
        # 获取业绩数据
        performance = fetcher.get_fund_performance(test_code)
        
        # 获取基金信息
        info = fetcher.get_fund_info(test_code)
        name = info.get('name', test_code) if info else test_code
        
        # 执行分析
        analyzer = FundTrendAnalyzer()
        result = analyzer.analyze(nav_df, test_code, name, performance)
        
        # 输出分析结果
        print(analyzer.format_analysis(result))
        
        print("\n✅ 基金分析测试完成！\n")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n" + "🎯 " + "基金分析系统测试".center(56) + " 🎯")
    
    # 测试1: 数据获取
    test1_passed = test_fund_fetcher()
    
    # 测试2: 基金分析
    test2_passed = test_fund_analyzer()
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"数据获取测试: {'✅ 通过' if test1_passed else '❌ 失败'}")
    print(f"基金分析测试: {'✅ 通过' if test2_passed else '❌ 失败'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 所有测试通过！基金分析系统运行正常。")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
