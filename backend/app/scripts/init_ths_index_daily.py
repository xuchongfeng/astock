import tushare as ts
import pandas as pd
from app import create_app, db
from app.models.ths_index import ThsIndex
from app.models.ths_index_daily import ThsIndexDaily
import datetime
import time

# 配置 tushare token
ts.set_token('82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
pro = ts.pro_api()

def parse_date(s):
    return datetime.datetime.strptime(str(s), '%Y%m%d').date()

def init_all_ths_index_daily(start_date, end_date, batch_size=1000):
    """
    初始化所有同花顺板块指数行情表
    :param start_date: 开始日期，格式 '20220101'
    :param end_date: 结束日期，格式 '20221231'
    :param batch_size: 每批写入数据库的行数
    """
    app = create_app()
    with app.app_context():
        all_indexes = ThsIndex.query.all()
        print(f"共{len(all_indexes)}个板块，将依次拉取并初始化行情数据。")
        for idx, index in enumerate(all_indexes):
            ts_code = index.ts_code
            print(f"[{idx+1}/{len(all_indexes)}] 拉取 {ts_code} {index.name} 板块数据 {start_date} ~ {end_date}")
            try:
                df = pro.ths_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            except Exception as e:
                print(f"tushare 拉取失败: {e}")
                continue

            if df.empty:
                print("无数据")
                continue

            df = df.drop_duplicates(subset=['ts_code', 'trade_date'])

            records = []
            for _, row in df.iterrows():
                try:
                    # 先查重，存在则跳过
                    exists = ThsIndexDaily.query.filter_by(ts_code=row['ts_code'], trade_date=parse_date(row['trade_date'])).first()
                    if exists:
                        continue
                    record = ThsIndexDaily(
                        ts_code=row['ts_code'],
                        trade_date=parse_date(row['trade_date']),
                        close=row.get('close'),
                        open=row.get('open'),
                        high=row.get('high'),
                        low=row.get('low'),
                        pre_close=row.get('pre_close'),
                        avg_price=row.get('avg_price'),
                        change=row.get('change'),
                        pct_change=row.get('pct_change'),
                        vol=row.get('vol') if not pd.isna(row.get('vol')) else None,
                        turnover_rate=row.get('turnover_rate') if not pd.isna(row.get('turnover_rate')) else None,
                        total_mv=row.get('total_mv'),
                        float_mv=row.get('float_mv')
                    )
                    records.append(record)
                except Exception as e:
                    print(f"行解析失败: {e}, 行数据: {row.to_dict()}")

            for i in range(0, len(records), batch_size):
                batch = records[i:i+batch_size]
                for rec in batch:
                    exists = ThsIndexDaily.query.filter_by(ts_code=rec.ts_code, trade_date=rec.trade_date).first()
                    if not exists:
                        db.session.add(rec)
                try:
                    db.session.commit()
                    print(f"已写入 {i+len(batch)}/{len(records)} 条")
                except Exception as e:
                    db.session.rollback()
                    print(f"数据库写入失败: {e}")
                time.sleep(0.1)  # 防止数据库压力过大

        print("全部板块初始化完成")

# 示例用法
if __name__ == '__main__':
    # 获取今天日期，格式为YYYYMMDD
    today = datetime.datetime.today().strftime('%Y%m%d')
    init_all_ths_index_daily(today, today)