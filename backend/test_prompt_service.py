#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
提示词模块和DeepSeek分析服务测试脚本
"""

import sys
import os
import json
from datetime import date

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_prompt_service():
    """测试提示词服务"""
    print("=== 测试提示词服务 ===")
    
    from app.services.prompt_service import prompt_service
    
    # 测试个股基本信息提示词
    print("\n1. 测试个股基本信息提示词:")
    basic_prompt = prompt_service.get_stock_analysis_prompt(
        'basic_info',
        stock_name='贵州茅台',
        stock_code='600519.SH',
        latest_data={'close': 1800.0, 'pe': 45.2, 'pb': 12.5}
    )
    print(f"提示词长度: {len(basic_prompt)} 字符")
    print(f"提示词预览: {basic_prompt[:200]}...")
    
    # 测试个股每日走势提示词
    print("\n2. 测试个股每日走势提示词:")
    daily_prompt = prompt_service.get_stock_analysis_prompt(
        'daily_analysis',
        stock_name='贵州茅台',
        stock_code='600519.SH',
        daily_data={'open': 1790, 'close': 1800, 'high': 1810, 'low': 1785, 'vol': 1000000},
        analysis_date=date(2024, 1, 15)
    )
    print(f"提示词长度: {len(daily_prompt)} 字符")
    print(f"提示词预览: {daily_prompt[:200]}...")
    
    # 测试个股趋势分析提示词
    print("\n3. 测试个股趋势分析提示词:")
    trend_prompt = prompt_service.get_stock_analysis_prompt(
        'trend_analysis',
        stock_name='贵州茅台',
        stock_code='600519.SH',
        period='近期'
    )
    print(f"提示词长度: {len(trend_prompt)} 字符")
    print(f"提示词预览: {trend_prompt[:200]}...")
    
    # 测试大盘分析提示词
    print("\n4. 测试大盘分析提示词:")
    market_prompt = prompt_service.get_market_analysis_prompt(
        'market_overview',
        analysis_date=date(2024, 1, 15)
    )
    print(f"提示词长度: {len(market_prompt)} 字符")
    print(f"提示词预览: {market_prompt[:200]}...")
    
    # 测试行业分析提示词
    print("\n5. 测试行业分析提示词:")
    industry_prompt = prompt_service.get_market_analysis_prompt(
        'industry_analysis',
        industry_name='科技',
        analysis_date=date(2024, 1, 15)
    )
    print(f"提示词长度: {len(industry_prompt)} 字符")
    print(f"提示词预览: {industry_prompt[:200]}...")

def test_deepseek_analysis_service():
    """测试DeepSeek分析服务"""
    print("\n=== 测试DeepSeek分析服务 ===")
    
    from app.services.deepseek_analysis_service import deepseek_analysis_service
    
    # 测试获取分析类型
    print("\n1. 测试获取分析类型:")
    analysis_types = deepseek_analysis_service.get_analysis_types()
    print(f"支持的分析类型: {json.dumps(analysis_types, ensure_ascii=False, indent=2)}")
    
    # 测试个股基本信息分析（模拟）
    print("\n2. 测试个股基本信息分析:")
    try:
        # 这里需要数据库中有相应的股票数据
        result = deepseek_analysis_service.analyze_stock_basic_info('000001.SZ', 'test_session_001')
        print(f"分析结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"分析失败（可能缺少数据）: {str(e)}")
    
    # 测试大盘概况分析（模拟）
    print("\n3. 测试大盘概况分析:")
    try:
        result = deepseek_analysis_service.analyze_market_overview(date.today(), 'test_session_002')
        print(f"分析结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"分析失败（可能缺少数据）: {str(e)}")

def test_api_endpoints():
    """测试API接口"""
    print("\n=== 测试API接口 ===")
    
    # 这里可以添加API接口测试
    print("API接口测试需要启动Flask应用")
    print("可用的API接口:")
    print("1. GET /api/deepseek_analysis/stock/basic_info/<ts_code>")
    print("2. GET /api/deepseek_analysis/stock/daily/<ts_code>")
    print("3. GET /api/deepseek_analysis/stock/trend/<ts_code>")
    print("4. GET /api/deepseek_analysis/market/overview")
    print("5. GET /api/deepseek_analysis/industry/<industry_name>")
    print("6. GET /api/deepseek_analysis/analysis_types")
    print("7. GET /api/deepseek_analysis/stock/<ts_code>/comprehensive")
    print("8. GET /api/deepseek_analysis/market/comprehensive")

def main():
    """主函数"""
    print("提示词模块和DeepSeek分析服务测试")
    print("=" * 50)
    
    try:
        # 测试提示词服务
        test_prompt_service()
        
        # 测试DeepSeek分析服务
        test_deepseek_analysis_service()
        
        # 测试API接口
        test_api_endpoints()
        
        print("\n" + "=" * 50)
        print("测试完成！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 