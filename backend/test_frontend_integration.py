#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试前端集成所需的后端API
"""

import requests
import json

def test_frontend_integration():
    """测试前端集成所需的后端API"""
    
    base_url = 'http://localhost:5000'
    
    print("=== 测试前端集成所需的后端API ===")
    
    # 1. 测试同花顺指数日线数据API（主数据源）
    print("\n1. 测试同花顺指数日线数据API (/api/ths_index_daily):")
    try:
        response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 5
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 状态码: {response.status_code}")
            print(f"   返回记录数: {len(data['data'])}")
            print(f"   总记录数: {data['total']}")
            
            if data['data']:
                print("   前3条记录:")
                for i, item in enumerate(data['data'][:3]):
                    print(f"     {i+1}. {item.get('name', 'N/A')} ({item.get('ts_code', 'N/A')})")
                    print(f"         涨跌幅: {item.get('pct_change', 'N/A')}%, 成交量: {item.get('vol', 'N/A')}")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 2. 测试同花顺概念成分股API（展开行数据源）
    print("\n2. 测试同花顺概念成分股API (/api/ths_member):")
    try:
        response = requests.get(f'{base_url}/api/ths_member/', params={
            'page': 1,
            'pageSize': 10
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 状态码: {response.status_code}")
            print(f"   返回记录数: {len(data['data'])}")
            print(f"   总记录数: {data['total']}")
            
            if data['data']:
                print("   前5条成分股:")
                for i, item in enumerate(data['data'][:5]):
                    print(f"     {i+1}. {item.get('con_name', 'N/A')} ({item.get('con_code', 'N/A')})")
                    print(f"         所属板块: {item.get('ts_code', 'N/A')}")
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
                    print(f"   ✅ 状态码: {member_response.status_code}")
                    print(f"   成分股数量: {len(member_data['data'])}")
                    
                    if member_data['data']:
                        print("   成分股列表:")
                        for i, item in enumerate(member_data['data'][:3]):
                            print(f"     {i+1}. {item.get('con_name', 'N/A')} ({item.get('con_code', 'N/A')})")
                    else:
                        print("   ⚠️  该板块暂无成分股数据")
                else:
                    print(f"   ❌ 查询成分股失败，状态码: {member_response.status_code}")
                    print(f"   错误信息: {member_response.text}")
            else:
                print("   ⚠️  没有概念板块数据")
        else:
            print(f"   ❌ 获取概念板块失败，状态码: {index_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 4. 测试API响应格式
    print("\n4. 测试API响应格式:")
    try:
        # 测试成分股API响应格式
        response = requests.get(f'{base_url}/api/ths_member/', params={
            'page': 1,
            'pageSize': 1
        })
        
        if response.status_code == 200:
            data = response.json()
            print("   成分股API响应格式:")
            print(f"     - 包含 'data' 字段: {'data' in data}")
            print(f"     - 包含 'total' 字段: {'total' in data}")
            print(f"     - data 是数组: {isinstance(data.get('data'), list)}")
            
            if data.get('data') and len(data['data']) > 0:
                sample_item = data['data'][0]
                required_fields = ['ts_code', 'con_code', 'con_name']
                print("     样本数据字段:")
                for field in required_fields:
                    print(f"       - {field}: {field in sample_item} (值: {sample_item.get(field, 'N/A')})")
        else:
            print(f"   ❌ API响应异常，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 5. 测试前端需要的具体API调用
    print("\n5. 测试前端需要的具体API调用:")
    try:
        # 模拟前端展开行的API调用
        member_response = requests.get(f'{base_url}/api/ths_member/', params={
            'ts_code': '885001.TI',  # 测试一个具体的概念板块代码
            'page_size': 100
        })
        
        if member_response.status_code == 200:
            member_data = member_response.json()
            print(f"   ✅ 前端API调用成功")
            print(f"   概念板块 885001.TI 的成分股数量: {len(member_data['data'])}")
            
            if member_data['data']:
                print("   前3只成分股:")
                for i, item in enumerate(member_data['data'][:3]):
                    print(f"     {i+1}. {item.get('con_name', 'N/A')} ({item.get('con_code', 'N/A')})")
            else:
                print("   ⚠️  该概念板块暂无成分股数据")
        else:
            print(f"   ❌ 前端API调用失败，状态码: {member_response.status_code}")
            print(f"   错误信息: {member_response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_frontend_integration() 