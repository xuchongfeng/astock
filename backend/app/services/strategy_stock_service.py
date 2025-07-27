from app.models.strategy_stock import StrategyStock
from app import db

def get_all_strategy_stocks(filters=None, query_only=False):
    query = StrategyStock.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(StrategyStock, attr) == value)
    if query_only:
        return query
    return query.all()

def get_strategy_stock_by_id(stock_id):
    return StrategyStock.query.get(stock_id)

def create_strategy_stock(data):
    stock = StrategyStock(**data)
    db.session.add(stock)
    db.session.commit()
    return stock

def update_strategy_stock(stock_id, data):
    stock = StrategyStock.query.get(stock_id)
    if not stock:
        return None
    for key, value in data.items():
        setattr(stock, key, value)
    db.session.commit()
    return stock

def delete_strategy_stock(stock_id):
    stock = StrategyStock.query.get(stock_id)
    if not stock:
        return False
    db.session.delete(stock)
    db.session.commit()
    return True 