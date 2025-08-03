from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from app.models.tag import Tag, StockTag
from app import db
    
def create_tag(name: str, description: str = None, color: str = '#1890ff', 
               category: str = 'trend') -> Tag:
    """创建标签"""
    tag = Tag(
        name=name,
        description=description,
        color=color,
        category=category
    )
    db.session.add(tag)
    db.session.commit()
    db.session.refresh(tag)
    return tag
    
def get_tag_by_id(tag_id: int) -> Optional[Tag]:
    """根据ID获取标签"""
    return Tag.query.get(tag_id)

def get_tag_by_name(name: str) -> Optional[Tag]:
    """根据名称获取标签"""
    return Tag.query.filter_by(name=name).first()

def get_all_tags(category: str = None) -> List[Tag]:
    """获取所有标签"""
    query = Tag.query
    if category:
        query = query.filter(Tag.category == category)
    return query.order_by(Tag.name).all()
    
def update_tag(tag_id: int, **kwargs) -> Optional[Tag]:
    """更新标签"""
    tag = get_tag_by_id(tag_id)
    if not tag:
        return None
    
    for key, value in kwargs.items():
        if hasattr(tag, key):
            setattr(tag, key, value)
    
    db.session.commit()
    db.session.refresh(tag)
    return tag

def delete_tag(tag_id: int) -> bool:
    """删除标签"""
    tag = get_tag_by_id(tag_id)
    if not tag:
        return False
    
    # 检查是否有关联的股票标签
    stock_tags = StockTag.query.filter_by(tag_id=tag_id).count()
    if stock_tags > 0:
        raise ValueError("该标签下还有关联的股票，无法删除")
    
    db.session.delete(tag)
    db.session.commit()
    return True
    
def add_stock_tag(ts_code: str, tag_id: int, user_id: int = None, 
                  start_date: date = None, end_date: date = None, note: str = None) -> StockTag:
    """为股票添加标签"""
    # 检查是否已存在相同的关联
    existing = StockTag.query.filter(
        and_(
            StockTag.ts_code == ts_code,
            StockTag.tag_id == tag_id,
            StockTag.user_id == user_id
        )
    ).first()
    
    if existing:
        raise ValueError("该股票已存在此标签")
    
    stock_tag = StockTag(
        ts_code=ts_code,
        tag_id=tag_id,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        note=note
    )
    db.session.add(stock_tag)
    db.session.commit()
    db.session.refresh(stock_tag)
    return stock_tag
    
def get_stock_tags(ts_code: str = None, tag_id: int = None, 
                   user_id: int = None, include_expired: bool = True) -> List[StockTag]:
    """获取股票标签关联"""
    query = StockTag.query.join(Tag)
    
    if ts_code:
        query = query.filter(StockTag.ts_code == ts_code)
    
    if tag_id:
        query = query.filter(StockTag.tag_id == tag_id)
    
    if user_id is not None:
        query = query.filter(StockTag.user_id == user_id)
    
    if not include_expired:
        today = date.today()
        query = query.filter(
            or_(
                StockTag.end_date.is_(None),
                StockTag.end_date >= today
            )
        )
    
    return query.order_by(StockTag.created_at.desc()).all()
    
def get_stocks_by_tag(tag_id: int, user_id: int = None) -> List[str]:
    """根据标签获取股票代码列表"""
    query = StockTag.query.with_entities(StockTag.ts_code).filter_by(tag_id=tag_id)
    
    if user_id is not None:
        query = query.filter(StockTag.user_id == user_id)
    
    return [row[0] for row in query.all()]
    
def remove_stock_tag(ts_code: str, tag_id: int, user_id: int = None) -> bool:
    """移除股票的标签"""
    stock_tag = StockTag.query.filter(
        and_(
            StockTag.ts_code == ts_code,
            StockTag.tag_id == tag_id,
            StockTag.user_id == user_id
        )
    ).first()
    
    if not stock_tag:
        return False
    
    db.session.delete(stock_tag)
    db.session.commit()
    return True
    
def update_stock_tag(ts_code: str, tag_id: int, user_id: int = None, 
                    **kwargs) -> Optional[StockTag]:
    """更新股票标签关联"""
    stock_tag = StockTag.query.filter(
        and_(
            StockTag.ts_code == ts_code,
            StockTag.tag_id == tag_id,
            StockTag.user_id == user_id
        )
    ).first()
    
    if not stock_tag:
        return None
    
    for key, value in kwargs.items():
        if hasattr(stock_tag, key):
            setattr(stock_tag, key, value)
    
    db.session.commit()
    db.session.refresh(stock_tag)
    return stock_tag
    
def get_stock_tag_summary(ts_code: str, user_id: int = None) -> Dict[str, Any]:
    """获取股票的标签摘要"""
    stock_tags = get_stock_tags(ts_code=ts_code, user_id=user_id)
    
    summary = {
        'ts_code': ts_code,
        'tags': [],
        'trend_tags': [],
        'status_tags': [],
        'custom_tags': []
    }
    
    for stock_tag in stock_tags:
        tag_info = stock_tag.to_dict()
        summary['tags'].append(tag_info)
        
        if stock_tag.tag.category == 'trend':
            summary['trend_tags'].append(tag_info)
        elif stock_tag.tag.category == 'status':
            summary['status_tags'].append(tag_info)
        elif stock_tag.tag.category == 'custom':
            summary['custom_tags'].append(tag_info)
    
    return summary
    
def get_popular_tags(limit: int = 10) -> List[Dict[str, Any]]:
    """获取热门标签（使用频率最高的标签）"""
    result = db.session.query(
        Tag.id,
        Tag.name,
        Tag.description,
        Tag.color,
        Tag.category,
        func.count(StockTag.id).label('usage_count')
    ).join(StockTag, Tag.id == StockTag.tag_id)\
     .group_by(Tag.id)\
     .order_by(func.count(StockTag.id).desc())\
     .limit(limit)\
     .all()
    
    return [
        {
            'id': row.id,
            'name': row.name,
            'description': row.description,
            'color': row.color,
            'category': row.category,
            'usage_count': row.usage_count
        }
        for row in result
    ] 