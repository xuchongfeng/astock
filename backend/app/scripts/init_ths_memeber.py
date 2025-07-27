import tushare as ts
import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.ths_member import ThsMember

def fetch_ths_member_data(ts_code):
    TS_TOKEN = os.getenv('TS_TOKEN', '82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
    ts.set_token(TS_TOKEN)
    pro = ts.pro_api()
    df = pro.ths_member(ts_code=ts_code)
    return df

def save_to_db(df):
    with create_app().app_context():
        count = 0
        for _, row in df.iterrows():
            in_date = None
            out_date = None
            if row.get('in_date'):
                try:
                    in_date = datetime.datetime.strptime(str(row['in_date']), '%Y%m%d').date()
                except Exception:
                    in_date = None
            if row.get('out_date'):
                try:
                    out_date = datetime.datetime.strptime(str(row['out_date']), '%Y%m%d').date()
                except Exception:
                    out_date = None
            member = ThsMember.query.filter_by(ts_code=row['ts_code'], con_code=row['con_code']).first()
            if not member:
                member = ThsMember(
                    ts_code=row['ts_code'],
                    con_code=row['con_code'],
                    con_name=row.get('con_name'),
                    weight=row.get('weight'),
                    in_date=in_date,
                    out_date=out_date,
                    is_new=row.get('is_new')
                )
                db.session.add(member)
                count += 1
            else:
                member.con_name = row.get('con_name')
                member.weight = row.get('weight')
                member.in_date = in_date
                member.out_date = out_date
                member.is_new = row.get('is_new')
        db.session.commit()
        print(f'已同步 {count} 条同花顺概念成分数据')

if __name__ == '__main__':
    # 你可以循环所有ths_index表的ts_code来批量拉取
    from app.models.ths_index import ThsIndex
    with create_app().app_context():
        ts_codes = [i.ts_code for i in ThsIndex.query.all()]
    for ts_code in ts_codes:
        print(f'拉取 {ts_code} ...')
        df = fetch_ths_member_data(ts_code)
        save_to_db(df)