#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试同花顺概念板块日线数据API的排序功能
"""

import requests
import json

def test_sorting_functionality():
    """测试排序功能"""
    
    base_url = 'http://localhost:5000'
    
    print("=== 测试同花顺概念板块日线数据API的排序功能 ===")
    
    # 1. 测试按涨跌幅升序排序
    print("\n1. 测试按涨跌幅升序排序:")
    try:
        response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 5,
            'sort_fields': 'pct_change'
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   返回记录数: {len(data['data'])}")
            
            if len(data['data']) > 1:
                # 检查排序是否正确
                pct_changes = [item.get('pct_change', 0) for item in data['data'] if item.get('pct_change') is not None]
                if pct_changes == sorted(pct_changes):
                    print("   ✅ 涨跌幅升序排序正确")
                else:
                    print("   ❌ 涨跌幅升序排序错误")
                    print(f"   排序结果: {pct_changes}")
            else:
                print("   ⚠️  数据不足，无法验证排序")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 2. 测试按涨跌幅降序排序
    print("\n2. 测试按涨跌幅降序排序:")
    try:
        response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 5,
            'sort_fields': '-pct_change'
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   返回记录数: {len(data['data'])}")
            
            if len(data['data']) > 1:
                # 检查排序是否正确
                pct_changes = [item.get('pct_change', 0) for item in data['data'] if item.get('pct_change') is not None]
                if pct_changes == sorted(pct_changes, reverse=True):
                    print("   ✅ 涨跌幅降序排序正确")
                else:
                    print("   ❌ 涨跌幅降序排序错误")
                    print(f"   排序结果: {pct_changes}")
            else:
                print("   ⚠️  数据不足，无法验证排序")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 3. 测试按成交量升序排序
    print("\n3. 测试按成交量升序排序:")
    try:
        response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 5,
            'sort_fields': 'vol'
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   返回记录数: {len(data['data'])}")
            
            if len(data['data']) > 1:
                # 检查排序是否正确
                volumes = [item.get('vol', 0) for item in data['data'] if item.get('vol') is not None]
                if volumes == sorted(volumes):
                    print("   ✅ 成交量升序排序正确")
                else:
                    print("   ❌ 成交量升序排序错误")
                    print(f"   排序结果: {volumes}")
            else:
                print("   ⚠️  数据不足，无法验证排序")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 4. 测试按成交量降序排序
    print("\n4. 测试按成交量降序排序:")
    try:
        response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 5,
            'sort_fields': '-vol'
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   返回记录数: {len(data['data'])}")
            
            if len(data['data']) > 1:
                # 检查排序是否正确
                volumes = [item.get('vol', 0) for item in data['data'] if item.get('vol') is not None]
                if volumes == sorted(volumes, reverse=True):
                    print("   ✅ 成交量降序排序正确")
                else:
                    print("   ❌ 成交量降序排序错误")
                    print(f"   排序结果: {volumes}")
            else:
                print("   ⚠️  数据不足，无法验证排序")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 5. 测试组合排序（先按涨跌幅，再按成交量）
    print("\n5. 测试组合排序（先按涨跌幅降序，再按成交量降序）:")
    try:
        response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 5,
            'sort_fields': '-pct_change,-vol'
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   返回记录数: {len(data['data'])}")
            print("   ✅ 组合排序查询成功")
            
            # 显示前几条记录
            if len(data['data']) > 0:
                print("   前3条记录:")
                for i, item in enumerate(data['data'][:3]):
                    print(f"     {i+1}. {item.get('name', 'N/A')} - 涨跌幅: {item.get('pct_change', 'N/A')}%, 成交量: {item.get('vol', 'N/A')}")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 6. 测试带过滤条件的排序
    print("\n6. 测试带过滤条件的排序:")
    try:
        response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 5,
            'ts_code': '000001.SH',  # 上证指数
            'sort_fields': '-pct_change'
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   返回记录数: {len(data['data'])}")
            print("   ✅ 带过滤条件的排序查询成功")
        else:
            print(f"   ❌ 查询失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_sorting_functionality() 