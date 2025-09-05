from app.models.ths_member import ThsMember
from app.models.stock_daily import StockDaily
from app import db
from sqlalchemy import desc, asc

def get_all_ths_member(filters=None, query_only=False):
    query = ThsMember.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(ThsMember, attr) == value)
    if query_only:
        return query
    return query.all()

def get_ths_member_with_daily_data(filters=None, trade_date=None, query_only=False):
    """
    获取成分股数据，关联stock_daily表获取涨幅信息
    
    Args:
        filters: 过滤条件
        trade_date: 交易日期，用于获取涨幅信息
        query_only: 是否只返回查询对象
    
    Returns:
        查询对象或结果列表
    """
    # 构建基础查询，关联stock_daily表
    query = db.session.query(
        ThsMember,
        StockDaily.pct_chg.label('pct_chg'),
        StockDaily.change.label('change'),
        StockDaily.close.label('close'),
        StockDaily.pre_close.label('pre_close'),
        StockDaily.vol.label('vol'),
        StockDaily.amount.label('amount'),
        StockDaily.turnover_rate.label('turnover_rate')
    ).outerjoin(
        StockDaily,
        db.and_(
            ThsMember.con_code == StockDaily.ts_code,
            StockDaily.trade_date == trade_date
        )
    )
    
    # 应用过滤条件
    if filters:
        for attr, value in filters.items():
            if hasattr(ThsMember, attr):
                query = query.filter(getattr(ThsMember, attr) == value)
    
    # 如果有交易日期，按涨幅倒序排序
    if trade_date:
        query = query.order_by(desc(StockDaily.pct_chg))
    
    if query_only:
        return query
    return query.all()

def get_ths_member_by_id(member_id):
    return ThsMember.query.get(member_id)

def create_ths_member(data):
    member = ThsMember(**data)
    db.session.add(member)
    db.session.commit()
    return member

def update_ths_member(member_id, data):
    member = ThsMember.query.get(member_id)
    if not member:
        return None
    for key, value in data.items():
        setattr(member, key, value)
    db.session.commit()
    return member

def delete_ths_member(member_id):
    member = ThsMember.query.get(member_id)
    if not member:
        return False
    db.session.delete(member)
    db.session.commit()
    return True