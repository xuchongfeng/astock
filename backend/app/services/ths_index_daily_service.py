from app.models.ths_index_daily import ThsIndexDaily
from app.models.ths_index import ThsIndex
from app import db

def get_all_ths_index_daily(filters=None, query_only=False):
    query = ThsIndexDaily.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(ThsIndexDaily, attr) == value)
    if query_only:
        return query
    return query.all()

def get_all_ths_index_daily_with_name(filters=None, query_only=False):
    """获取包含指数名称的指数日线数据"""
    # 使用更明确的字段选择
    query = db.session.query(
        ThsIndexDaily,
        ThsIndex.name
    ).outerjoin(
        ThsIndex, 
        ThsIndexDaily.ts_code == ThsIndex.ts_code
    )
    
    if filters:
        for attr, value in filters.items():
            if hasattr(ThsIndexDaily, attr):
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