#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试同花顺指数日线数据查询
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.ths_index_daily import ThsIndexDaily
from app.models.ths_index import ThsIndex
from sqlalchemy import text

def debug_ths_index_query():
    """调试指数日线数据查询"""
    app = create_app()
    
    with app.app_context():
        print("=== 调试同花顺指数日线数据查询 ===")
        
        # 1. 检查基础数据
        print("\n1. 检查基础数据:")
        daily_count = ThsIndexDaily.query.count()
        index_count = ThsIndex.query.count()
        print(f"   ThsIndexDaily 记录数: {daily_count}")
        print(f"   ThsIndex 记录数: {index_count}")
        
        if daily_count > 0:
            # 查看前几条日线数据
            daily_samples = ThsIndexDaily.query.limit(3).all()
            print(f"   前3条日线数据:")
            for i, daily in enumerate(daily_samples):
                print(f"     {i+1}. ts_code: {daily.ts_code}, trade_date: {daily.trade_date}")
        
        if index_count > 0:
            # 查看前几条指数数据
            index_samples = ThsIndex.query.limit(3).all()
            print(f"   前3条指数数据:")
            for i, index in enumerate(index_samples):
                print(f"     {i+1}. ts_code: {index.ts_code}, name: {index.name}")
        
        # 2. 测试JOIN查询
        print("\n2. 测试JOIN查询:")
        try:
            # 使用原生SQL查询
            sql = """
            SELECT 
                d.id, d.ts_code, d.trade_date, d.close,
                i.name as index_name
            FROM ths_index_daily d
            LEFT JOIN ths_index i ON d.ts_code = i.ts_code
            LIMIT 5
            """
            
            result = db.session.execute(text(sql))
            rows = result.fetchall()
            
            print(f"   JOIN查询结果 (前5条):")
            for i, row in enumerate(rows):
                print(f"     {i+1}. ts_code: {row.ts_code}, name: {row.index_name}, date: {row.trade_date}")
                
        except Exception as e:
            print(f"   JOIN查询失败: {e}")
        
        # 3. 测试SQLAlchemy查询
        print("\n3. 测试SQLAlchemy查询:")
        try:
            query = db.session.query(
                ThsIndexDaily,
                ThsIndex.name
            ).outerjoin(
                ThsIndex, 
                ThsIndexDaily.ts_code == ThsIndex.ts_code
            ).limit(5)
            
            items = query.all()
            print(f"   SQLAlchemy查询结果 (前5条):")
            for i, item in enumerate(items):
                daily = item[0]
                index_name = item[1]
                print(f"     {i+1}. ts_code: {daily.ts_code}, name: {index_name}, date: {daily.trade_date}")
                
        except Exception as e:
            print(f"   SQLAlchemy查询失败: {e}")
        
        # 4. 检查是否有重复的ts_code
        print("\n4. 检查ts_code重复情况:")
        try:
            # 检查日线数据中的ts_code分布
            daily_ts_codes = db.session.query(ThsIndexDaily.ts_code).distinct().all()
            print(f"   日线数据中不同的ts_code数量: {len(daily_ts_codes)}")
            
            if len(daily_ts_codes) <= 10:
                print(f"   ts_code列表: {[code[0] for code in daily_ts_codes]}")
            
            # 检查指数数据中的ts_code分布
            index_ts_codes = db.session.query(ThsIndex.ts_code).distinct().all()
            print(f"   指数数据中不同的ts_code数量: {len(index_ts_codes)}")
            
            if len(index_ts_codes) <= 10:
                print(f"   ts_code列表: {[code[0] for code in index_ts_codes]}")
                
        except Exception as e:
            print(f"   检查ts_code失败: {e}")

if __name__ == '__main__':
    debug_ths_index_query() 