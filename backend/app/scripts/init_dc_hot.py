#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
东方财富热榜数据初始化脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.dc_hot import DcHot
from app.services.dc_hot_service import DcHotService
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_dc_hot_table():
    """初始化东方财富热榜表"""
    try:
        app = create_app()
        with app.app_context():
            # 创建表
            DcHot.__table__.create(db.bind, checkfirst=True)
            logger.info("东方财富热榜表创建成功")
            
            # 检查是否已有数据
            existing_count = db.query(DcHot).count()
            if existing_count > 0:
                logger.info(f"表中已有 {existing_count} 条数据，跳过初始化")
                return
            
            # 插入示例数据
            sample_data = [
                {
                    'trade_date': '20250101',
                    'data_type': '热榜',
                    'ts_code': '000001.SZ',
                    'ts_name': '平安银行',
                    'rank': 1,
                    'pct_change': 5.23,
                    'current_price': 12.34,
                    'rank_time': '09:30:00',
                    'market': 'A股市场',
                    'hot_type': '人气榜',
                    'is_new': 'Y'
                },
                {
                    'trade_date': '20250101',
                    'data_type': '热榜',
                    'ts_code': '000002.SZ',
                    'ts_name': '万科A',
                    'rank': 2,
                    'pct_change': 3.45,
                    'current_price': 18.56,
                    'rank_time': '09:30:00',
                    'market': 'A股市场',
                    'hot_type': '人气榜',
                    'is_new': 'Y'
                },
                {
                    'trade_date': '20250101',
                    'data_type': '热榜',
                    'ts_code': '600000.SH',
                    'ts_name': '浦发银行',
                    'rank': 3,
                    'pct_change': 2.78,
                    'current_price': 8.92,
                    'rank_time': '09:30:00',
                    'market': 'A股市场',
                    'hot_type': '人气榜',
                    'is_new': 'Y'
                },
                {
                    'trade_date': '20250101',
                    'data_type': '热榜',
                    'ts_code': '600036.SH',
                    'ts_name': '招商银行',
                    'rank': 4,
                    'pct_change': 4.12,
                    'current_price': 45.67,
                    'rank_time': '09:30:00',
                    'market': 'A股市场',
                    'hot_type': '人气榜',
                    'is_new': 'Y'
                },
                {
                    'trade_date': '20250101',
                    'data_type': '热榜',
                    'ts_code': '000858.SZ',
                    'ts_name': '五粮液',
                    'rank': 5,
                    'pct_change': 1.89,
                    'current_price': 156.78,
                    'rank_time': '09:30:00',
                    'market': 'A股市场',
                    'hot_type': '人气榜',
                    'is_new': 'Y'
                }
            ]
            
            # 批量插入数据
            for data in sample_data:
                dc_hot = DcHot(**data)
                db.session.add(dc_hot)
            
            db.session.commit()
            logger.info(f"成功插入 {len(sample_data)} 条示例数据")
            
    except Exception as e:
        logger.error(f"初始化东方财富热榜表失败: {str(e)}")
        raise e

def main():
    """主函数"""
    try:
        logger.info("开始初始化东方财富热榜数据...")
        init_dc_hot_table()
        logger.info("东方财富热榜数据初始化完成！")
    except Exception as e:
        logger.error(f"初始化失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
