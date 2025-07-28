from app.models.stock_daily import StockDaily
from app import db
from datetime import timedelta

def get_all_daily(filters=None, query_only=False):
    query = StockDaily.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(StockDaily, attr) == value)
    if query_only:
        return query
    return query.all()

def get_daily_by_id(daily_id):
    return StockDaily.query.get(daily_id)

def create_daily(data):
    daily = StockDaily(**data)
    db.session.add(daily)
    db.session.commit()
    return daily

def update_daily(daily_id, data):
    daily = StockDaily.query.get(daily_id)
    if not daily:
        return None
    for key, value in data.items():
        setattr(daily, key, value)
    db.session.commit()
    return daily

def delete_daily(daily_id):
    daily = StockDaily.query.get(daily_id)
    if not daily:
        return False
    db.session.delete(daily)
    db.session.commit()
    return True

def get_close_price_n_days_ago(ts_code, trade_date, n):
    """获取指定股票在trade_date往前推n日的收盘价"""
    prev_date = trade_date - timedelta(days=n)
    daily = StockDaily.query.filter(StockDaily.ts_code == ts_code, StockDaily.trade_date <= prev_date).order_by(StockDaily.trade_date.desc()).first()
    return float(daily.close) if daily else None

def calc_n_day_pct_chg(ts_code, trade_date, n):
    """计算指定股票在trade_date的N日涨幅（百分比）"""
    today_daily = StockDaily.query.filter_by(ts_code=ts_code, trade_date=trade_date).first()
    if not today_daily:
        return None
    today_close = float(today_daily.close)
    prev_close = get_close_price_n_days_ago(ts_code, trade_date, n)
    if prev_close is None or prev_close == 0:
        return None
    return round((today_close - prev_close) / prev_close * 100, 2)

def get_latest_stock_price(ts_code):
    """获取股票的最新价格信息"""
    latest_daily = StockDaily.query.filter_by(ts_code=ts_code).order_by(StockDaily.trade_date.desc()).first()
    if latest_daily:
        return {
            'close': float(latest_daily.close) if latest_daily.close else None,
            'open': float(latest_daily.open) if latest_daily.open else None,
            'high': float(latest_daily.high) if latest_daily.high else None,
            'low': float(latest_daily.low) if latest_daily.low else None,
            'trade_date': latest_daily.trade_date.strftime('%Y-%m-%d') if latest_daily.trade_date else None,
            'pct_chg': float(latest_daily.pct_chg) if latest_daily.pct_chg else None,
            'vol': float(latest_daily.vol) if latest_daily.vol else None,
            'amount': float(latest_daily.amount) if latest_daily.amount else None
        }
    return None 