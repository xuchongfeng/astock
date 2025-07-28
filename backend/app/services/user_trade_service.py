from app.models.user_trade import UserTrade
from app import db

def get_all_trades(filters=None, query_only=False):
    query = UserTrade.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(UserTrade, attr) == value)
    if query_only:
        return query
    return query.all()

def get_trade_by_id(trade_id):
    return UserTrade.query.get(trade_id)

def create_trade(data):
    trade = UserTrade(**data)
    db.session.add(trade)
    db.session.commit()
    return trade

def update_trade(trade_id, data):
    trade = UserTrade.query.get(trade_id)
    if not trade:
        return None
    for key, value in data.items():
        setattr(trade, key, value)
    db.session.commit()
    return trade

def delete_trade(trade_id):
    trade = UserTrade.query.get(trade_id)
    if not trade:
        return False
    db.session.delete(trade)
    db.session.commit()
    return True

def get_latest_buy_trade(user_id, ts_code):
    """获取指定用户和股票的最新买入记录"""
    return UserTrade.query.filter(
        UserTrade.user_id == user_id,
        UserTrade.ts_code == ts_code,
        UserTrade.trade_type == 'buy'
    ).order_by(UserTrade.trade_date.desc(), UserTrade.id.desc()).first()

def calculate_profit_loss(sell_price, sell_quantity, buy_price, buy_quantity):
    """计算盈利/亏损"""
    if not buy_price or not sell_price:
        return None
    
    # 计算平均买入价格
    total_buy_amount = buy_price * buy_quantity
    total_sell_amount = sell_price * sell_quantity
    
    # 盈利 = 卖出金额 - 买入金额
    profit_loss = total_sell_amount - total_buy_amount
    
    return round(profit_loss, 4) 