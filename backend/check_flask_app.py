#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Flask应用是否正确启动和配置
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def check_flask_app():
    """检查Flask应用配置"""
    app = create_app()
    
    print("=== 检查Flask应用配置 ===")
    
    # 1. 检查应用配置
    print(f"\n1. 应用配置:")
    print(f"   DEBUG模式: {app.debug}")
    print(f"   TESTING模式: {app.testing}")
    print(f"   SECRET_KEY: {'已设置' if app.config.get('SECRET_KEY') else '未设置'}")
    
    # 2. 检查数据库配置
    print(f"\n2. 数据库配置:")
    print(f"   SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI', '未设置')}")
    print(f"   SQLALCHEMY_TRACK_MODIFICATIONS: {app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS', '未设置')}")
    
    # 3. 检查注册的Blueprint
    print(f"\n3. 注册的Blueprint:")
    for rule in app.url_map.iter_rules():
        if rule.rule.startswith('/api/'):
            print(f"   {rule.rule} -> {rule.endpoint}")
    
    # 4. 检查数据库连接
    print(f"\n4. 数据库连接测试:")
    try:
        with app.app_context():
            # 测试数据库连接
            db.engine.execute('SELECT 1')
            print("   ✅ 数据库连接成功")
            
            # 检查ths_member表是否存在
            result = db.engine.execute("SHOW TABLES LIKE 'ths_member'")
            if result.fetchone():
                print("   ✅ ths_member表存在")
            else:
                print("   ❌ ths_member表不存在")
                
            # 检查ths_index表是否存在
            result = db.engine.execute("SHOW TABLES LIKE 'ths_index'")
            if result.fetchone():
                print("   ✅ ths_index表存在")
            else:
                print("   ❌ ths_index表不存在")
                
            # 检查ths_index_daily表是否存在
            result = db.engine.execute("SHOW TABLES LIKE 'ths_index_daily'")
            if result.fetchone():
                print("   ✅ ths_index_daily表存在")
            else:
                print("   ❌ ths_index_daily表不存在")
                
    except Exception as e:
        print(f"   ❌ 数据库连接失败: {e}")
    
    # 5. 检查模型导入
    print(f"\n5. 模型导入测试:")
    try:
        from app.models.ths_member import ThsMember
        print("   ✅ ThsMember模型导入成功")
        
        from app.models.ths_index import ThsIndex
        print("   ✅ ThsIndex模型导入成功")
        
        from app.models.ths_index_daily import ThsIndexDaily
        print("   ✅ ThsIndexDaily模型导入成功")
        
    except Exception as e:
        print(f"   ❌ 模型导入失败: {e}")
    
    # 6. 检查服务导入
    print(f"\n6. 服务导入测试:")
    try:
        from app.services.ths_member_service import get_all_ths_member
        print("   ✅ ths_member_service导入成功")
        
        from app.services.ths_index_service import get_all_ths_index
        print("   ✅ ths_index_service导入成功")
        
        from app.services.ths_index_daily_service import get_all_ths_index_daily
        print("   ✅ ths_index_daily_service导入成功")
        
    except Exception as e:
        print(f"   ❌ 服务导入失败: {e}")
    
    print(f"\n=== 检查完成 ===")

if __name__ == '__main__':
    check_flask_app() 