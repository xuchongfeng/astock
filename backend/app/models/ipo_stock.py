from app import db
from datetime import datetime

class IpoStock(db.Model):
    """IPO新股信息模型"""
    __tablename__ = 'ipo_stock'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ts_code = db.Column(db.String(16), nullable=False, unique=True, comment='TS代码')
    name = db.Column(db.String(64), nullable=False, comment='股票名称')
    ipo_date = db.Column(db.Date, comment='上市日期')
    issue_date = db.Column(db.Date, comment='发行日期')
    amount = db.Column(db.Float, comment='发行总量（万股）')
    market_amount = db.Column(db.Float, comment='发行流通市值（万元）')
    price = db.Column(db.Float, comment='发行价格')
    pe = db.Column(db.Float, comment='发行市盈率')
    limit_amount = db.Column(db.Float, comment='发行后总股本（万股）')
    funds = db.Column(db.Float, comment='募集资金（万元）')
    ballot = db.Column(db.Float, comment='中签率')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def as_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'ts_code': self.ts_code,
            'name': self.name,
            'ipo_date': self.ipo_date.isoformat() if self.ipo_date else None,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'amount': self.amount,
            'market_amount': self.market_amount,
            'price': self.price,
            'pe': self.pe,
            'limit_amount': self.limit_amount,
            'funds': self.funds,
            'ballot': self.ballot,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<IpoStock {self.ts_code} {self.name}>' 