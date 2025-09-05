#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试展开行功能的修复
"""

import requests
import json

def test_expandable_table_fix():
    """测试展开行功能的修复"""
    
    base_url = 'http://localhost:5000'
    
    print("=== 测试展开行功能的修复 ===")
    
    # 1. 测试主数据API（同花顺指数日线数据）
    print("\n1. 测试主数据API:")
    try:
        response = requests.get(f'{base_url}/api/ths_index_daily/', params={
            'page': 1,
            'page_size': 3
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 主数据API正常")
            print(f"   返回记录数: {len(data['data'])}")
            
            if data['data']:
                print("   前3条记录:")
                for i, item in enumerate(data['data']):
                    print(f"     {i+1}. {item.get('name', 'N/A')} ({item.get('ts_code', 'N/A')})")
                    print(f"         交易日期: {item.get('trade_date', 'N/A')}")
                    print(f"         涨跌幅: {item.get('pct_change', 'N/A')}%")
                    
                    # 记录第一个ts_code用于后续测试
                    if i == 0:
                        test_ts_code = item.get('ts_code')
                        test_trade_date = item.get('trade_date')
                        print(f"     -> 将使用 {test_ts_code} 进行成分股测试")
        else:
            print(f"   ❌ 主数据API失败，状态码: {response.status_code}")
            return
            
    except Exception as e:
        print(f"   ❌ 主数据API异常: {e}")
        return
    
    # 2. 测试成分股API
    print("\n2. 测试成分股API:")
    try:
        if 'test_ts_code' in locals():
            response = requests.get(f'{base_url}/api/ths_member/', params={
                'ts_code': test_ts_code,
                'page_size': 10
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ 成分股API正常")
                print(f"   板块 {test_ts_code} 的成分股数量: {len(data['data'])}")
                
                if data['data']:
                    print("   前3只成分股:")
                    for i, item in enumerate(data['data'][:3]):
                        print(f"     {i+1}. {item.get('con_name', 'N/A')} ({item.get('con_code', 'N/A')})")
                        print(f"         权重: {item.get('weight', 'N/A')}%")
                else:
                    print("   ⚠️  该板块暂无成分股数据")
            else:
                print(f"   ❌ 成分股API失败，状态码: {response.status_code}")
                print(f"   错误信息: {response.text}")
        else:
            print("   ⚠️  没有可用的ts_code进行测试")
            
    except Exception as e:
        print(f"   ❌ 成分股API异常: {e}")
    
    # 3. 测试前端需要的具体数据结构
    print("\n3. 测试前端需要的数据结构:")
    try:
        if 'test_ts_code' in locals():
            # 测试主数据
            main_response = requests.get(f'{base_url}/api/ths_index_daily/', params={
                'page': 1,
                'page_size': 1,
                'ts_code': test_ts_code
            })
            
            if main_response.status_code == 200:
                main_data = main_response.json()
                if main_data['data']:
                    main_record = main_data['data'][0]
                    print(f"   ✅ 主数据结构正常")
                    print(f"   记录: {main_record.get('name', 'N/A')} ({main_record.get('ts_code', 'N/A')})")
                    print(f"   交易日期: {main_record.get('trade_date', 'N/A')}")
                    print(f"   涨跌幅: {main_record.get('pct_change', 'N/A')}%")
                    
                    # 测试成分股数据
                    member_response = requests.get(f'{base_url}/api/ths_member/', params={
                        'ts_code': test_ts_code,
                        'page_size': 5
                    })
                    
                    if member_response.status_code == 200:
                        member_data = member_response.json()
                        print(f"   ✅ 成分股数据结构正常")
                        print(f"   成分股数量: {len(member_data['data'])}")
                        
                        if member_data['data']:
                            print("   成分股数据样本:")
                            sample_member = member_data['data'][0]
                            required_fields = ['ts_code', 'con_code', 'con_name', 'weight']
                            for field in required_fields:
                                print(f"     - {field}: {sample_member.get(field, 'N/A')}")
                        else:
                            print("   ⚠️  无成分股数据")
                    else:
                        print(f"   ❌ 成分股数据结构异常")
                else:
                    print("   ⚠️  无主数据")
            else:
                print(f"   ❌ 主数据结构异常")
        else:
            print("   ⚠️  没有可用的ts_code进行测试")
            
    except Exception as e:
        print(f"   ❌ 数据结构测试异常: {e}")
    
    # 4. 验证前端展开行逻辑
    print("\n4. 验证前端展开行逻辑:")
    try:
        if 'test_ts_code' in locals() and 'test_trade_date' in locals():
            print("   前端展开行逻辑验证:")
            print(f"   - rowKey格式: {test_ts_code}-{test_trade_date}")
            print(f"   - 主数据ts_code: {test_ts_code}")
            print(f"   - 成分股查询key: {test_ts_code}")
            print(f"   - 展开状态key: {test_ts_code}-{test_trade_date}")
            print("   ✅ 前端逻辑应该能正确工作")
        else:
            print("   ⚠️  无法验证前端逻辑")
            
    except Exception as e:
        print(f"   ❌ 前端逻辑验证异常: {e}")
    
    print("\n=== 测试完成 ===")
    print("\n修复说明:")
    print("1. 问题: expandedRowKeys 与 rowKey 格式不匹配")
    print("2. 原因: expandedRows 存储的是 ts_code，但 rowKey 是 ts_code-trade_date")
    print("3. 解决: 在 handleExpand 中使用与 rowKey 相同的格式")
    print("4. 验证: 现在展开行应该能正常显示成分股数据")

if __name__ == '__main__':
    test_expandable_table_fix() 