import tushare as ts
import os
import sys
import datetime
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import logging
import pandas as pd

# 让脚本可以导入 app 相关模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.stock_company import StockCompany
from app.models.stock_daily_basic import StockDailyBasic
from app.scripts.config import THREADING_CONFIG, TUSHARE_CONFIG, DB_CONFIG, LOGGING_CONFIG

# 设置日志
log_config = LOGGING_CONFIG
if log_config['file']:
    logging.basicConfig(
        level=getattr(logging, log_config['level']),
        format=log_config['format'],
        handlers=[
            logging.FileHandler(log_config['file']),
            logging.StreamHandler()
        ]
    )
else:
    logging.basicConfig(
        level=getattr(logging, log_config['level']),
        format=log_config['format']
    )

logger = logging.getLogger(__name__)

# 设置你的Tushare Token
TS_TOKEN = os.getenv('TS_TOKEN', '82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
ts.set_token(TS_TOKEN)
pro = ts.pro_api()

# 线程锁，用于数据库操作
db_lock = threading.Lock()

def fetch_all_ts_codes():
    with create_app().app_context():
        return [c.ts_code for c in StockCompany.query.all()]

def fetch_daily_basic_with_retry(ts_code, trade_date=None, max_retries=None):
    """带重试机制的每日指标数据获取"""
    if max_retries is None:
        max_retries = TUSHARE_CONFIG['retry_times']
    
    for attempt in range(max_retries + 1):
        try:
            if trade_date:
                df = pro.daily_basic(ts_code=ts_code, trade_date=trade_date)
            else:
                df = pro.daily_basic(ts_code=ts_code)
            return df
        except Exception as e:
            if attempt < max_retries:
                logger.warning(f"获取 {ts_code} 每日指标失败，第 {attempt + 1} 次重试: {e}")
                time.sleep(TUSHARE_CONFIG['retry_delay'])
            else:
                logger.error(f"获取 {ts_code} 每日指标最终失败: {e}")
                return None

def save_daily_basic_to_db(df):
    from app import create_app, db
    from app.models.stock_daily_basic import StockDailyBasic
    import datetime
    import pandas as pd

    with db_lock:  # 使用线程锁保护数据库操作
        with create_app().app_context():
            objs = []
            for _, row in df.iterrows():
                trade_date = datetime.datetime.strptime(str(row['trade_date']), '%Y%m%d').date()
                
                # 处理数值字段，避免NaN值
                def safe_float(value):
                    if pd.isna(value):
                        return None
                    try:
                        return float(value)
                    except (ValueError, TypeError):
                        return None
                
                objs.append(StockDailyBasic(
                    ts_code=row['ts_code'],
                    trade_date=trade_date,
                    close=safe_float(row.get('close')),
                    turnover_rate=safe_float(row.get('turnover_rate')),
                    turnover_rate_f=safe_float(row.get('turnover_rate_f')),
                    volume_ratio=safe_float(row.get('volume_ratio')),
                    pe=safe_float(row.get('pe')),
                    pe_ttm=safe_float(row.get('pe_ttm')),
                    pb=safe_float(row.get('pb')),
                    ps=safe_float(row.get('ps')),
                    ps_ttm=safe_float(row.get('ps_ttm')),
                    dv_ratio=safe_float(row.get('dv_ratio')),
                    dv_ttm=safe_float(row.get('dv_ttm')),
                    total_share=safe_float(row.get('total_share')),
                    float_share=safe_float(row.get('float_share')),
                    free_share=safe_float(row.get('free_share')),
                    total_mv=safe_float(row.get('total_mv')),
                    circ_mv=safe_float(row.get('circ_mv')),
                ))
            if objs:
                db.session.bulk_save_objects(objs)
                db.session.commit()
                logger.info(f'批量写入 {len(objs)} 条每日指标数据')
                time.sleep(DB_CONFIG['commit_delay'])  # 提交后稍作延迟

def process_single_stock_basic(ts_code, trade_date=None):
    """处理单个股票的每日指标数据获取和保存"""
    try:
        logger.info(f"Fetching daily basic for {ts_code} ...")
        df = fetch_daily_basic_with_retry(ts_code, trade_date)
        if df is not None and not df.empty:
            save_daily_basic_to_db(df)
            logger.info(f"  {len(df)} rows saved for {ts_code}.")
            return True
        else:
            logger.info(f"  No daily basic data for {ts_code}.")
            return False
    except Exception as e:
        logger.error(f"Error processing daily basic for {ts_code}: {e}")
        return False

def process_stocks_basic_batch(ts_codes, trade_date=None, max_workers=None):
    """批量处理股票每日指标数据"""
    if max_workers is None:
        max_workers = THREADING_CONFIG['max_workers']
    
    logger.info(f"开始处理 {len(ts_codes)} 只股票的每日指标数据，使用 {max_workers} 个线程")
    
    success_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_ts_code = {
            executor.submit(process_single_stock_basic, ts_code, trade_date): ts_code 
            for ts_code in ts_codes
        }
        
        # 处理完成的任务
        for future in as_completed(future_to_ts_code):
            ts_code = future_to_ts_code[future]
            try:
                result = future.result()
                if result:
                    success_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                logger.error(f"处理 {ts_code} 每日指标时发生异常: {e}")
                failed_count += 1
    
    logger.info(f"处理完成: 成功 {success_count} 只，失败 {failed_count} 只")
    return success_count, failed_count

def process_stocks_basic_with_progress(ts_codes, trade_date=None, max_workers=None, batch_size=None):
    """分批处理股票每日指标数据，显示进度"""
    if max_workers is None:
        max_workers = THREADING_CONFIG['max_workers']
    if batch_size is None:
        batch_size = THREADING_CONFIG['batch_size']
    
    total_stocks = len(ts_codes)
    processed = 0
    total_success = 0
    total_failed = 0
    
    logger.info(f"总共需要处理 {total_stocks} 只股票的每日指标数据")
    if trade_date:
        logger.info(f"目标日期: {trade_date}")
    
    # 分批处理
    for i in range(0, total_stocks, batch_size):
        batch = ts_codes[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total_stocks + batch_size - 1) // batch_size
        
        logger.info(f"处理第 {batch_num}/{total_batches} 批 ({len(batch)} 只股票)")
        
        success, failed = process_stocks_basic_batch(batch, trade_date, max_workers)
        total_success += success
        total_failed += failed
        processed += len(batch)
        
        logger.info(f"进度: {processed}/{total_stocks} ({processed/total_stocks*100:.1f}%)")
        
        # 批次间稍作休息，避免API限制
        if i + batch_size < total_stocks:
            time.sleep(THREADING_CONFIG['batch_delay'])
    
    logger.info(f"全部完成: 成功 {total_success} 只，失败 {total_failed} 只")
    return total_success, total_failed

def fetch_all_daily_basic_by_date(trade_date):
    """获取指定日期的所有股票每日指标数据"""
    try:
        logger.info(f"获取 {trade_date} 的所有股票每日指标数据")
        df = pro.daily_basic(trade_date=trade_date)
        if df is not None and not df.empty:
            save_daily_basic_to_db(df)
            logger.info(f"成功保存 {len(df)} 条每日指标数据")
            return len(df)
        else:
            logger.info(f"未找到 {trade_date} 的每日指标数据")
            return 0
    except Exception as e:
        logger.error(f"获取 {trade_date} 每日指标数据失败: {e}")
        return 0

def main():
    """主函数"""
    import pandas as pd
    
    # 获取所有股票代码
    ts_codes = fetch_all_ts_codes()
    today = datetime.datetime.today().strftime('%Y%m%d')
    
    logger.info(f"开始获取 {len(ts_codes)} 只股票的每日指标数据")
    logger.info(f"目标日期: {today}")
    logger.info(f"配置信息: 线程数={THREADING_CONFIG['max_workers']}, "
                f"批次大小={THREADING_CONFIG['batch_size']}, "
                f"重试次数={TUSHARE_CONFIG['retry_times']}")
    
    start_time = time.time()
    
    # 执行多线程处理
    success_count, failed_count = process_stocks_basic_with_progress(
        ts_codes, today, 
        THREADING_CONFIG['max_workers'], 
        THREADING_CONFIG['batch_size']
    )
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    logger.info(f"任务完成，耗时: {elapsed_time:.2f} 秒")
    if success_count + failed_count > 0:
        logger.info(f"成功率: {success_count/(success_count+failed_count)*100:.1f}%")
    
    return success_count, failed_count, elapsed_time

def fetch_by_date_main():
    """按日期获取所有股票每日指标数据的主函数"""
    today = datetime.datetime.today().strftime('%Y%m%d')
    
    logger.info(f"开始获取 {today} 的所有股票每日指标数据")
    
    start_time = time.time()
    
    # 直接获取指定日期的所有数据
    count = fetch_all_daily_basic_by_date(today)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    logger.info(f"任务完成，耗时: {elapsed_time:.2f} 秒")
    logger.info(f"成功获取 {count} 条数据")
    
    return count, elapsed_time

if __name__ == '__main__':
    # 可以选择两种模式：
    # 1. 逐个股票获取（适合历史数据）
    # main()
    
    # 2. 按日期获取所有股票（适合当日数据，推荐）
    fetch_by_date_main() 