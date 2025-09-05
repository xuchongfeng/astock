#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试同花顺概念板块日线数据API的trade_date参数格式转换
"""

import requests
import json
from datetime import datetime

def test_trade_date_format():
    """测试trade_date参数格式转换"""
    
    base_url = 'http://localhost:5000'
    
    print("=== 测试同花顺概念板块日线数据API的trade_date参数格式转换 ===")
    
    # 1. 测试不带日期参数的查询
    print("\n1. 测试不带日期参数的查询:")
    try:
        response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 5
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   返回记录数: {len(data['data'])}")
            print(f"   总记录数: {data['total']}")
            print("   ✅ 不带日期参数的查询成功")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 2. 测试带正确格式日期参数的查询
    print("\n2. 测试带正确格式日期参数的查询 (YYYY-MM-DD):")
    try:
        test_date = '2024-01-01'
        response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 5,
            'trade_date': test_date
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   查询日期: {test_date}")
            print(f"   返回记录数: {len(data['data'])}")
            print(f"   总记录数: {data['total']}")
            print("   ✅ 正确格式日期参数查询成功")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 3. 测试带错误格式日期参数的查询
    print("\n3. 测试带错误格式日期参数的查询:")
    try:
        test_date = '2024/01/01'  # 错误的日期格式
        response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 5,
            'trade_date': test_date
        })
        
        if response.status_code == 400:
            error_data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   错误日期格式: {test_date}")
            print(f"   错误信息: {error_data.get('error')}")
            print("   ✅ 错误格式日期参数被正确拒绝")
        else:
            print(f"   ⚠️  意外状态码: {response.status_code}")
            print(f"   响应内容: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 4. 测试带ts_code和日期的组合查询
    print("\n4. 测试带ts_code和日期的组合查询:")
    try:
        test_ts_code = '000001.SH'  # 上证指数
        test_date = '2024-01-01'
        response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 5,
            'ts_code': test_ts_code,
            'trade_date': test_date
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   查询代码: {test_ts_code}")
            print(f"   查询日期: {test_date}")
            print(f"   返回记录数: {len(data['data'])}")
            print(f"   总记录数: {data['total']}")
            print("   ✅ 组合查询成功")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 5. 测试日期格式转换的边界情况
    print("\n5. 测试日期格式转换的边界情况:")
    test_cases = [
        ('2024-12-31', '年末日期'),
        ('2024-02-29', '闰年日期'),
        ('2024-01-01', '年初日期'),
        ('2023-12-31', '去年年末'),
        ('2025-01-01', '明年年初')
    ]
    
    for test_date, description in test_cases:
        try:
            response = requests.get(f'{base_url}/api/ths_index_daily/', params={
                'page': 1,
                'page_size': 1,
                'trade_date': test_date
            })
            
            if response.status_code == 200:
                print(f"   ✅ {description}: {test_date} - 查询成功")
            else:
                print(f"   ❌ {description}: {test_date} - 查询失败，状态码: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {description}: {test_date} - 请求异常: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_trade_date_format() 