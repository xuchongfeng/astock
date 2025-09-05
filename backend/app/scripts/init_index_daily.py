#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
指数日线行情初始化脚本
从Tushare获取指数日线行情数据并存储到数据库
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.index_daily import IndexDaily
from app.models.index_basic import IndexBasic
import tushare as ts
import logging
from datetime import datetime, timedelta
import pandas as pd

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_index_daily_by_ts_code(ts_code, start_date=None, end_date=None):
    """初始化指定指数的日线行情数据"""
    try:
        app = create_app()
        
        with app.app_context():
            # 检查表是否存在，如果不存在则创建
            db.create_all()
            
            # 设置Tushare token（需要替换为实际的token）
            ts.set_token('82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
            pro = ts.pro_api()
            
            # 如果没有指定日期范围，默认获取最近30天的数据
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')
            
            logger.info(f"开始获取指数 {ts_code} 从 {start_date} 到 {end_date} 的日线行情...")
            
            # 获取指数日线行情
            df = pro.index_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            
            if df is not None and not df.empty:
                logger.info(f"获取到 {len(df)} 条 {ts_code} 日线行情数据")
                
                success_count = 0
                for _, row in df.iterrows():
                    try:
                        # 检查是否已存在
                        existing = IndexDaily.query.filter_by(
                            ts_code=row['ts_code'],
                            trade_date=datetime.strptime(row['trade_date'], '%Y%m%d').date()
                        ).first()
                        
                        if existing:
                            # 更新现有记录
                            for key, value in row.items():
                                if hasattr(existing, key) and pd.notna(value):
                                    if key == 'trade_date':
                                        # 转换日期格式
                                        value = datetime.strptime(str(value), '%Y%m%d').date()
                                    setattr(existing, key, value)
                            existing.updated_at = datetime.now()
                            logger.debug(f"更新日线行情: {row['ts_code']} - {row['trade_date']}")
                        else:
                            # 创建新记录
                            daily_data = {}
                            for key, value in row.items():
                                if pd.notna(value):
                                    if key == 'trade_date':
                                        # 转换日期格式
                                        daily_data[key] = datetime.strptime(str(value), '%Y%m%d').date()
                                    else:
                                        daily_data[key] = value
                            
                            daily = IndexDaily(**daily_data)
                            db.session.add(daily)
                            logger.debug(f"新增日线行情: {row['ts_code']} - {row['trade_date']}")
                        
                        success_count += 1
                        
                    except Exception as e:
                        logger.error(f"处理日线行情 {row.get('ts_code', 'Unknown')} - {row.get('trade_date', 'Unknown')} 时出错: {e}")
                        continue
                
                # 提交所有更改
                db.session.commit()
                logger.info(f"指数 {ts_code} 日线行情处理完成，成功处理 {success_count} 条数据")
                
            else:
                logger.warning(f"指数 {ts_code} 未获取到日线行情数据")
                
    except Exception as e:
        logger.error(f"初始化指数 {ts_code} 日线行情失败: {e}")
        raise

def init_all_index_daily(start_date=None, end_date=None):
    """初始化所有指数的日线行情数据"""
    try:
        app = create_app()
        
        with app.app_context():
            # 检查表是否存在，如果不存在则创建
            db.create_all()
            
            # 获取所有指数基本信息
            indices = IndexBasic.query.all()
            
            if not indices:
                logger.warning("未找到指数基本信息，请先运行指数基本信息初始化脚本")
                return
            
            logger.info(f"开始初始化 {len(indices)} 个指数的日线行情数据...")
            
            # 如果没有指定日期范围，默认获取最近7天的数据
            if not start_date:
                start_date = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')
            
            success_count = 0
            for index in indices:
                try:
                    logger.info(f"正在处理指数: {index.ts_code} - {index.name}")
                    init_index_daily_by_ts_code(index.ts_code, start_date, end_date)
                    success_count += 1
                except Exception as e:
                    logger.error(f"处理指数 {index.ts_code} 失败: {e}")
                    continue
            
            logger.info(f"所有指数日线行情初始化完成，成功处理 {success_count} 个指数")
            
    except Exception as e:
        logger.error(f"初始化所有指数日线行情失败: {e}")
        raise

def init_index_daily_by_market(market, start_date=None, end_date=None):
    """初始化指定市场指数的日线行情数据"""
    try:
        app = create_app()
        
        with app.app_context():
            # 检查表是否存在，如果不存在则创建
            db.create_all()
            
            # 获取指定市场的指数
            indices = IndexBasic.query.filter_by(market=market).all()
            
            if not indices:
                logger.warning(f"未找到 {market} 市场的指数信息")
                return
            
            logger.info(f"开始初始化 {market} 市场 {len(indices)} 个指数的日线行情数据...")
            
            # 如果没有指定日期范围，默认获取最近7天的数据
            if not start_date:
                start_date = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')
            
            success_count = 0
            for index in indices:
                try:
                    logger.info(f"正在处理指数: {index.ts_code} - {index.name}")
                    init_index_daily_by_ts_code(index.ts_code, start_date, end_date)
                    success_count += 1
                except Exception as e:
                    logger.error(f"处理指数 {index.ts_code} 失败: {e}")
                    continue
            
            logger.info(f"{market} 市场指数日线行情初始化完成，成功处理 {success_count} 个指数")
            
    except Exception as e:
        logger.error(f"初始化 {market} 市场指数日线行情失败: {e}")
        raise

def get_index_daily_data(ts_code, start_date=None, end_date=None):
    """获取指定指数的日线行情数据"""
    try:
        app = create_app()
        
        with app.app_context():
            db.create_all()
            
            ts.set_token('82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
            pro = ts.pro_api()
            
            # 如果没有指定日期范围，默认获取最近30天的数据
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')
            
            logger.info(f"获取指数 {ts_code} 从 {start_date} 到 {end_date} 的日线行情...")
            
            df = pro.index_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            
            if df is not None and not df.empty:
                logger.info(f"获取到 {len(df)} 条 {ts_code} 日线行情数据")
                return df
            else:
                logger.warning(f"指数 {ts_code} 未获取到日线行情数据")
                return None
                
    except Exception as e:
        logger.error(f"获取指数 {ts_code} 日线行情失败: {e}")
        return None

if __name__ == '__main__':
    # 初始化所有指数的日线行情数据（最近7天）
    # init_all_index_daily()
    
    # 初始化指定指数的日线行情数据
    # init_index_daily_by_ts_code('000001.SH', '20240101', '20240131')
    
    # 初始化指定市场指数的日线行情数据
    # init_index_daily_by_market('SSE')
    
    # 获取指定指数的日线行情数据
    # daily_data = get_index_daily_data('000001.SH', '20240101', '20240131')
    # if daily_data is not None:
    #     print(daily_data.head())

    # 000001.SH
    # 399107.SZ
    # 399006.SZ
    logger.info("请根据需要调用相应的函数")
