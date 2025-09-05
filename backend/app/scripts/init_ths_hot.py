#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同花顺热榜数据初始化脚本
参考文档: https://tushare.pro/document/2?doc_id=320
"""

import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
import time
import logging
from app import create_app, db
from app.models.ths_hot import ThsHot

ts.set_token('82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
pro = ts.pro_api()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('init_ths_hot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置Tushare
# ts.set_token('your_tushare_token')  # 请替换为你的token
# pro = ts.pro_api()

def safe_float(value):
    """安全转换为浮点数"""
    if pd.isna(value) or value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def safe_int(value):
    """安全转换为整数"""
    if pd.isna(value) or value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def safe_str(value):
    """安全转换为字符串"""
    if pd.isna(value) or value is None:
        return None
    return str(value).strip()

def fetch_ths_hot_data(trade_date, market_type='热股'):
    """
    获取同花顺热榜数据
    
    Args:
        trade_date: 交易日期，格式：YYYYMMDD
        market_type: 热榜类型，如：热股、ETF、可转债、行业板块、概念板块等
    
    Returns:
        DataFrame: 热榜数据
    """
    try:
        logger.info(f"正在获取 {trade_date} {market_type} 热榜数据...")
        
        # 调用Tushare API
        df = pro.ths_hot(
            trade_date=trade_date,
            market=market_type,
            fields='trade_date,data_type,ts_code,ts_name,rank,pct_change,current_price,concept,rank_reason,hot,rank_time'
        )
        
        if df is None or df.empty:
            logger.warning(f"{trade_date} {market_type} 无数据")
            return None
        
        logger.info(f"成功获取 {len(df)} 条 {market_type} 数据")
        return df
        
    except Exception as e:
        logger.error(f"获取 {trade_date} {market_type} 数据失败: {str(e)}")
        return None

def process_ths_hot_data(df, market_type):
    """
    处理热榜数据
    
    Args:
        df: Tushare返回的DataFrame
        market_type: 热榜类型
    
    Returns:
        list: 处理后的数据列表
    """
    if df is None or df.empty:
        return []
    
    processed_data = []
    
    for _, row in df.iterrows():
        try:
            # 处理数据
            hot_data = {
                'trade_date': datetime.strptime(str(row['trade_date']), '%Y%m%d').date(),
                'data_type': market_type,
                'ts_code': safe_str(row['ts_code']),
                'ts_name': safe_str(row['ts_name']),
                'rank': safe_int(row['rank']),
                'pct_change': safe_float(row['pct_change']),
                'current_price': safe_float(row['current_price']),
                'concept': safe_str(row['concept']),
                'rank_reason': safe_str(row['rank_reason']),
                'hot': safe_float(row['hot']),
                'rank_time': safe_str(row['rank_time'])
            }
            
            # 验证必填字段
            if hot_data['ts_code'] and hot_data['ts_name'] and hot_data['rank'] is not None:
                processed_data.append(hot_data)
            
        except Exception as e:
            logger.error(f"处理数据行失败: {row}, 错误: {str(e)}")
            continue
    
    return processed_data

def save_ths_hot_data(hot_data_list):
    """
    保存热榜数据到数据库
    
    Args:
        hot_data_list: 热榜数据列表
    
    Returns:
        int: 成功保存的记录数
    """
    if not hot_data_list:
        return 0
    
    try:
        # 使用upsert逻辑保存数据
        from app.services.ths_hot_service import upsert_hot_data
        success = upsert_hot_data(hot_data_list)
        
        if success:
            logger.info(f"成功保存 {len(hot_data_list)} 条热榜数据")
            return len(hot_data_list)
        else:
            logger.error("保存数据失败")
            return 0
            
    except Exception as e:
        logger.error(f"保存数据失败: {str(e)}")
        return 0

def get_market_types():
    """获取支持的热榜类型"""
    return [
        '热股',
        'ETF', 
        '可转债',
        '行业板块',
        '概念板块',
        '期货',
        '港股',
        '热基',
        '美股'
    ]

def get_trading_dates(start_date, end_date):
    """
    获取交易日期列表
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        list: 交易日期列表
    """
    dates = []
    current_date = start_date
    
    while current_date <= end_date:
        # 跳过周末（简单处理，实际应该使用交易日历）
        if current_date.weekday() < 8:  # 0-4 表示周一到周五
            dates.append(current_date.strftime('%Y%m%d'))
        current_date += timedelta(days=1)
    
    return dates

def init_ths_hot_data(start_date=None, end_date=None, market_types=None):
    """
    初始化热榜数据
    
    Args:
        start_date: 开始日期，格式：YYYY-MM-DD
        end_date: 结束日期，格式：YYYY-MM-DD
        market_types: 热榜类型列表，如果为None则获取所有类型
    """
    try:
        # 设置默认日期范围（最近7天）
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # 设置默认热榜类型
        if not market_types:
            market_types = get_market_types()
        
        logger.info(f"开始初始化热榜数据，日期范围: {start_date} 到 {end_date}")
        logger.info(f"热榜类型: {', '.join(market_types)}")
        
        # 转换日期格式
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        # 获取交易日期列表
        trading_dates = get_trading_dates(start_dt, end_dt)
        logger.info(f"共 {len(trading_dates)} 个交易日")
        
        total_saved = 0
        
        # 遍历每个交易日
        for trade_date in trading_dates:
            logger.info(f"处理交易日: {trade_date}")
            
            # 遍历每个热榜类型
            for market_type in market_types:
                try:
                    # 获取数据
                    df = fetch_ths_hot_data(trade_date, market_type)
                    
                    if df is not None and not df.empty:
                        # 处理数据
                        processed_data = process_ths_hot_data(df, market_type)
                        
                        if processed_data:
                            # 保存数据
                            saved_count = save_ths_hot_data(processed_data)
                            total_saved += saved_count
                        
                        # 添加延迟避免API限制
                        time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"处理 {trade_date} {market_type} 失败: {str(e)}")
                    continue
        
        logger.info(f"热榜数据初始化完成，共保存 {total_saved} 条记录")
        
    except Exception as e:
        logger.error(f"初始化热榜数据失败: {str(e)}")
        raise

def main():
    """主函数"""
    try:
        # 创建Flask应用上下文
        app = create_app()
        with app.app_context():
            logger.info("开始初始化同花顺热榜数据...")
            
            # 初始化数据（最近7天）
            init_ths_hot_data()
            
            logger.info("同花顺热榜数据初始化完成！")
            
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        raise

if __name__ == '__main__':
    # 注意：运行前请确保已设置Tushare token
    # 可以通过环境变量设置：export TUSHARE_TOKEN=your_token
    # 或者在代码中设置：ts.set_token('your_token')
    
    main() 