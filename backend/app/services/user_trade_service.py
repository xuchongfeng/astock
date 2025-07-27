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