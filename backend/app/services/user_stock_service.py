from app.models.user_stock import UserStock
from app import db

def get_user_stocks(user_id, query_only=False):
    query = UserStock.query.filter_by(user_id=user_id)
    if query_only:
        return query
    return query.all()

def get_user_stock_by_id(stock_id):
    return UserStock.query.get(stock_id)

def get_user_stock_by_user_and_code(user_id, ts_code):
    return UserStock.query.filter_by(user_id=user_id, ts_code=ts_code).first()

def get_user_stock_by_user_and_id(user_id, stock_id):
    return UserStock.query.filter_by(user_id=user_id, id=stock_id).first()

def create_user_stock(data):
    user_stock = UserStock(**data)
    db.session.add(user_stock)
    db.session.commit()
    return user_stock

def update_user_stock(stock_id, data):
    user_stock = UserStock.query.get(stock_id)
    if not user_stock:
        return None
    for key, value in data.items():
        setattr(user_stock, key, value)
    db.session.commit()
    return user_stock

def delete_user_stock(stock_id):
    user_stock = UserStock.query.get(stock_id)
    if not user_stock:
        return False
    db.session.delete(user_stock)
    db.session.commit()
    return True

def delete_user_stock_by_user_and_code(user_id, ts_code):
    user_stock = UserStock.query.filter_by(user_id=user_id, ts_code=ts_code).first()
    if not user_stock:
        return False
    db.session.delete(user_stock)
    db.session.commit()
    return True

def delete_user_stock_by_user_and_id(user_id, stock_id):
    user_stock = UserStock.query.filter_by(user_id=user_id, id=stock_id).first()
    if not user_stock:
        return False
    db.session.delete(user_stock)
    db.session.commit()
    return True 