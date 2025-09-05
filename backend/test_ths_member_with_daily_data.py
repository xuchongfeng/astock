#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试带涨幅信息的成分股API功能
"""

import requests
import json

def test_ths_member_with_daily_data():
    """测试带涨幅信息的成分股API功能"""
    
    base_url = 'http://localhost:5000'
    
    print("=== 测试带涨幅信息的成分股API功能 ===")
    
    # 1. 测试不带trade_date参数的原有功能
    print("\n1. 测试不带trade_date参数的原有功能:")
    try:
        response = requests.get(f'{base_url}/api/ths_member/', params={
            'page': 1,
            'pageSize': 5
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 原有API正常")
            print(f"   返回记录数: {len(data['data'])}")
            print(f"   总记录数: {data['total']}")
            
            if data['data']:
                print("   前3条记录:")
                for i, item in enumerate(data['data'][:3]):
                    print(f"     {i+1}. {item.get('con_name', 'N/A')} ({item.get('con_code', 'N/A')})")
                    print(f"         所属板块: {item.get('ts_code', 'N/A')}")
                    print(f"         权重: {item.get('weight', 'N/A')}%")
        else:
            print(f"   ❌ 原有API失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 原有API异常: {e}")
    
    # 2. 测试带trade_date参数的新功能
    print("\n2. 测试带trade_date参数的新功能:")
    try:
        # 使用一个具体的交易日期
        trade_date = '2024-01-15'  # 可以根据实际情况调整
        
        response = requests.get(f'{base_url}/api/ths_member/', params={
            'page': 1,
            'pageSize': 10,
            'trade_date': trade_date
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 新API正常")
            print(f"   交易日期: {data.get('trade_date', 'N/A')}")
            print(f"   返回记录数: {len(data['data'])}")
            print(f"   总记录数: {data['total']}")
            
            if data['data']:
                print("   前5条记录（按涨幅倒序）:")
                for i, item in enumerate(data['data'][:5]):
                    print(f"     {i+1}. {item.get('con_name', 'N/A')} ({item.get('con_code', 'N/A')})")
                    print(f"         涨跌幅: {item.get('pct_chg', 'N/A')}%")
                    print(f"         涨跌额: {item.get('change', 'N/A')}")
                    print(f"         收盘价: {item.get('close', 'N/A')}")
                    print(f"         成交量: {item.get('vol', 'N/A')}手")
                    print(f"         权重: {item.get('weight', 'N/A')}%")
        else:
            print(f"   ❌ 新API失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 新API异常: {e}")
    
    # 3. 测试按板块代码过滤
    print("\n3. 测试按板块代码过滤:")
    try:
        # 先获取一个板块代码
        member_response = requests.get(f'{base_url}/api/ths_member/', params={
            'page': 1,
            'pageSize': 1
        })
        
        if member_response.status_code == 200:
            member_data = member_response.json()
            if member_data['data']:
                ts_code = member_data['data'][0]['ts_code']
                print(f"   使用板块代码: {ts_code}")
                
                # 测试该板块的成分股（带涨幅信息）
                response = requests.get(f'{base_url}/api/ths_member/', params={
                    'ts_code': ts_code,
                    'page': 1,
                    'pageSize': 10,
                    'trade_date': '2024-01-15'
                })
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ 板块过滤成功")
                    print(f"   板块 {ts_code} 的成分股数量: {len(data['data'])}")
                    
                    if data['data']:
                        print("   前3只成分股（按涨幅倒序）:")
                        for i, item in enumerate(data['data'][:3]):
                            print(f"     {i+1}. {item.get('con_name', 'N/A')} ({item.get('con_code', 'N/A')})")
                            print(f"         涨跌幅: {item.get('pct_chg', 'N/A')}%")
                            print(f"         涨跌额: {item.get('change', 'N/A')}")
                            print(f"         权重: {item.get('weight', 'N/A')}%")
                    else:
                        print("   ⚠️  该板块暂无成分股数据")
                else:
                    print(f"   ❌ 板块过滤失败，状态码: {response.status_code}")
            else:
                print("   ⚠️  没有可用的板块代码")
        else:
            print(f"   ❌ 获取板块代码失败，状态码: {member_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 板块过滤测试异常: {e}")
    
    # 4. 测试数据格式和排序
    print("\n4. 测试数据格式和排序:")
    try:
        response = requests.get(f'{base_url}/api/ths_member/', params={
            'page': 1,
            'pageSize': 20,
            'trade_date': '2024-01-15'
        })
        
        if response.status_code == 200:
            data = response.json()
            print("   数据格式验证:")
            
            if data['data']:
                # 检查涨幅字段
                sample_item = data['data'][0]
                required_fields = ['pct_chg', 'change', 'close', 'vol', 'weight']
                for field in required_fields:
                    print(f"     - {field}: {field in sample_item} (值: {sample_item.get(field, 'N/A')})")
                
                # 检查排序（应该按涨幅倒序）
                print("   排序验证（前5条）:")
                for i, item in enumerate(data['data'][:5]):
                    pct_chg = item.get('pct_chg')
                    if pct_chg is not None:
                        print(f"     {i+1}. 涨跌幅: {pct_chg}%")
                    else:
                        print(f"     {i+1}. 涨跌幅: 无数据")
                
                # 验证排序是否正确
                pct_changes = [item.get('pct_chg') for item in data['data'] if item.get('pct_chg') is not None]
                if len(pct_changes) >= 2:
                    is_sorted = all(pct_changes[i] >= pct_changes[i+1] for i in range(len(pct_changes)-1))
                    print(f"     ✅ 排序验证: {'正确（倒序）' if is_sorted else '错误'}")
                else:
                    print("     ⚠️  数据不足，无法验证排序")
            else:
                print("   ⚠️  无数据")
        else:
            print(f"   ❌ 数据格式测试失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 数据格式测试异常: {e}")
    
    # 5. 测试错误处理
    print("\n5. 测试错误处理:")
    try:
        # 测试无效的日期格式
        response = requests.get(f'{base_url}/api/ths_member/', params={
            'trade_date': 'invalid-date'
        })
        
        if response.status_code == 400:
            print("   ✅ 无效日期格式处理正确")
            error_data = response.json()
            print(f"   错误信息: {error_data.get('error', 'N/A')}")
        else:
            print(f"   ❌ 无效日期格式处理异常，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 错误处理测试异常: {e}")
    
    print("\n=== 测试完成 ===")
    print("\n功能说明:")
    print("1. 新增 trade_date 参数支持")
    print("2. 关联 stock_daily 表获取涨幅信息")
    print("3. 按涨幅倒序排序")
    print("4. 返回完整的成分股和涨幅数据")
    print("5. 保持向后兼容性")

if __name__ == '__main__':
    test_ths_member_with_daily_data() 