from app.models.ths_index_daily import ThsIndexDaily
from app import db

def get_all_ths_index_daily(filters=None, query_only=False):
    query = ThsIndexDaily.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(ThsIndexDaily, attr) == value)
    if query_only:
        return query
    return query.all()

def get_ths_index_daily_by_id(daily_id):
    return ThsIndexDaily.query.get(daily_id)

def create_ths_index_daily(data):
    daily = ThsIndexDaily(**data)
    db.session.add(daily)
    db.session.commit()
    return daily

def update_ths_index_daily(daily_id, data):
    daily = ThsIndexDaily.query.get(daily_id)
    if not daily:
        return None
    for key, value in data.items():
        setattr(daily, key, value)
    db.session.commit()
    return daily

def delete_ths_index_daily(daily_id):
    daily = ThsIndexDaily.query.get(daily_id)
    if not daily:
        return False
    db.session.delete(daily)
    db.session.commit()
    return True