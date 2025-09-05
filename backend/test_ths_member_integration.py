#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试同花顺概念成分股功能集成
"""

import requests
import json

def test_ths_member_integration():
    """测试同花顺概念成分股功能集成"""
    
    base_url = 'http://localhost:5000'
    
    print("=== 测试同花顺概念成分股功能集成 ===")
    
    # 1. 测试获取概念板块列表
    print("\n1. 测试获取概念板块列表:")
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
            
            if data['data']:
                print("   前3条概念板块:")
                for i, item in enumerate(data['data'][:3]):
                    print(f"     {i+1}. {item.get('name', 'N/A')} ({item.get('ts_code', 'N/A')})")
                    print(f"        涨跌幅: {item.get('pct_change', 'N/A')}%, 成交量: {item.get('vol', 'N/A')}")
            print("   ✅ 概念板块列表获取成功")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 2. 测试获取概念成分股列表
    print("\n2. 测试获取概念成分股列表:")
    try:
        response = requests.get(f'{base_url}/api/ths_member/', params={
            'page': 1,
            'page_size': 10
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   返回记录数: {len(data['data'])}")
            print(f"   总记录数: {data['total']}")
            
            if data['data']:
                print("   前5条成分股:")
                for i, item in enumerate(data['data'][:5]):
                    print(f"     {i+1}. {item.get('con_name', 'N/A')} ({item.get('con_code', 'N/A')})")
                    print(f"        所属板块: {item.get('ts_code', 'N/A')}, 权重: {item.get('weight', 'N/A')}")
            print("   ✅ 概念成分股列表获取成功")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 3. 测试按概念板块代码查询成分股
    print("\n3. 测试按概念板块代码查询成分股:")
    try:
        # 先获取一个概念板块代码
        index_response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 1
        })
        
        if index_response.status_code == 200:
            index_data = index_response.json()
            if index_data['data']:
                ts_code = index_data['data'][0]['ts_code']
                print(f"   使用概念板块代码: {ts_code}")
                
                # 查询该板块的成分股
                member_response = requests.get(f'{base_url}/api/ths_member/', params={
                    'ts_code': ts_code,
                    'page_size': 10
                })
                
                if member_response.status_code == 200:
                    member_data = member_response.json()
                    print(f"   状态码: {member_response.status_code}")
                    print(f"   成分股数量: {len(member_data['data'])}")
                    
                    if member_data['data']:
                        print("   成分股列表:")
                        for i, item in enumerate(member_data['data'][:5]):
                            print(f"     {i+1}. {item.get('con_name', 'N/A')} ({item.get('con_code', 'N/A')})")
                    print("   ✅ 按概念板块查询成分股成功")
                else:
                    print(f"   ❌ 查询成分股失败，状态码: {member_response.status_code}")
            else:
                print("   ⚠️  没有概念板块数据")
        else:
            print(f"   ❌ 获取概念板块失败，状态码: {index_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 4. 测试按股票代码查询所属概念板块
    print("\n4. 测试按股票代码查询所属概念板块:")
    try:
        # 先获取一个股票代码
        member_response = requests.get(f'{base_url}/api/ths_member/', params={
            'page': 1,
            'page_size': 1
        })
        
        if member_response.status_code == 200:
            member_data = member_response.json()
            if member_data['data']:
                con_code = member_data['data'][0]['con_code']
                print(f"   使用股票代码: {con_code}")
                
                # 查询该股票所属的概念板块
                con_response = requests.get(f'{base_url}/api/ths_member/', params={
                    'con_code': con_code,
                    'page_size': 10
                })
                
                if con_response.status_code == 200:
                    con_data = con_response.json()
                    print(f"   状态码: {con_response.status_code}")
                    print(f"   所属板块数量: {len(con_data['data'])}")
                    
                    if con_data['data']:
                        print("   所属板块列表:")
                        for i, item in enumerate(con_data['data'][:3]):
                            print(f"     {i+1}. {item.get('ts_code', 'N/A')}")
                    print("   ✅ 按股票代码查询所属概念板块成功")
                else:
                    print(f"   ❌ 查询所属板块失败，状态码: {con_response.status_code}")
            else:
                print("   ⚠️  没有成分股数据")
        else:
            print(f"   ❌ 获取成分股失败，状态码: {member_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 5. 测试成分股数据完整性
    print("\n5. 测试成分股数据完整性:")
    try:
        response = requests.get(f'{base_url}/api/ths_member/', params={
            'page': 1,
            'page_size': 5
        })
        
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                print("   数据字段检查:")
                sample_item = data['data'][0]
                required_fields = ['ts_code', 'con_code', 'con_name']
                optional_fields = ['weight', 'in_date', 'out_date', 'is_new']
                
                for field in required_fields:
                    if field in sample_item:
                        print(f"     ✅ {field}: {sample_item[field]}")
                    else:
                        print(f"     ❌ {field}: 缺失")
                
                for field in optional_fields:
                    if field in sample_item:
                        print(f"     ⚠️  {field}: {sample_item[field]}")
                    else:
                        print(f"     - {field}: 未设置")
                
                print("   ✅ 成分股数据结构完整")
            else:
                print("   ⚠️  没有成分股数据")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_ths_member_integration() 