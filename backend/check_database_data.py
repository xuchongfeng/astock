#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中的数据情况
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.ths_member import ThsMember
from app.models.ths_index import ThsIndex
from app.models.ths_index_daily import ThsIndexDaily

def check_database_data():
    """检查数据库中的数据情况"""
    app = create_app()
    
    with app.app_context():
        print("=== 检查数据库中的数据情况 ===")
        
        # 1. 检查同花顺指数表
        print("\n1. 同花顺指数表 (ths_index):")
        try:
            index_count = ThsIndex.query.count()
            print(f"   总记录数: {index_count}")
            
            if index_count > 0:
                # 显示前几条记录
                indices = ThsIndex.query.limit(5).all()
                print("   前5条记录:")
                for i, index in enumerate(indices):
                    print(f"     {i+1}. {index.name} ({index.ts_code}) - 类型: {index.type}")
            else:
                print("   ⚠️  表中没有数据")
                
        except Exception as e:
            print(f"   ❌ 查询失败: {e}")
        
        # 2. 检查同花顺指数日线表
        print("\n2. 同花顺指数日线表 (ths_index_daily):")
        try:
            daily_count = ThsIndexDaily.query.count()
            print(f"   总记录数: {daily_count}")
            
            if daily_count > 0:
                # 显示前几条记录
                dailies = ThsIndexDaily.query.limit(5).all()
                print("   前5条记录:")
                for i, daily in enumerate(dailies):
                    print(f"     {i+1}. {daily.ts_code} - {daily.trade_date} - 涨跌幅: {daily.pct_change}%")
            else:
                print("   ⚠️  表中没有数据")
                
        except Exception as e:
            print(f"   ❌ 查询失败: {e}")
        
        # 3. 检查同花顺概念成分股表
        print("\n3. 同花顺概念成分股表 (ths_member):")
        try:
            member_count = ThsMember.query.count()
            print(f"   总记录数: {member_count}")
            
            if member_count > 0:
                # 显示前几条记录
                members = ThsMember.query.limit(5).all()
                print("   前5条记录:")
                for i, member in enumerate(members):
                    print(f"     {i+1}. {member.con_name} ({member.con_code}) - 板块: {member.ts_code}")
                
                # 统计不同板块的成分股数量
                from sqlalchemy import func
                ts_code_stats = db.session.query(
                    ThsMember.ts_code,
                    func.count(ThsMember.id).label('count')
                ).group_by(ThsMember.ts_code).all()
                
                print(f"   板块统计 (共{len(ts_code_stats)}个板块):")
                for ts_code, count in ts_code_stats[:5]:  # 只显示前5个
                    print(f"     - {ts_code}: {count}只成分股")
                    
            else:
                print("   ⚠️  表中没有数据")
                
        except Exception as e:
            print(f"   ❌ 查询失败: {e}")
        
        # 4. 检查数据关联性
        print("\n4. 数据关联性检查:")
        try:
            if member_count > 0 and daily_count > 0:
                # 检查是否有匹配的数据
                sample_member = ThsMember.query.first()
                if sample_member:
                    ts_code = sample_member.ts_code
                    print(f"   检查板块 {ts_code} 的数据关联:")
                    
                    # 检查该板块是否有日线数据
                    daily_data = ThsIndexDaily.query.filter_by(ts_code=ts_code).count()
                    print(f"     - 日线数据: {daily_data} 条")
                    
                    # 检查该板块有多少成分股
                    member_data = ThsMember.query.filter_by(ts_code=ts_code).count()
                    print(f"     - 成分股: {member_data} 只")
                    
                    if daily_data > 0 and member_data > 0:
                        print("     ✅ 数据关联正常")
                    else:
                        print("     ⚠️  数据关联不完整")
            else:
                print("   ⚠️  数据不足，无法检查关联性")
                
        except Exception as e:
            print(f"   ❌ 关联性检查失败: {e}")
        
        print("\n=== 检查完成 ===")

if __name__ == '__main__':
    check_database_data() 