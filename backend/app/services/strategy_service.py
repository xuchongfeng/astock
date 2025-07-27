from app.models.strategy import Strategy
from app import db

def get_all_strategies(filters=None, query_only=False):
    query = Strategy.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(Strategy, attr) == value)
    if query_only:
        return query
    return query.all()

def get_strategy_by_id(strategy_id):
    return Strategy.query.get(strategy_id)

def create_strategy(data):
    strategy = Strategy(**data)
    db.session.add(strategy)
    db.session.commit()
    return strategy

def update_strategy(strategy_id, data):
    strategy = Strategy.query.get(strategy_id)
    if not strategy:
        return None
    for key, value in data.items():
        setattr(strategy, key, value)
    db.session.commit()
    return strategy

def delete_strategy(strategy_id):
    strategy = Strategy.query.get(strategy_id)
    if not strategy:
        return False
    db.session.delete(strategy)
    db.session.commit()
    return True 