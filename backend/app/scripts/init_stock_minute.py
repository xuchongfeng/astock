#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
分钟行情数据初始化脚本
使用多线程从Tushare获取数据并保存到数据库
"""

import sys
import os
import tushare as ts
import pandas as pd
from datetime import datetime, date, timedelta
import threading
import concurrent.futures
import queue
import logging
import time
from typing import List, Dict, Any, Optional

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app, db
from app.services.stock_minute_service import stock_minute_service
from app.scripts.config import THREADING_CONFIG, TUSHARE_CONFIG, DB_CONFIG, LOGGING_CONFIG

# 配置日志
logging.basicConfig(
    level=LOGGING_CONFIG['level'],
    format=LOGGING_CONFIG['format'],
    handlers=[
        logging.FileHandler(LOGGING_CONFIG['file']),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 数据库锁
db_lock = threading.Lock()

class StockMinuteInitializer:
    """分钟行情数据初始化器"""
    
    def __init__(self):
        """初始化"""
        self.app = create_app()
        self.pro = ts.pro_api(TUSHARE_CONFIG['token'])
        self.max_workers = THREADING_CONFIG['max_workers']
        self.batch_size = THREADING_CONFIG['batch_size']
        self.retry_times = THREADING_CONFIG['retry_times']
        self.retry_delay = THREADING_CONFIG['retry_delay']
    
    def fetch_minute_data_with_retry(self, ts_code: str, trade_date: str, freq: str = '1min') -> Optional[pd.DataFrame]:
        """
        带重试的分钟数据获取
        :param ts_code: 股票代码
        :param trade_date: 交易日期
        :param freq: 频率 1min/5min/15min/30min/60min
        :return: 数据DataFrame
        """
        for attempt in range(self.retry_times):
            try:
                logger.info(f"获取分钟数据: {ts_code} {trade_date} {freq} (尝试 {attempt + 1}/{self.retry_times})")
                
                # 调用Tushare API
                df = self.pro.stk_mins(
                    ts_code=ts_code,
                    trade_date=trade_date,
                    freq=freq,
                    fields='ts_code,trade_time,open,high,low,close,pre_close,change,pct_chg,vol,amount'
                )
                
                if df is not None and not df.empty:
                    logger.info(f"成功获取分钟数据: {ts_code} {trade_date} {freq}, 记录数: {len(df)}")
                    return df
                else:
                    logger.warning(f"分钟数据为空: {ts_code} {trade_date} {freq}")
                    return None
                    
            except Exception as e:
                logger.error(f"获取分钟数据失败: {ts_code} {trade_date} {freq}, 错误: {str(e)}")
                if attempt < self.retry_times - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"重试次数已用完: {ts_code} {trade_date} {freq}")
                    return None
        
        return None
    
    def process_single_stock_minute(self, ts_code: str, trade_date: str, freq: str = '1min') -> Dict[str, Any]:
        """
        处理单个股票的分钟数据
        :param ts_code: 股票代码
        :param trade_date: 交易日期
        :param freq: 频率
        :return: 处理结果
        """
        try:
            # 获取数据
            df = self.fetch_minute_data_with_retry(ts_code, trade_date, freq)
            
            if df is None or df.empty:
                return {
                    'ts_code': ts_code,
                    'trade_date': trade_date,
                    'freq': freq,
                    'success': False,
                    'error': '数据为空'
                }
            
            # 转换为字典列表
            data_list = []
            for _, row in df.iterrows():
                data = {
                    'ts_code': row['ts_code'],
                    'trade_time': row['trade_time'],
                    'open': row.get('open'),
                    'high': row.get('high'),
                    'low': row.get('low'),
                    'close': row.get('close'),
                    'pre_close': row.get('pre_close'),
                    'change': row.get('change'),
                    'pct_chg': row.get('pct_chg'),
                    'vol': row.get('vol'),
                    'amount': row.get('amount')
                }
                data_list.append(data)
            
            # 保存到数据库
            with self.app.app_context():
                with db_lock:
                    success_count = stock_minute_service.batch_create_or_update(data_list)
                
                return {
                    'ts_code': ts_code,
                    'trade_date': trade_date,
                    'freq': freq,
                    'success': True,
                    'total': len(data_list),
                    'success_count': success_count
                }
                
        except Exception as e:
            logger.error(f"处理分钟数据失败: {ts_code} {trade_date} {freq}, 错误: {str(e)}")
            return {
                'ts_code': ts_code,
                'trade_date': trade_date,
                'freq': freq,
                'success': False,
                'error': str(e)
            }
    
    def process_minutes_batch(self, task_queue: queue.Queue, result_queue: queue.Queue):
        """
        批量处理分钟数据
        :param task_queue: 任务队列
        :param result_queue: 结果队列
        """
        while True:
            try:
                # 获取任务
                task = task_queue.get(timeout=1)
                if task is None:
                    break
                
                ts_code, trade_date, freq = task
                result = self.process_single_stock_minute(ts_code, trade_date, freq)
                result_queue.put(result)
                
                # 标记任务完成
                task_queue.task_done()
                
            except queue.Empty:
                break
            except Exception as e:
                logger.error(f"批量处理失败: {str(e)}")
                result_queue.put({
                    'success': False,
                    'error': str(e)
                })
    
    def process_minutes_with_progress(self, stock_list: List[str], date_list: List[str], 
                                    freq_list: List[str] = None, max_workers: int = None) -> List[Dict[str, Any]]:
        """
        带进度显示的多线程处理
        :param stock_list: 股票代码列表
        :param date_list: 日期列表
        :param freq_list: 频率列表
        :param max_workers: 最大工作线程数
        :return: 处理结果列表
        """
        if max_workers is None:
            max_workers = self.max_workers
        
        if freq_list is None:
            freq_list = ['1min']
        
        # 创建任务队列
        task_queue = queue.Queue()
        result_queue = queue.Queue()
        
        # 添加任务
        total_tasks = 0
        for ts_code in stock_list:
            for trade_date in date_list:
                for freq in freq_list:
                    task_queue.put((ts_code, trade_date, freq))
                    total_tasks += 1
        
        logger.info(f"总任务数: {total_tasks}")
        
        # 启动工作线程
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交工作线程
            futures = []
            for _ in range(max_workers):
                future = executor.submit(self.process_minutes_batch, task_queue, result_queue)
                futures.append(future)
            
            # 等待所有任务完成
            completed_tasks = 0
            results = []
            
            while completed_tasks < total_tasks:
                try:
                    result = result_queue.get(timeout=1)
                    results.append(result)
                    completed_tasks += 1
                    
                    # 显示进度
                    progress = (completed_tasks / total_tasks) * 100
                    logger.info(f"进度: {completed_tasks}/{total_tasks} ({progress:.2f}%)")
                    
                except queue.Empty:
                    continue
            
            # 添加结束标记
            for _ in range(max_workers):
                task_queue.put(None)
            
            # 等待所有线程完成
            concurrent.futures.wait(futures)
        
        return results
    
    def generate_date_list(self, start_date: str, end_date: str) -> List[str]:
        """
        生成日期列表
        :param start_date: 开始日期 (YYYYMMDD)
        :param end_date: 结束日期 (YYYYMMDD)
        :return: 日期列表
        """
        start = datetime.strptime(start_date, '%Y%m%d').date()
        end = datetime.strptime(end_date, '%Y%m%d').date()
        
        date_list = []
        current = start
        while current <= end:
            date_list.append(current.strftime('%Y%m%d'))
            current += timedelta(days=1)
        
        return date_list
    
    def run(self, stock_list: List[str] = None, start_date: str = None, end_date: str = None, 
            freq_list: List[str] = None, max_workers: int = None):
        """
        运行初始化
        :param stock_list: 股票代码列表
        :param start_date: 开始日期 (YYYYMMDD)
        :param end_date: 结束日期 (YYYYMMDD)
        :param freq_list: 频率列表
        :param max_workers: 最大工作线程数
        """
        try:
            logger.info("开始分钟行情数据初始化")
            
            # 设置默认股票列表
            if stock_list is None:
                stock_list = ['000001.SZ', '000002.SZ', '000858.SZ']  # 示例股票
            
            # 设置默认日期范围
            if start_date is None:
                start_date = (date.today() - timedelta(days=7)).strftime('%Y%m%d')
            if end_date is None:
                end_date = date.today().strftime('%Y%m%d')
            
            # 设置默认频率
            if freq_list is None:
                freq_list = ['1min']
            
            logger.info(f"股票列表: {stock_list}")
            logger.info(f"日期范围: {start_date} - {end_date}")
            logger.info(f"频率列表: {freq_list}")
            
            # 生成日期列表
            date_list = self.generate_date_list(start_date, end_date)
            logger.info(f"日期数量: {len(date_list)}")
            
            # 多线程处理
            start_time = time.time()
            results = self.process_minutes_with_progress(stock_list, date_list, freq_list, max_workers)
            end_time = time.time()
            
            # 统计结果
            success_count = sum(1 for r in results if r.get('success', False))
            total_count = len(results)
            
            logger.info(f"处理完成!")
            logger.info(f"总任务数: {total_count}")
            logger.info(f"成功数: {success_count}")
            logger.info(f"失败数: {total_count - success_count}")
            logger.info(f"耗时: {end_time - start_time:.2f}秒")
            
            # 输出详细结果
            for result in results:
                if result.get('success'):
                    logger.info(f"成功: {result['ts_code']} {result['trade_date']} {result['freq']} - {result['success_count']}/{result['total']}")
                else:
                    logger.error(f"失败: {result.get('ts_code', 'N/A')} {result.get('trade_date', 'N/A')} {result.get('freq', 'N/A')} - {result.get('error', 'Unknown error')}")
            
        except Exception as e:
            logger.error(f"初始化失败: {str(e)}")
            raise

def main():
    """主函数"""
    try:
        # 创建初始化器
        initializer = StockMinuteInitializer()
        
        # 运行初始化
        initializer.run()
        
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 