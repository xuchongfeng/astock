from app import db
from sqlalchemy.orm import relationship
from datetime import datetime


class Tag(db.Model):
    """股票标签表"""
    __tablename__ = 'tag'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键ID')
    name = db.Column(db.String(64), nullable=False, unique=True, comment='标签名称')
    description = db.Column(db.String(255), comment='标签描述')
    color = db.Column(db.String(16), default='#1890ff', comment='标签颜色')
    category = db.Column(db.String(32), default='trend', comment='标签分类：trend-走势，status-状态，custom-自定义')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')
    
    # 关联关系
    stock_tags = relationship("StockTag", back_populates="tag")
    
    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}', category='{self.category}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class StockTag(db.Model):
    """股票标签关联表"""
    __tablename__ = 'stock_tag'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键ID')
    ts_code = db.Column(db.String(16), nullable=False, comment='股票代码')
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False, comment='标签ID')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment='用户ID（NULL表示系统标签）')
    start_date = db.Column(db.Date, comment='标签开始日期')
    end_date = db.Column(db.Date, comment='标签结束日期')
    note = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')
    
    # 关联关系
    tag = relationship("Tag", back_populates="stock_tags")
    
    # 唯一约束
    __table_args__ = (
        db.UniqueConstraint('ts_code', 'tag_id', 'user_id', name='uk_stock_tag_user'),
        db.Index('idx_ts_code', 'ts_code'),
        db.Index('idx_tag_id', 'tag_id'),
        db.Index('idx_user_id', 'user_id')
    )
    
    def __repr__(self):
        return f"<StockTag(id={self.id}, ts_code='{self.ts_code}', tag_id={self.tag_id})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'ts_code': self.ts_code,
            'tag_id': self.tag_id,
            'user_id': self.user_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'note': self.note,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tag': self.tag.to_dict() if self.tag else None
        } 