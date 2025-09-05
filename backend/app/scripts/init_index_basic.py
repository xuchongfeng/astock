#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
指数基本信息初始化脚本
从Tushare获取指数基本信息并存储到数据库
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.index_basic import IndexBasic
import tushare as ts
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_index_basic():
    """初始化指数基本信息"""
    try:
        # 创建Flask应用
        app = create_app()
        
        with app.app_context():
            # 检查表是否存在，如果不存在则创建
            db.create_all()
            
            # 设置Tushare token（需要替换为实际的token）
            ts.set_token('82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
            pro = ts.pro_api()
            
            logger.info("开始获取指数基本信息...")
            
            # 获取所有市场的指数基本信息
            markets = ['SSE', 'SZSE', 'CSI', 'SW', 'CICC', 'MSCI', 'OTH']
            
            for market in markets:
                try:
                    logger.info(f"正在获取 {market} 市场的指数信息...")
                    
                    # 获取指数基本信息
                    df = pro.index_basic(market=market)
                    
                    if df is not None and not df.empty:
                        logger.info(f"获取到 {len(df)} 条 {market} 市场指数信息")
                        
                        for _, row in df.iterrows():
                            try:
                                # 检查是否已存在
                                existing = IndexBasic.query.filter_by(ts_code=row['ts_code']).first()
                                
                                if existing:
                                    # 更新现有记录
                                    for key, value in row.items():
                                        if hasattr(existing, key) and pd.notna(value):
                                            setattr(existing, key, value)
                                    existing.updated_at = datetime.now()
                                    logger.info(f"更新指数: {row['ts_code']} - {row['name']}")
                                else:
                                    # 创建新记录
                                    index_data = {}
                                    for key, value in row.items():
                                        if pd.notna(value):
                                            index_data[key] = value
                                    
                                    index = IndexBasic(**index_data)
                                    db.session.add(index)
                                    logger.info(f"新增指数: {row['ts_code']} - {row['name']}")
                                
                            except Exception as e:
                                logger.error(f"处理指数 {row.get('ts_code', 'Unknown')} 时出错: {e}")
                                continue
                        
                        # 提交当前市场的所有更改
                        db.session.commit()
                        logger.info(f"{market} 市场指数信息处理完成")
                        
                    else:
                        logger.warning(f"{market} 市场未获取到指数信息")
                        
                except Exception as e:
                    logger.error(f"获取 {market} 市场指数信息失败: {e}")
                    continue
            
            logger.info("指数基本信息初始化完成")
            
    except Exception as e:
        logger.error(f"初始化指数基本信息失败: {e}")
        raise

def get_index_basic_by_market(market):
    """获取指定市场的指数基本信息"""
    try:
        app = create_app()
        
        with app.app_context():
            db.create_all()
            
            ts.set_token('82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
            pro = ts.pro_api()
            
            logger.info(f"获取 {market} 市场指数信息...")
            
            df = pro.index_basic(market=market)
            
            if df is not None and not df.empty:
                logger.info(f"获取到 {len(df)} 条 {market} 市场指数信息")
                return df
            else:
                logger.warning(f"{market} 市场未获取到指数信息")
                return None
                
    except Exception as e:
        logger.error(f"获取 {market} 市场指数信息失败: {e}")
        return None

def get_index_basic_by_publisher(publisher):
    """获取指定发布方的指数基本信息"""
    try:
        app = create_app()
        
        with app.app_context():
            db.create_all()
            
            ts.set_token('82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
            pro = ts.pro_api()
            
            logger.info(f"获取 {publisher} 发布方指数信息...")
            
            df = pro.index_basic(publisher=publisher)
            
            if df is not None and not df.empty:
                logger.info(f"获取到 {len(df)} 条 {publisher} 发布方指数信息")
                return df
            else:
                logger.warning(f"{publisher} 发布方未获取到指数信息")
                return None
                
    except Exception as e:
        logger.error(f"获取 {publisher} 发布方指数信息失败: {e}")
        return None

if __name__ == '__main__':
    # 导入pandas（在函数内部导入避免循环导入问题）
    import pandas as pd
    
    # 初始化所有指数基本信息
    init_index_basic()
    
    # 示例：获取特定市场的指数信息
    # sse_indices = get_index_basic_by_market('SSE')
    # if sse_indices is not None:
    #     print(sse_indices.head())
    
    # 示例：获取申万指数信息
    # sw_indices = get_index_basic_by_publisher('SW')
    # if sw_indices is not None:
    #     print(sw_indices.head())
