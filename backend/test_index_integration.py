#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
指数功能集成测试脚本
测试指数基本信息、日线行情、服务层和API层的功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.index_basic import IndexBasic
from app.models.index_daily import IndexDaily
from app.services.index_basic_service import IndexBasicService
from app.services.index_daily_service import IndexDailyService
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_index_basic_model():
    """测试指数基本信息模型"""
    logger.info("开始测试指数基本信息模型...")
    
    try:
        app = create_app()
        
        with app.app_context():
            # 创建表
            db.create_all()
            
            # 测试数据
            test_data = {
                'ts_code': '000001.SH',
                'name': '上证指数',
                'fullname': '上证综合指数',
                'market': 'SSE',
                'publisher': 'SSE',
                'index_type': '综合指数',
                'category': '综合指数',
                'base_date': '19901219',
                'base_point': 100.0,
                'list_date': '19901219',
                'weight_rule': '市值加权',
                'desc': '上证综合指数是以上海证券交易所上市的所有股票为样本编制的综合指数'
            }
            
            # 创建测试记录
            index = IndexBasic(**test_data)
            db.session.add(index)
            db.session.commit()
            
            # 查询测试
            queried_index = IndexBasic.query.filter_by(ts_code='000001.SH').first()
            assert queried_index is not None
            assert queried_index.name == '上证指数'
            assert queried_index.market == 'SSE'
            
            # 测试as_dict方法
            index_dict = queried_index.as_dict()
            assert 'ts_code' in index_dict
            assert 'name' in index_dict
            assert 'market' in index_dict
            
            logger.info("✅ 指数基本信息模型测试通过")
            
            # 清理测试数据
            db.session.delete(queried_index)
            db.session.commit()
            
    except Exception as e:
        logger.error(f"❌ 指数基本信息模型测试失败: {e}")
        raise

def test_index_daily_model():
    """测试指数日线行情模型"""
    logger.info("开始测试指数日线行情模型...")
    
    try:
        app = create_app()
        
        with app.app_context():
            # 创建表
            db.create_all()
            
            # 测试数据
            test_data = {
                'ts_code': '000001.SH',
                'trade_date': datetime.now().date(),
                'close': 3000.0,
                'open': 2990.0,
                'high': 3010.0,
                'low': 2980.0,
                'pre_close': 2985.0,
                'change': 15.0,
                'pct_chg': 0.5,
                'vol': 1000000.0,
                'amount': 3000000000.0
            }
            
            # 创建测试记录
            daily = IndexDaily(**test_data)
            db.session.add(daily)
            db.session.commit()
            
            # 查询测试
            queried_daily = IndexDaily.query.filter_by(
                ts_code='000001.SH',
                trade_date=datetime.now().date()
            ).first()
            
            assert queried_daily is not None
            assert float(queried_daily.close) == 3000.0
            assert float(queried_daily.open) == 2990.0
            
            # 测试as_dict方法
            daily_dict = queried_daily.as_dict()
            assert 'ts_code' in daily_dict
            assert 'trade_date' in daily_dict
            assert 'close' in daily_dict
            
            logger.info("✅ 指数日线行情模型测试通过")
            
            # 清理测试数据
            db.session.delete(queried_daily)
            db.session.commit()
            
    except Exception as e:
        logger.error(f"❌ 指数日线行情模型测试失败: {e}")
        raise

def test_index_basic_service():
    """测试指数基本信息服务"""
    logger.info("开始测试指数基本信息服务...")
    
    try:
        app = create_app()
        
        with app.app_context():
            # 创建表
            db.create_all()
            
            # 测试数据
            test_data = {
                'ts_code': '000002.SH',
                'name': '上证A股',
                'fullname': '上证A股指数',
                'market': 'SSE',
                'publisher': 'SSE',
                'index_type': '成分指数',
                'category': '成分指数'
            }
            
            # 测试创建
            created_index = IndexBasicService.create_index_basic(test_data)
            assert created_index is not None
            assert created_index['ts_code'] == '000002.SH'
            
            # 测试查询
            queried_index = IndexBasicService.get_index_basic_by_ts_code('000002.SH')
            assert queried_index is not None
            assert queried_index['name'] == '上证A股'
            
            # 测试按市场查询
            sse_indices = IndexBasicService.get_index_basic_by_market('SSE')
            assert len(sse_indices) > 0
            
            # 测试搜索
            search_results = IndexBasicService.search_index_basic('上证')
            assert len(search_results) > 0
            
            # 测试更新
            update_data = {'name': '上证A股指数'}
            updated_index = IndexBasicService.update_index_basic('000002.SH', update_data)
            assert updated_index is not None
            assert updated_index['name'] == '上证A股指数'
            
            # 测试删除
            success = IndexBasicService.delete_index_basic('000002.SH')
            assert success is True
            
            logger.info("✅ 指数基本信息服务测试通过")
            
    except Exception as e:
        logger.error(f"❌ 指数基本信息服务测试失败: {e}")
        raise

