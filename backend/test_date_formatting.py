#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试同花顺概念板块日期格式化功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.ths_index import ThsIndex
from app.models.ths_index_daily import ThsIndexDaily
from app.models.ths_member import ThsMember
from datetime import datetime, date

def test_date_formatting():
    """测试日期格式化功能"""
    app = create_app()
    
    with app.app_context():
        print("=== 测试同花顺概念板块日期格式化功能 ===")
        
        # 1. 测试 ThsIndex 模型
        print("\n1. 测试 ThsIndex 模型:")
        try:
            # 创建测试数据
            test_index = ThsIndex(
                ts_code='TEST001.TI',
                name='测试概念板块',
                count=100,
                exchange='SZSE',
                list_date=date(2024, 1, 1),
                type='N',
                created_at=datetime(2024, 1, 1, 10, 0, 0),
                updated_at=datetime(2024, 1, 1, 10, 0, 0)
            )
            
            # 测试 as_dict 方法
            index_dict = test_index.as_dict()
            print(f"   ts_code: {index_dict.get('ts_code')}")
            print(f"   name: {index_dict.get('name')}")
            print(f"   list_date: {index_dict.get('list_date')} (类型: {type(index_dict.get('list_date'))})")
            print(f"   created_at: {index_dict.get('created_at')} (类型: {type(index_dict.get('created_at'))})")
            print(f"   updated_at: {index_dict.get('updated_at')} (类型: {type(index_dict.get('updated_at'))})")
            
            # 验证日期格式
            if (index_dict.get('list_date') == '2024-01-01' and 
                index_dict.get('created_at') == '2024-01-01' and 
                index_dict.get('updated_at') == '2024-01-01'):
                print("   ✅ ThsIndex 日期格式化成功")
            else:
                print("   ❌ ThsIndex 日期格式化失败")
                
        except Exception as e:
            print(f"   ❌ ThsIndex 测试失败: {e}")
        
        # 2. 测试 ThsIndexDaily 模型
        print("\n2. 测试 ThsIndexDaily 模型:")
        try:
            # 创建测试数据
            test_daily = ThsIndexDaily(
                ts_code='TEST001.TI',
                trade_date=date(2024, 1, 1),
                close=1000.0,
                open=990.0,
                high=1010.0,
                low=980.0,
                pre_close=985.0,
                avg_price=995.0,
                change=15.0,
                pct_change=1.5,
                vol=1000000.0,
                turnover_rate=2.5,
                total_mv=500000000000.0,
                float_mv=300000000000.0,
                created_at=datetime(2024, 1, 1, 10, 0, 0),
                updated_at=datetime(2024, 1, 1, 10, 0, 0)
            )
            
            # 测试 as_dict 方法
            daily_dict = test_daily.as_dict()
            print(f"   ts_code: {daily_dict.get('ts_code')}")
            print(f"   trade_date: {daily_dict.get('trade_date')} (类型: {type(daily_dict.get('trade_date'))})")
            print(f"   close: {daily_dict.get('close')}")
            print(f"   created_at: {daily_dict.get('created_at')} (类型: {type(daily_dict.get('created_at'))})")
            print(f"   updated_at: {daily_dict.get('updated_at')} (类型: {type(daily_dict.get('updated_at'))})")
            
            # 验证日期格式
            if (daily_dict.get('trade_date') == '2024-01-01' and 
                daily_dict.get('created_at') == '2024-01-01' and 
                daily_dict.get('updated_at') == '2024-01-01'):
                print("   ✅ ThsIndexDaily 日期格式化成功")
            else:
                print("   ❌ ThsIndexDaily 日期格式化失败")
                
        except Exception as e:
            print(f"   ❌ ThsIndexDaily 测试失败: {e}")
        
        # 3. 测试 ThsMember 模型
        print("\n3. 测试 ThsMember 模型:")
        try:
            # 创建测试数据
            test_member = ThsMember(
                ts_code='TEST001.TI',
                con_code='000001.SZ',
                con_name='测试股票',
                weight=1.5,
                in_date=date(2024, 1, 1),
                out_date=None,
                is_new='Y',
                created_at=datetime(2024, 1, 1, 10, 0, 0),
                updated_at=datetime(2024, 1, 1, 10, 0, 0)
            )
            
            # 测试 as_dict 方法
            member_dict = test_member.as_dict()
            print(f"   ts_code: {member_dict.get('ts_code')}")
            print(f"   con_code: {member_dict.get('con_code')}")
            print(f"   in_date: {member_dict.get('in_date')} (类型: {type(member_dict.get('in_date'))})")
            print(f"   out_date: {member_dict.get('out_date')} (类型: {type(member_dict.get('out_date'))})")
            print(f"   created_at: {member_dict.get('created_at')} (类型: {type(member_dict.get('created_at'))})")
            print(f"   updated_at: {member_dict.get('updated_at')} (类型: {type(member_dict.get('updated_at'))})")
            
            # 验证日期格式
            if (member_dict.get('in_date') == '2024-01-01' and 
                member_dict.get('out_date') is None and
                member_dict.get('created_at') == '2024-01-01' and 
                member_dict.get('updated_at') == '2024-01-01'):
                print("   ✅ ThsMember 日期格式化成功")
            else:
                print("   ❌ ThsMember 日期格式化失败")
                
        except Exception as e:
            print(f"   ❌ ThsMember 测试失败: {e}")
        
        print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_date_formatting() 