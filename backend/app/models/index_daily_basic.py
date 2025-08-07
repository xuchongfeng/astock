from app import db
from datetime import datetime

class IndexDailyBasic(db.Model):
    """大盘指数每日指标模型"""
    __tablename__ = 'index_daily_basic'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ts_code = db.Column(db.String(20), nullable=False, index=True, comment='TS代码')
    trade_date = db.Column(db.Date, nullable=False, index=True, comment='交易日期')
    total_mv = db.Column(db.Float, comment='当日总市值（元）')
    float_mv = db.Column(db.Float, comment='当日流通市值（元）')
    total_share = db.Column(db.Float, comment='当日总股本（股）')
    float_share = db.Column(db.Float, comment='当日流通股本（股）')
    free_share = db.Column(db.Float, comment='当日自由流通股本（股）')
    turnover_rate = db.Column(db.Float, comment='换手率')
    turnover_rate_f = db.Column(db.Float, comment='换手率(基于自由流通股本)')
    pe = db.Column(db.Float, comment='市盈率')
    pe_ttm = db.Column(db.Float, comment='市盈率TTM')
    pb = db.Column(db.Float, comment='市净率')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 唯一约束
    __table_args__ = (
        db.UniqueConstraint('ts_code', 'trade_date', name='uk_ts_code_trade_date'),
    )
    
    def as_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'ts_code': self.ts_code,
            'trade_date': self.trade_date.isoformat() if self.trade_date else None,
            'total_mv': self.total_mv,
            'float_mv': self.float_mv,
            'total_share': self.total_share,
            'float_share': self.float_share,
            'free_share': self.free_share,
            'turnover_rate': self.turnover_rate,
            'turnover_rate_f': self.turnover_rate_f,
            'pe': self.pe,
            'pe_ttm': self.pe_ttm,
            'pb': self.pb,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<IndexDailyBasic {self.ts_code} {self.trade_date}>' 