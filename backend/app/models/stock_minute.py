from app import db
from datetime import datetime

class StockMinute(db.Model):
    """分钟行情数据模型"""
    __tablename__ = 'stock_minute'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    ts_code = db.Column(db.String(16), nullable=False, index=True, comment='TS代码')
    trade_time = db.Column(db.DateTime, nullable=False, index=True, comment='交易时间')
    open = db.Column(db.Float, comment='开盘价')
    high = db.Column(db.Float, comment='最高价')
    low = db.Column(db.Float, comment='最低价')
    close = db.Column(db.Float, comment='收盘价')
    pre_close = db.Column(db.Float, comment='昨收价')
    change = db.Column(db.Float, comment='涨跌额')
    pct_chg = db.Column(db.Float, comment='涨跌幅')
    vol = db.Column(db.BigInteger, comment='成交量（手）')
    amount = db.Column(db.Float, comment='成交额（千元）')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 唯一约束
    __table_args__ = (
        db.UniqueConstraint('ts_code', 'trade_time', name='uk_ts_code_trade_time'),
    )
    
    def as_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'ts_code': self.ts_code,
            'trade_time': self.trade_time.isoformat() if self.trade_time else None,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'pre_close': self.pre_close,
            'change': self.change,
            'pct_chg': self.pct_chg,
            'vol': self.vol,
            'amount': self.amount,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<StockMinute {self.ts_code} {self.trade_time}>' 