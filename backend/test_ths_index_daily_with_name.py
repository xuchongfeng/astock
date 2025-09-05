#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试同花顺指数日线数据接口（包含指数名称）
"""

import requests
import json

def test_ths_index_daily_with_name():
    """测试获取包含指数名称的指数日线数据"""
    
    # 测试基础列表接口
    print("测试基础列表接口...")
    response = requests.get('http://localhost:5000/api/ths_index_daily/', params={
        'page': 1,
        'page_size': 5
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"状态码: {response.status_code}")
        print(f"总记录数: {data['total']}")
        print(f"返回记录数: {len(data['data'])}")
        
        if data['data']:
            print("\n第一条记录示例:")
            first_record = data['data'][0]
            print(f"  TS代码: {first_record.get('ts_code')}")
            print(f"  指数名称: {first_record.get('index_name')}")
            print(f"  交易日期: {first_record.get('trade_date')}")
            print(f"  收盘点位: {first_record.get('close')}")
            print(f"  涨跌幅: {first_record.get('pct_change')}%")
            
            # 检查是否包含指数名称字段
            if 'index_name' in first_record:
                print("✅ 成功：接口返回数据包含指数名称字段")
            else:
                print("❌ 失败：接口返回数据不包含指数名称字段")
        else:
            print("⚠️  警告：没有返回数据")
    else:
        print(f"❌ 请求失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
    
    # 测试带过滤条件的接口
    print("\n测试带过滤条件的接口...")
    response = requests.get('http://localhost:5000/api/ths_index_daily/', params={
        'ts_code': '000001.SH',  # 上证指数
        'page': 1,
        'page_size': 3
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"过滤后的记录数: {len(data['data'])}")
        if data['data']:
            print("过滤后的第一条记录:")
            first_record = data['data'][0]
            print(f"  TS代码: {first_record.get('ts_code')}")
            print(f"  指数名称: {first_record.get('index_name')}")
    else:
        print(f"过滤查询失败，状态码: {response.status_code}")

if __name__ == '__main__':
    print("开始测试同花顺指数日线数据接口（包含指数名称）")
    print("=" * 60)
    
    try:
        test_ths_index_daily_with_name()
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误：请确保后端服务正在运行 (http://localhost:5000)")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
    
    print("\n测试完成！") 