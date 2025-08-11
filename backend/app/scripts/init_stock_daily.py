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
from app.models.stock_daily import StockDaily
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

def get_latest_update_date():
    """获取数据库中最新数据的更新日期"""
    with create_app().app_context():
        latest_record = StockDaily.query.order_by(StockDaily.trade_date.desc()).first()
        if latest_record:
            return latest_record.trade_date
        else:
            # 如果没有数据，返回30天前的日期作为默认值
            return datetime.datetime.now().date() - datetime.timedelta(days=30)

def fetch_daily_data_with_retry(ts_code, start_date=None, end_date=None, max_retries=None):
    """带重试机制的数据获取"""
    if max_retries is None:
        max_retries = TUSHARE_CONFIG['retry_times']
    
    for attempt in range(max_retries + 1):
        try:
            df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            return df
        except Exception as e:
            if attempt < max_retries:
                logger.warning(f"获取 {ts_code} 失败，第 {attempt + 1} 次重试: {e}")
                time.sleep(TUSHARE_CONFIG['retry_delay'])
            else:
                logger.error(f"获取 {ts_code} 最终失败: {e}")
                return None

def save_daily_to_db(df):
    from app import create_app, db
    from app.models.stock_daily import StockDaily
    import datetime
    import pandas as pd

    with db_lock:  # 使用线程锁保护数据库操作
        with create_app().app_context():
            objs = []
            for _, row in df.iterrows():
                trade_date = datetime.datetime.strptime(str(row['trade_date']), '%Y%m%d').date()
                # 只插入数据库中不存在的记录（如需upsert可先查已存在的ts_code+trade_date）
                objs.append(StockDaily(
                    ts_code=row['ts_code'],
                    trade_date=trade_date,
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    pre_close=row['pre_close'],
                    change=row['change'],
                    pct_chg=row['pct_chg'],
                    vol=int(row['vol']) if not pd.isna(row['vol']) else None,
                    amount=float(row['amount']) * 1000 if not pd.isna(row['amount']) else None,
                    turnover_rate=None,
                ))
            if objs:
                db.session.bulk_save_objects(objs)
                db.session.commit()
                logger.info(f'批量写入 {len(objs)} 条数据')
                time.sleep(DB_CONFIG['commit_delay'])  # 提交后稍作延迟

def process_single_stock(ts_code, start_date, end_date):
    """处理单只股票的数据"""
    try:
        # 获取日线数据
        df = fetch_daily_data_with_retry(ts_code, start_date=start_date, end_date=end_date)
        
        if df is not None and not df.empty:
            # 保存到数据库
            save_daily_to_db(df)
            logger.info(f"成功处理 {ts_code}: {len(df)} 条数据")
            return True
        else:
            logger.warning(f"未获取到 {ts_code} 的数据")
            return False
            
    except Exception as e:
        logger.error(f"处理 {ts_code} 时发生异常: {e}")
        return False

def process_stocks_batch(ts_codes, start_date, end_date, max_workers=None):
    """批量处理股票数据"""
    if max_workers is None:
        max_workers = THREADING_CONFIG['max_workers']
    
    logger.info(f"开始处理 {len(ts_codes)} 只股票，使用 {max_workers} 个线程")
    
    success_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_ts_code = {
            executor.submit(process_single_stock, ts_code, start_date, end_date): ts_code 
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
                logger.error(f"处理 {ts_code} 时发生异常: {e}")
                failed_count += 1
    
    logger.info(f"处理完成: 成功 {success_count} 只，失败 {failed_count} 只")
    return success_count, failed_count

def process_stocks_with_progress(ts_codes, start_date, end_date, max_workers=None, batch_size=None):
    """分批处理股票数据，显示进度"""
    if max_workers is None:
        max_workers = THREADING_CONFIG['max_workers']
    if batch_size is None:
        batch_size = THREADING_CONFIG['batch_size']
    
    total_stocks = len(ts_codes)
    processed = 0
    total_success = 0
    total_failed = 0
    
    logger.info(f"总共需要处理 {total_stocks} 只股票")
    
    # 分批处理
    for i in range(0, total_stocks, batch_size):
        batch = ts_codes[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total_stocks + batch_size - 1) // batch_size
        
        logger.info(f"处理第 {batch_num}/{total_batches} 批 ({len(batch)} 只股票)")
        
        success, failed = process_stocks_batch(batch, start_date, end_date, max_workers)
        total_success += success
        total_failed += failed
        processed += len(batch)
        
        logger.info(f"进度: {processed}/{total_stocks} ({processed/total_stocks*100:.1f}%)")
        
        # 批次间稍作休息，避免API限制
        if i + batch_size < total_stocks:
            time.sleep(THREADING_CONFIG['batch_delay'])
    
    logger.info(f"全部完成: 成功 {total_success} 只，失败 {total_failed} 只")
    return total_success, total_failed

def main():
    """主函数"""
    import pandas as pd
    
    # 获取所有股票代码
    ts_codes = fetch_all_ts_codes()
    
    # 获取数据库中最新的更新日期
    latest_date = get_latest_update_date()
    today = datetime.datetime.now().date()
    
    # 如果最新日期是今天，则不需要更新
    if latest_date >= today:
        logger.info(f"数据已是最新，最新更新日期: {latest_date}")
        return 0, 0, 0
    
    # 计算需要更新的日期范围
    start_date = (latest_date + datetime.timedelta(days=1)).strftime('%Y%m%d')
    end_date = today.strftime('%Y%m%d')
    
    logger.info(f"开始获取 {len(ts_codes)} 只股票的日线数据")
    logger.info(f"更新日期范围: {start_date} 到 {end_date}")
    logger.info(f"配置信息: 线程数={THREADING_CONFIG['max_workers']}, "
                f"批次大小={THREADING_CONFIG['batch_size']}, "
                f"重试次数={TUSHARE_CONFIG['retry_times']}")
    
    start_time = time.time()
    
    # 执行多线程处理
    success_count, failed_count = process_stocks_with_progress(
        ts_codes, start_date, end_date,
        THREADING_CONFIG['max_workers'], 
        THREADING_CONFIG['batch_size']
    )
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    logger.info(f"任务完成，耗时: {elapsed_time:.2f} 秒")
    if success_count + failed_count > 0:
        logger.info(f"成功率: {success_count/(success_count+failed_count)*100:.1f}%")
    
    return success_count, failed_count, elapsed_time

if __name__ == '__main__':
    main()