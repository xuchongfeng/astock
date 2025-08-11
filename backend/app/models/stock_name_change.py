from app import db
from datetime import datetime

class StockNameChange(db.Model):
    """股票曾用名模型"""
    __tablename__ = 'stock_name_change'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ts_code = db.Column(db.String(16), nullable=False, index=True, comment='TS代码')
    name = db.Column(db.String(64), nullable=False, comment='证券名称')
    start_date = db.Column(db.Date, comment='开始日期')
    end_date = db.Column(db.Date, comment='结束日期')
    ann_date = db.Column(db.Date, comment='公告日期')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def as_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'ts_code': self.ts_code,
            'name': self.name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'ann_date': self.ann_date.isoformat() if self.ann_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<StockNameChange {self.ts_code} {self.name}>' 