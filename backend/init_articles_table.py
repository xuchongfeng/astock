#!/usr/bin/env python3
"""
初始化文章表脚本
运行此脚本创建文章相关的数据库表
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.article import Article

def init_articles_table():
    """初始化文章表"""
    app = create_app()
    
    with app.app_context():
        try:
            # 创建文章表
            db.create_all()
            print("✅ 文章表创建成功！")
            
            # 检查表是否创建成功
            if Article.query.first() is None:
                print("✅ 文章表结构验证成功！")
            else:
                print("✅ 文章表已存在，验证成功！")
                
        except Exception as e:
            print(f"❌ 创建文章表失败: {str(e)}")
            return False
    
    return True

if __name__ == '__main__':
    print("🚀 开始初始化文章表...")
    success = init_articles_table()
    
    if success:
        print("🎉 文章表初始化完成！")
        print("\n📋 表结构说明:")
        print("- articles: 用户文章表")
        print("- 支持文章分类、标签、状态管理")
        print("- 支持公开/私有设置")
        print("- 支持浏览和点赞统计")
    else:
        print("💥 文章表初始化失败！")
        sys.exit(1)
