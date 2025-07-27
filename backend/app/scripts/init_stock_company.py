import tushare as ts
import os
import sys
import datetime

# 让脚本可以导入 app 相关模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.stock_company import StockCompany

# 设置你的Tushare Token
TS_TOKEN = os.getenv('TS_TOKEN', '82184947ad890848c5873e738c856ecff5d31d649d9d443c34b6f5b4')
ts.set_token(TS_TOKEN)
pro = ts.pro_api()

def fetch_stock_company_data():
    # 只取常用字段，按需可扩展
    fields = 'ts_code,symbol,name,area,industry,fullname,enname,market,exchange,list_date'
    df = pro.stock_basic(exchange='', list_status='L', fields=fields)
    return df

def save_to_db(df):
    with create_app().app_context():
        for _, row in df.iterrows():
            now = datetime.datetime.now()
            company = StockCompany(
                ts_code=row['ts_code'],
                symbol=row['symbol'],
                name=row['name'],
                area=row.get('area'),
                industry=row.get('industry'),
                fullname=row.get('fullname'),
                enname=row.get('enname'),
                market=row.get('market'),
                exchange=row.get('exchange'),
                list_date=row.get('list_date') if row.get('list_date') else None,
                created_at=now,
                updated_at=now
            )
            # 避免重复插入
            exists = StockCompany.query.filter_by(ts_code=company.ts_code).first()
            if not exists:
                db.session.add(company)
        db.session.commit()
        print(f'已导入 {len(df)} 条公司数据')

if __name__ == '__main__':
    df = fetch_stock_company_data()
    save_to_db(df)
