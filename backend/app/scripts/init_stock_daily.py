import tushare as ts
import os
import sys
import datetime
import time

# 让脚本可以导入 app 相关模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.stock_company import StockCompany
from app.models.stock_daily import StockDaily

# 设置你的Tushare Token
TS_TOKEN = os.getenv('TS_TOKEN', '82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
ts.set_token(TS_TOKEN)
pro = ts.pro_api()

def fetch_all_ts_codes():
    with create_app().app_context():
        return [c.ts_code for c in StockCompany.query.all()]

def fetch_daily_data(ts_code, start_date=None, end_date=None):
    # Tushare接口默认返回全部历史数据，支持分日期拉取
    try:
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df
    except Exception as e:
        print(f"Error fetching {ts_code}: {e}")
        return None

def save_daily_to_db(df):
    from app import create_app, db
    from app.models.stock_daily import StockDaily
    import datetime
    import pandas as pd

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
            print(f'批量写入 {len(objs)} 条数据')

if __name__ == '__main__':
    import pandas as pd
    ts_codes = fetch_all_ts_codes()
    for i, ts_code in enumerate(ts_codes):
        print(f"[{i+1}/{len(ts_codes)}] Fetching {ts_code} ...")
        today = datetime.datetime.today().strftime('%Y%m%d')
        df = fetch_daily_data(ts_code, start_date=today, end_date=today)
        if df is not None and not df.empty:
            save_daily_to_db(df)
            print(f"  {len(df)} rows saved.")
        else:
            print("  No data.")
    print("All done.")