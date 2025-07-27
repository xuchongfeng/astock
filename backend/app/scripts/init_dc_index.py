import tushare as ts
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.dc_index import DcIndex

def fetch_dc_index_data():
    TS_TOKEN = os.getenv('TS_TOKEN', '你的tushare_token')
    ts.set_token(TS_TOKEN)
    pro = ts.pro_api()
    df = pro.dc_index(fields='ts_code,name')
    return df

def save_to_db(df):
    with create_app().app_context():
        total_count = 0
        for _, row in df.iterrows():
            dc_index = DcIndex.query.filter_by(ts_code=row['ts_code']).first()
            if not dc_index:
                dc_index = DcIndex(
                    ts_code=row['ts_code'],
                    name=row['name']
                )
                db.session.add(dc_index)
                total_count += 1
            else:
                dc_index.name = row['name']
        db.session.commit()
        print(f'已同步 {total_count} 条东方财富概念板块数据')

if __name__ == '__main__':
    df = fetch_dc_index_data()
    save_to_db(df) 