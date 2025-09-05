from app.models.ths_hot import ThsHot
from app import db
from datetime import datetime, date
from sqlalchemy import desc, asc, and_, or_

def get_all_hot_data(filters=None, query_only=False):
    """获取所有热榜数据"""
    query = ThsHot.query
    
    if filters:
        for key, value in filters.items():
            if value is not None:
                if key == 'trade_date':
                    query = query.filter(ThsHot.trade_date == value)
                elif key == 'ts_code':
                    query = query.filter(ThsHot.ts_code == value)
                elif key == 'data_type':
                    query = query.filter(ThsHot.data_type == value)
                elif key == 'start_date':
                    query = query.filter(ThsHot.trade_date >= value)
                elif key == 'end_date':
                    query = query.filter(ThsHot.trade_date <= value)
                elif key == 'search':
                    query = query.filter(
                        or_(
                            ThsHot.ts_name.like(f'%{value}%'),
                            ThsHot.ts_code.like(f'%{value}%'),
                            ThsHot.concept.like(f'%{value}%')
                        )
                    )
    
    if query_only:
        return query
    
    return query.all()

def get_hot_data_by_id(hot_id):
    """根据ID获取热榜数据"""
    return ThsHot.query.get(hot_id)

def get_hot_data_by_date_and_type(trade_date, data_type):
    """根据日期和数据类型获取热榜数据"""
    return ThsHot.query.filter(
        and_(
            ThsHot.trade_date == trade_date,
            ThsHot.data_type == data_type
        )
    ).order_by(ThsHot.rank).all()

def get_latest_hot_data(data_type=None, limit=100):
    """获取最新的热榜数据"""
    query = ThsHot.query
    
    if data_type:
        query = query.filter(ThsHot.data_type == data_type)
    
    # 获取最新日期
    latest_date = query.with_entities(db.func.max(ThsHot.trade_date)).scalar()
    
    if not latest_date:
        return []
    
    # 根据最新日期获取数据
    query = query.filter(ThsHot.trade_date == latest_date)
    return query.order_by(ThsHot.rank).limit(limit).all()

def get_hot_data_by_ts_code(ts_code, limit=50):
    """根据股票代码获取热榜历史数据"""
    return ThsHot.query.filter(
        ThsHot.ts_code == ts_code
    ).order_by(desc(ThsHot.trade_date)).limit(limit).all()

def create_hot_data(hot_data):
    """创建热榜数据"""
    try:
        hot = ThsHot(**hot_data)
        db.session.add(hot)
        db.session.commit()
        return hot
    except Exception as e:
        db.session.rollback()
        raise e

def update_hot_data(hot_id, update_data):
    """更新热榜数据"""
    try:
        hot = ThsHot.query.get(hot_id)
        if not hot:
            return None
        
        for key, value in update_data.items():
            if hasattr(hot, key):
                setattr(hot, key, value)
        
        hot.updated_at = datetime.now()
        db.session.commit()
        return hot
    except Exception as e:
        db.session.rollback()
        raise e

def delete_hot_data(hot_id):
    """删除热榜数据"""
    try:
        hot = ThsHot.query.get(hot_id)
        if not hot:
            return False
        
        db.session.delete(hot)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e

def upsert_hot_data(hot_data_list):
    """批量插入或更新热榜数据"""
    try:
        for hot_data in hot_data_list:
            # 检查是否已存在相同记录
            existing = ThsHot.query.filter(
                and_(
                    ThsHot.trade_date == hot_data['trade_date'],
                    ThsHot.data_type == hot_data['data_type'],
                    ThsHot.ts_code == hot_data['ts_code']
                )
            ).first()
            
            if existing:
                # 更新现有记录
                for key, value in hot_data.items():
                    if hasattr(existing, key) and key not in ['id', 'created_at']:
                        setattr(existing, key, value)
                existing.updated_at = datetime.now()
            else:
                # 创建新记录
                hot = ThsHot(**hot_data)
                db.session.add(hot)
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e

def get_hot_data_statistics(start_date=None, end_date=None):
    """获取热榜数据统计信息"""
    query = ThsHot.query
    
    if start_date:
        query = query.filter(ThsHot.trade_date >= start_date)
    if end_date:
        query = query.filter(ThsHot.trade_date <= end_date)
    
    # 统计各类型数据数量
    type_stats = db.session.query(
        ThsHot.data_type,
        db.func.count(ThsHot.id).label('count')
    ).group_by(ThsHot.data_type).all()
    
    # 统计日期范围
    date_range = db.session.query(
        db.func.min(ThsHot.trade_date).label('min_date'),
        db.func.max(ThsHot.trade_date).label('max_date')
    ).scalar()
    
    return {
        'type_statistics': [{'data_type': stat.data_type, 'count': stat.count} for stat in type_stats],
        'date_range': {
            'start_date': date_range.min_date.strftime('%Y-%m-%d') if date_range.min_date else None,
            'end_date': date_range.max_date.strftime('%Y-%m-%d') if date_range.max_date else None
        }
    } 