#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
大盘指数每日指标测试脚本
"""

import sys
import os
import requests
import json
from datetime import date

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# API基础URL
BASE_URL = "http://localhost:5000/api"

def test_get_index_by_ts_code():
    """测试根据TS代码获取指数数据"""
    print("=== 测试根据TS代码获取指数数据 ===")
    
    ts_code = "000001.SH"  # 上证综指
    url = f"{BASE_URL}/index_daily_basic/{ts_code}"
    
    try:
        response = requests.get(url)
        print(f"请求URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['success']}")
            print(f"数据条数: {data['total']}")
            if data['data']:
                print(f"最新数据: {data['data'][0]}")
        else:
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_get_latest_index():
    """测试获取最新指数数据"""
    print("\n=== 测试获取最新指数数据 ===")
    
    ts_code = "000300.SH"  # 沪深300
    url = f"{BASE_URL}/index_daily_basic/{ts_code}/latest"
    
    try:
        response = requests.get(url)
        print(f"请求URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['success']}")
            if data['data']:
                print(f"最新数据: {data['data']}")
        else:
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_get_index_by_date():
    """测试根据日期获取指数数据"""
    print("\n=== 测试根据日期获取指数数据 ===")
    
    trade_date = "2024-01-15"
    url = f"{BASE_URL}/index_daily_basic/date/{trade_date}"
    
    try:
        response = requests.get(url)
        print(f"请求URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['success']}")
            print(f"数据条数: {data['total']}")
            if data['data']:
                print(f"第一条数据: {data['data'][0]}")
        else:
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_get_index_by_date_range():
    """测试根据日期范围获取指数数据"""
    print("\n=== 测试根据日期范围获取指数数据 ===")
    
    ts_code = "000001.SH"
    start_date = "2024-01-01"
    end_date = "2024-01-31"
    url = f"{BASE_URL}/index_daily_basic/{ts_code}/date_range?start_date={start_date}&end_date={end_date}"
    
    try:
        response = requests.get(url)
        print(f"请求URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['success']}")
            print(f"数据条数: {data['total']}")
            if data['data']:
                print(f"第一条数据: {data['data'][0]}")
        else:
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_get_index_by_pe_range():
    """测试根据市盈率范围获取指数数据"""
    print("\n=== 测试根据市盈率范围获取指数数据 ===")
    
    min_pe = 10
    max_pe = 20
    url = f"{BASE_URL}/index_daily_basic/pe_range?min_pe={min_pe}&max_pe={max_pe}"
    
    try:
        response = requests.get(url)
        print(f"请求URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['success']}")
            print(f"数据条数: {data['total']}")
            if data['data']:
                print(f"第一条数据: {data['data'][0]}")
        else:
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_get_index_by_pb_range():
    """测试根据市净率范围获取指数数据"""
    print("\n=== 测试根据市净率范围获取指数数据 ===")
    
    min_pb = 1
    max_pb = 3
    url = f"{BASE_URL}/index_daily_basic/pb_range?min_pb={min_pb}&max_pb={max_pb}"
    
    try:
        response = requests.get(url)
        print(f"请求URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['success']}")
            print(f"数据条数: {data['total']}")
            if data['data']:
                print(f"第一条数据: {data['data'][0]}")
        else:
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_get_index_by_turnover_rate():
    """测试根据换手率范围获取指数数据"""
    print("\n=== 测试根据换手率范围获取指数数据 ===")
    
    min_rate = 0.5
    max_rate = 2.0
    url = f"{BASE_URL}/index_daily_basic/turnover_rate?min_rate={min_rate}&max_rate={max_rate}"
    
    try:
        response = requests.get(url)
        print(f"请求URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['success']}")
            print(f"数据条数: {data['total']}")
            if data['data']:
                print(f"第一条数据: {data['data'][0]}")
        else:
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_get_market_summary():
    """测试获取市场概况"""
    print("\n=== 测试获取市场概况 ===")
    
    trade_date = "2024-01-15"
    url = f"{BASE_URL}/index_daily_basic/market_summary?trade_date={trade_date}"
    
    try:
        response = requests.get(url)
        print(f"请求URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['success']}")
            if data['summary']:
                summary = data['summary']
                print(f"交易日期: {summary.get('trade_date')}")
                print(f"指数总数: {summary.get('total_indices')}")
                print(f"平均市盈率: {summary.get('avg_pe')}")
                print(f"平均市净率: {summary.get('avg_pb')}")
                print(f"平均换手率: {summary.get('avg_turnover_rate')}")
                print(f"总市值: {summary.get('total_market_value')}")
        else:
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_get_fields():
    """测试获取字段信息"""
    print("\n=== 测试获取字段信息 ===")
    
    url = f"{BASE_URL}/index_daily_basic/fields"
    
    try:
        response = requests.get(url)
        print(f"请求URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['success']}")
            if data['fields']:
                print("字段信息:")
                for field, description in data['fields'].items():
                    print(f"  {field}: {description}")
        else:
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_create_index_data():
    """测试创建指数数据"""
    print("\n=== 测试创建指数数据 ===")
    
    url = f"{BASE_URL}/index_daily_basic/"
    
    # 测试数据
    test_data = {
        "ts_code": "000001.SH",
        "trade_date": "20240115",
        "total_mv": 5000000000000,
        "float_mv": 4000000000000,
        "total_share": 1000000000000,
        "float_share": 800000000000,
        "free_share": 600000000000,
        "turnover_rate": 1.2,
        "turnover_rate_f": 1.5,
        "pe": 15.5,
        "pe_ttm": 16.2,
        "pb": 1.8
    }
    
    try:
        response = requests.post(url, json=test_data)
        print(f"请求URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['success']}")
            print(f"消息: {data['message']}")
            if data['data']:
                print(f"创建的数据: {data['data']}")
        else:
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_batch_create_index_data():
    """测试批量创建指数数据"""
    print("\n=== 测试批量创建指数数据 ===")
    
    url = f"{BASE_URL}/index_daily_basic/batch"
    
    # 测试数据
    test_data_list = [
        {
            "ts_code": "000300.SH",
            "trade_date": "20240115",
            "total_mv": 3000000000000,
            "float_mv": 2500000000000,
            "total_share": 800000000000,
            "float_share": 600000000000,
            "free_share": 500000000000,
            "turnover_rate": 0.8,
            "turnover_rate_f": 1.0,
            "pe": 12.5,
            "pe_ttm": 13.1,
            "pb": 1.5
        },
        {
            "ts_code": "000905.SH",
            "trade_date": "20240115",
            "total_mv": 2000000000000,
            "float_mv": 1800000000000,
            "total_share": 600000000000,
            "float_share": 500000000000,
            "free_share": 400000000000,
            "turnover_rate": 1.5,
            "turnover_rate_f": 1.8,
            "pe": 18.5,
            "pe_ttm": 19.2,
            "pb": 2.2
        }
    ]
    
    try:
        response = requests.post(url, json=test_data_list)
        print(f"请求URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['success']}")
            print(f"消息: {data['message']}")
            print(f"总数: {data['total']}")
            print(f"成功数: {data['success_count']}")
        else:
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {str(e)}")

def main():
    """主函数"""
    print("大盘指数每日指标API测试")
    print("=" * 50)
    
    try:
        # 测试各种API接口
        test_get_index_by_ts_code()
        test_get_latest_index()
        test_get_index_by_date()
        test_get_index_by_date_range()
        test_get_index_by_pe_range()
        test_get_index_by_pb_range()
        test_get_index_by_turnover_rate()
        test_get_market_summary()
        test_get_fields()
        test_create_index_data()
        test_batch_create_index_data()
        
        print("\n" + "=" * 50)
        print("测试完成！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 