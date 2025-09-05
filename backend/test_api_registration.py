#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试API注册是否正常
"""

import requests
import json

def test_api_registration():
    """测试API注册是否正常"""
    
    base_url = 'http://localhost:5000'
    
    print("=== 测试API注册是否正常 ===")
    
    # 1. 测试同花顺指数API
    print("\n1. 测试同花顺指数API (/api/ths_index):")
    try:
        response = requests.get(f'{base_url}/api/ths_index/', params={
            'page': 1,
            'pageSize': 5
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 状态码: {response.status_code}")
            print(f"   返回记录数: {len(data['data'])}")
            print(f"   总记录数: {data['total']}")
        else:
            print(f"   ❌ 状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 2. 测试同花顺指数日线API
    print("\n2. 测试同花顺指数日线API (/api/ths_index_daily):")
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
        else:
            print(f"   ❌ 状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 3. 测试同花顺概念成分股API
    print("\n3. 测试同花顺概念成分股API (/api/ths_member):")
    try:
        response = requests.get(f'{base_url}/api/ths_member/', params={
            'page': 1,
            'pageSize': 5
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 状态码: {response.status_code}")
            print(f"   返回记录数: {len(data['data'])}")
            print(f"   总记录数: {data['total']}")
        else:
            print(f"   ❌ 状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 4. 测试404错误（不存在的API）
    print("\n4. 测试404错误（不存在的API):")
    try:
        response = requests.get(f'{base_url}/api/nonexistent/')
        
        if response.status_code == 404:
            print(f"   ✅ 状态码: {response.status_code} (预期的404错误)")
        else:
            print(f"   ⚠️  意外状态码: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 5. 测试API根路径
    print("\n5. 测试API根路径:")
    try:
        response = requests.get(f'{base_url}/api/')
        
        if response.status_code == 404:
            print(f"   ✅ 状态码: {response.status_code} (预期的404错误，因为没有根路径)")
        else:
            print(f"   ⚠️  意外状态码: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_api_registration() 