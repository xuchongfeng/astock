from app import db
from datetime import datetime

class TradeCalendar(db.Model):
    """交易日历模型"""
    __tablename__ = 'trade_calendar'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exchange = db.Column(db.String(8), nullable=False, index=True, comment='交易所 SSE上交所 SZSE深交所')
    cal_date = db.Column(db.Date, nullable=False, index=True, comment='日历日期')
    is_open = db.Column(db.Boolean, nullable=False, comment='是否交易 0休市 1交易')
    pretrade_date = db.Column(db.Date, comment='上一交易日')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 唯一约束
    __table_args__ = (
        db.UniqueConstraint('exchange', 'cal_date', name='uk_exchange_cal_date'),
    )
    
    def as_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'exchange': self.exchange,
            'cal_date': self.cal_date.isoformat() if self.cal_date else None,
            'is_open': self.is_open,
            'pretrade_date': self.pretrade_date.isoformat() if self.pretrade_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<TradeCalendar {self.exchange} {self.cal_date}>' 