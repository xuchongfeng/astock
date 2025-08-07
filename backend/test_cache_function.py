#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
缓存功能测试脚本
"""

import sys
import os
import json
from datetime import date

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_db_record_function():
    """测试从数据库读取记录功能"""
    print("=== 测试从数据库读取记录功能 ===")
    
    from app.services.deepseek_analysis_service import deepseek_analysis_service
    
    # 测试股票代码
    test_stock_code = '000001.SZ'
    
    print(f"\n测试股票: {test_stock_code}")
    
    # 第一次分析（应该调用DeepSeek API）
    print("\n1. 第一次分析个股基本信息:")
    result1 = deepseek_analysis_service.analyze_stock_basic_info(test_stock_code)
    print(f"分析结果: {'成功' if result1.get('success') else '失败'}")
    print(f"是否缓存: {result1.get('cached', False)}")
    print(f"来自数据库: {result1.get('from_db', False)}")
    if result1.get('success'):
        print(f"分析内容长度: {len(result1.get('analysis', ''))}")
    else:
        print(f"错误信息: {result1.get('error')}")
    
    # 第二次分析（应该返回数据库记录）
    print("\n2. 第二次分析个股基本信息（应该返回数据库记录）:")
    result2 = deepseek_analysis_service.analyze_stock_basic_info(test_stock_code)
    print(f"分析结果: {'成功' if result2.get('success') else '失败'}")
    print(f"是否缓存: {result2.get('cached', False)}")
    print(f"来自数据库: {result2.get('from_db', False)}")
    if result2.get('success'):
        print(f"分析内容长度: {len(result2.get('analysis', ''))}")
        if result2.get('from_db'):
            print(f"记录创建时间: {result2.get('created_at')}")
            print(f"记录更新时间: {result2.get('updated_at')}")
    else:
        print(f"错误信息: {result2.get('error')}")
    
    # 测试每日走势分析
    print("\n3. 第一次分析个股每日走势:")
    result3 = deepseek_analysis_service.analyze_stock_daily(test_stock_code, date.today())
    print(f"分析结果: {'成功' if result3.get('success') else '失败'}")
    print(f"是否缓存: {result3.get('cached', False)}")
    print(f"来自数据库: {result3.get('from_db', False)}")
    if result3.get('success'):
        print(f"分析内容长度: {len(result3.get('analysis', ''))}")
    else:
        print(f"错误信息: {result3.get('error')}")
    
    # 第二次每日走势分析（应该返回数据库记录）
    print("\n4. 第二次分析个股每日走势（应该返回数据库记录）:")
    result4 = deepseek_analysis_service.analyze_stock_daily(test_stock_code, date.today())
    print(f"分析结果: {'成功' if result4.get('success') else '失败'}")
    print(f"是否缓存: {result4.get('cached', False)}")
    print(f"来自数据库: {result4.get('from_db', False)}")
    if result4.get('success'):
        print(f"分析内容长度: {len(result4.get('analysis', ''))}")
        if result4.get('from_db'):
            print(f"记录创建时间: {result4.get('created_at')}")
            print(f"记录更新时间: {result4.get('updated_at')}")
    else:
        print(f"错误信息: {result4.get('error')}")
    
    # 测试趋势分析
    print("\n5. 第一次分析个股趋势:")
    result5 = deepseek_analysis_service.analyze_stock_trend(test_stock_code, '近期')
    print(f"分析结果: {'成功' if result5.get('success') else '失败'}")
    print(f"是否缓存: {result5.get('cached', False)}")
    print(f"来自数据库: {result5.get('from_db', False)}")
    if result5.get('success'):
        print(f"分析内容长度: {len(result5.get('analysis', ''))}")
    else:
        print(f"错误信息: {result5.get('error')}")
    
    # 第二次趋势分析（应该返回数据库记录）
    print("\n6. 第二次分析个股趋势（应该返回数据库记录）:")
    result6 = deepseek_analysis_service.analyze_stock_trend(test_stock_code, '近期')
    print(f"分析结果: {'成功' if result6.get('success') else '失败'}")
    print(f"是否缓存: {result6.get('cached', False)}")
    print(f"来自数据库: {result6.get('from_db', False)}")
    if result6.get('success'):
        print(f"分析内容长度: {len(result6.get('analysis', ''))}")
        if result6.get('from_db'):
            print(f"记录创建时间: {result6.get('created_at')}")
            print(f"记录更新时间: {result6.get('updated_at')}")
    else:
        print(f"错误信息: {result6.get('error')}")

def test_different_dates_db():
    """测试不同日期的数据库记录"""
    print("\n=== 测试不同日期的数据库记录 ===")
    
    from app.services.deepseek_analysis_service import deepseek_analysis_service
    
    test_stock_code = '000001.SZ'
    test_date = date(2024, 1, 15)
    
    print(f"\n测试股票: {test_stock_code}, 日期: {test_date}")
    
    # 第一次分析指定日期
    print("\n1. 第一次分析指定日期的每日走势:")
    result1 = deepseek_analysis_service.analyze_stock_daily(test_stock_code, test_date)
    print(f"分析结果: {'成功' if result1.get('success') else '失败'}")
    print(f"是否缓存: {result1.get('cached', False)}")
    print(f"来自数据库: {result1.get('from_db', False)}")
    
    # 第二次分析指定日期（应该返回数据库记录）
    print("\n2. 第二次分析指定日期的每日走势（应该返回数据库记录）:")
    result2 = deepseek_analysis_service.analyze_stock_daily(test_stock_code, test_date)
    print(f"分析结果: {'成功' if result2.get('success') else '失败'}")
    print(f"是否缓存: {result2.get('cached', False)}")
    print(f"来自数据库: {result2.get('from_db', False)}")
    
    # 分析今天的数据（应该重新请求）
    print("\n3. 分析今天的每日走势（应该重新请求）:")
    result3 = deepseek_analysis_service.analyze_stock_daily(test_stock_code, date.today())
    print(f"分析结果: {'成功' if result3.get('success') else '失败'}")
    print(f"是否缓存: {result3.get('cached', False)}")
    print(f"来自数据库: {result3.get('from_db', False)}")

def test_db_query_function():
    """测试数据库查询功能"""
    print("\n=== 测试数据库查询功能 ===")
    
    from app.services.deepseek_analysis_service import deepseek_analysis_service
    
    test_stock_code = '000001.SZ'
    
    # 测试查询基本信息记录
    print(f"\n查询股票 {test_stock_code} 的基本信息记录:")
    existing_record = deepseek_analysis_service._get_existing_deepseek_record(test_stock_code, 'basic_info')
    if existing_record:
        print(f"找到记录，创建时间: {existing_record.created_at}")
        print(f"更新时间: {existing_record.updated_at}")
        print(f"内容长度: {len(existing_record.content)}")
        print(f"Session ID: {existing_record.session_id}")
    else:
        print("未找到记录")
    
    # 测试查询每日走势记录
    print(f"\n查询股票 {test_stock_code} 的每日走势记录:")
    existing_record = deepseek_analysis_service._get_existing_deepseek_record(test_stock_code, 'daily_analysis')
    if existing_record:
        print(f"找到记录，创建时间: {existing_record.created_at}")
        print(f"更新时间: {existing_record.updated_at}")
        print(f"内容长度: {len(existing_record.content)}")
        print(f"Session ID: {existing_record.session_id}")
    else:
        print("未找到记录")
    
    # 测试查询趋势分析记录
    print(f"\n查询股票 {test_stock_code} 的趋势分析记录:")
    existing_record = deepseek_analysis_service._get_existing_deepseek_record(test_stock_code, 'trend_analysis')
    if existing_record:
        print(f"找到记录，创建时间: {existing_record.created_at}")
        print(f"更新时间: {existing_record.updated_at}")
        print(f"内容长度: {len(existing_record.content)}")
        print(f"Session ID: {existing_record.session_id}")
    else:
        print("未找到记录")

def test_cache_function():
    """测试缓存功能（保留原有功能）"""
    print("\n=== 测试缓存功能 ===")
    
    from app.services.deepseek_analysis_service import deepseek_analysis_service
    
    # 测试股票代码
    test_stock_code = '000001.SZ'
    
    print(f"\n测试股票: {test_stock_code}")
    
    # 第一次分析（应该调用DeepSeek API）
    print("\n1. 第一次分析个股基本信息:")
    result1 = deepseek_analysis_service.analyze_stock_basic_info(test_stock_code)
    print(f"分析结果: {'成功' if result1.get('success') else '失败'}")
    print(f"是否缓存: {result1.get('cached', False)}")
    print(f"来自数据库: {result1.get('from_db', False)}")
    if result1.get('success'):
        print(f"分析内容长度: {len(result1.get('analysis', ''))}")
    else:
        print(f"错误信息: {result1.get('error')}")
    
    # 第二次分析（应该返回数据库记录）
    print("\n2. 第二次分析个股基本信息（应该返回数据库记录）:")
    result2 = deepseek_analysis_service.analyze_stock_basic_info(test_stock_code)
    print(f"分析结果: {'成功' if result2.get('success') else '失败'}")
    print(f"是否缓存: {result2.get('cached', False)}")
    print(f"来自数据库: {result2.get('from_db', False)}")
    if result2.get('success'):
        print(f"分析内容长度: {len(result2.get('analysis', ''))}")
        if result2.get('from_db'):
            print(f"记录创建时间: {result2.get('created_at')}")
            print(f"记录更新时间: {result2.get('updated_at')}")
    else:
        print(f"错误信息: {result2.get('error')}")

def test_different_dates():
    """测试不同日期的缓存"""
    print("\n=== 测试不同日期的缓存 ===")
    
    from app.services.deepseek_analysis_service import deepseek_analysis_service
    
    test_stock_code = '000001.SZ'
    test_date = date(2024, 1, 15)
    
    print(f"\n测试股票: {test_stock_code}, 日期: {test_date}")
    
    # 第一次分析指定日期
    print("\n1. 第一次分析指定日期的每日走势:")
    result1 = deepseek_analysis_service.analyze_stock_daily(test_stock_code, test_date)
    print(f"分析结果: {'成功' if result1.get('success') else '失败'}")
    print(f"是否缓存: {result1.get('cached', False)}")
    print(f"来自数据库: {result1.get('from_db', False)}")
    
    # 第二次分析指定日期（应该返回数据库记录）
    print("\n2. 第二次分析指定日期的每日走势（应该返回数据库记录）:")
    result2 = deepseek_analysis_service.analyze_stock_daily(test_stock_code, test_date)
    print(f"分析结果: {'成功' if result2.get('success') else '失败'}")
    print(f"是否缓存: {result2.get('cached', False)}")
    print(f"来自数据库: {result2.get('from_db', False)}")
    
    # 分析今天的数据（应该重新请求）
    print("\n3. 分析今天的每日走势（应该重新请求）:")
    result3 = deepseek_analysis_service.analyze_stock_daily(test_stock_code, date.today())
    print(f"分析结果: {'成功' if result3.get('success') else '失败'}")
    print(f"是否缓存: {result3.get('cached', False)}")
    print(f"来自数据库: {result3.get('from_db', False)}")

def test_cache_query():
    """测试缓存查询功能"""
    print("\n=== 测试缓存查询功能 ===")
    
    from app.services.deepseek_service import get_deepseek_by_ts_code_and_analysis_type
    
    test_stock_code = '000001.SZ'
    
    # 测试查询基本信息缓存
    print(f"\n查询股票 {test_stock_code} 的基本信息缓存:")
    cached_record = get_deepseek_by_ts_code_and_analysis_type(test_stock_code, 'basic_info')
    if cached_record:
        print(f"找到缓存记录，创建时间: {cached_record.created_at}")
        print(f"内容长度: {len(cached_record.content)}")
    else:
        print("未找到缓存记录")
    
    # 测试查询每日走势缓存
    print(f"\n查询股票 {test_stock_code} 的每日走势缓存:")
    cached_record = get_deepseek_by_ts_code_and_analysis_type(test_stock_code, 'daily_analysis')
    if cached_record:
        print(f"找到缓存记录，创建时间: {cached_record.created_at}")
        print(f"内容长度: {len(cached_record.content)}")
    else:
        print("未找到缓存记录")
    
    # 测试查询趋势分析缓存
    print(f"\n查询股票 {test_stock_code} 的趋势分析缓存:")
    cached_record = get_deepseek_by_ts_code_and_analysis_type(test_stock_code, 'trend_analysis')
    if cached_record:
        print(f"找到缓存记录，创建时间: {cached_record.created_at}")
        print(f"内容长度: {len(cached_record.content)}")
    else:
        print("未找到缓存记录")

def main():
    """主函数"""
    print("数据库记录读取功能测试")
    print("=" * 50)
    
    try:
        # 测试从数据库读取记录功能
        test_db_record_function()
        
        # 测试不同日期的数据库记录
        test_different_dates_db()
        
        # 测试数据库查询功能
        test_db_query_function()
        
        # 保留原有测试功能
        test_cache_function()
        test_different_dates()
        test_cache_query()
        
        print("\n" + "=" * 50)
        print("测试完成！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 