def test_index_daily_service():
    """测试指数日线行情服务"""
    logger.info("开始测试指数日线行情服务...")
    
    try:
        app = create_app()
        
        with app.app_context():
            # 创建表
            db.create_all()
            
            # 测试数据
            test_data = {
                'ts_code': '000003.SH',
                'trade_date': datetime.now().date(),
                'close': 2500.0,
                'open': 2490.0,
                'high': 2510.0,
                'low': 2480.0,
                'pre_close': 2485.0,
                'change': 15.0,
                'pct_chg': 0.6,
                'vol': 800000.0,
                'amount': 2000000000.0
            }
            
            # 测试创建
            created_daily = IndexDailyService.create_index_daily(test_data)
            assert created_daily is not None
            assert created_daily['ts_code'] == '000003.SH'
            
            # 测试查询
            queried_daily = IndexDailyService.get_index_daily_by_ts_code('000003.SH')
            assert len(queried_daily) > 0
            
            # 测试按日期范围查询
            start_date = datetime.now().date() - timedelta(days=1)
            end_date = datetime.now().date()
            range_data = IndexDailyService.get_index_daily_by_date_range('000003.SH', start_date, end_date)
            assert len(range_data) > 0
            
            # 测试获取最新数据
            latest_data = IndexDailyService.get_latest_index_daily('000003.SH')
            assert latest_data is not None
            
            # 测试获取统计信息
            stats = IndexDailyService.get_index_daily_statistics('000003.SH', 1)
            assert stats is not None
            assert 'ts_code' in stats
            
            # 测试批量创建
            batch_data = [
                {
                    'ts_code': '000004.SH',
                    'trade_date': datetime.now().date(),
                    'close': 2000.0,
                    'open': 1990.0,
                    'high': 2010.0,
                    'low': 1980.0,
                    'pre_close': 1985.0,
                    'change': 15.0,
                    'pct_chg': 0.75,
                    'vol': 600000.0,
                    'amount': 1200000000.0
                }
            ]
            
            success = IndexDailyService.batch_create_index_daily(batch_data)
            assert success is True
            
            # 测试更新
            update_data = {'close': 2005.0}
            updated_daily = IndexDailyService.update_index_daily('000004.SH', datetime.now().date(), update_data)
            assert updated_daily is not None
            assert float(updated_daily['close']) == 2005.0
            
            # 测试删除
            success = IndexDailyService.delete_index_daily('000003.SH', datetime.now().date())
            assert success is True
            
            success = IndexDailyService.delete_index_daily('000004.SH', datetime.now().date())
            assert success is True
            
            logger.info("✅ 指数日线行情服务测试通过")
            
    except Exception as e:
        logger.error(f"❌ 指数日线行情服务测试失败: {e}")
        raise

def test_database_operations():
    """测试数据库操作"""
    logger.info("开始测试数据库操作...")
    
    try:
        app = create_app()
        
        with app.app_context():
            # 创建表
            db.create_all()
            
            # 检查表是否存在
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            assert 'index_basic' in tables
            assert 'index_daily' in tables
            
            logger.info(f"数据库表检查通过，现有表: {tables}")
            
            # 测试索引
            index_basic_indexes = inspector.get_indexes('index_basic')
            index_daily_indexes = inspector.get_indexes('index_daily')
            
            logger.info(f"index_basic表索引: {index_basic_indexes}")
            logger.info(f"index_daily表索引: {index_daily_indexes}")
            
            logger.info("✅ 数据库操作测试通过")
            
    except Exception as e:
        logger.error(f"❌ 数据库操作测试失败: {e}")
        raise

def main():
    """主测试函数"""
    logger.info("🚀 开始执行指数功能集成测试")
    
    test_functions = [
        test_database_operations,
        test_index_basic_model,
        test_index_daily_model,
        test_index_basic_service,
        test_index_daily_service
    ]
    
    success_count = 0
    total_count = len(test_functions)
    
    for i, test_func in enumerate(test_functions, 1):
        logger.info(f"\n📋 测试进度: {i}/{total_count}")
        try:
            test_func()
            success_count += 1
        except Exception as e:
            logger.error(f"测试 {test_func.__name__} 失败: {e}")
    
    # 输出测试结果
    logger.info(f"\n{'='*60}")
    logger.info("🏁 指数功能集成测试完成")
    logger.info(f"{'='*60}")
    logger.info(f"总测试数: {total_count}")
    logger.info(f"成功测试: {success_count}")
    logger.info(f"失败数量: {total_count - success_count}")
    
    if success_count == total_count:
        logger.info("\n🎉 所有测试通过！")
    else:
        logger.info(f"\n⚠️  有 {total_count - success_count} 个测试失败")
    
    logger.info(f"\n{'='*60}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  用户中断了测试过程")
    except Exception as e:
        logger.error(f"\n❌ 测试过程中发生错误: {e}")
