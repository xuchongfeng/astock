import tushare as ts
import os
import sys
import datetime

# 让脚本可以导入 app 相关模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.ths_index import ThsIndex

def fetch_ths_index_data():
    TS_TOKEN = os.getenv('TS_TOKEN', '82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
    ts.set_token(TS_TOKEN)
    pro = ts.pro_api()
    df = pro.ths_index()
    return df

def safe_int(val, default=None):
    try:
        if val is None:
            return default
        return int(val)
    except Exception:
        return default

def save_to_db(df):
    with create_app().app_context():
        total_count = 0
        for _, row in df.iterrows():
            # 处理日期
            list_date = None
            if row.get('list_date'):
                try:
                    list_date = datetime.datetime.strptime(str(row['list_date']), '%Y%m%d').date()
                except Exception:
                    list_date = None
            count = safe_int(row.get('count'))
            ths_index = ThsIndex.query.filter_by(ts_code=row['ts_code']).first()
            if not ths_index:
                ths_index = ThsIndex(
                    ts_code=row['ts_code'],
                    name=row['name'],
                    count=count,
                    exchange=row.get('exchange'),
                    list_date=list_date,
                    type=row.get('type')
                )
                db.session.add(ths_index)
                total_count += 1
            else:
                ths_index.name = row['name']
                ths_index.count = count
                ths_index.exchange = row.get('exchange')
                ths_index.list_date = list_date
                ths_index.type = row.get('type')
        db.session.commit()
        print(f'已同步 {total_count} 条同花顺行业概念板块数据')

if __name__ == '__main__':
    df = fetch_ths_index_data()
    save_to_db(df) 