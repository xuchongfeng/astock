from app import db
from datetime import datetime

class ThsIndexDaily(db.Model):
    __tablename__ = 'ths_index_daily'

    id = db.Column(db.Integer, primary_key=True)
    ts_code = db.Column(db.String(16), nullable=False, comment='TS指数代码')
    trade_date = db.Column(db.Date, nullable=False, comment='交易日')
    close = db.Column(db.Numeric(16, 4), comment='收盘点位')
    open = db.Column(db.Numeric(16, 4), comment='开盘点位')
    high = db.Column(db.Numeric(16, 4), comment='最高点位')
    low = db.Column(db.Numeric(16, 4), comment='最低点位')
    pre_close = db.Column(db.Numeric(16, 4), comment='昨日收盘点')
    avg_price = db.Column(db.Numeric(16, 4), comment='平均价')
    change = db.Column(db.Numeric(16, 4), comment='涨跌点位')
    pct_change = db.Column(db.Numeric(8, 4), comment='涨跌幅')
    vol = db.Column(db.Numeric(20, 4), comment='成交量')
    turnover_rate = db.Column(db.Numeric(8, 4), comment='换手率')
    total_mv = db.Column(db.Numeric(20, 4), comment='总市值')
    float_mv = db.Column(db.Numeric(20, 4), comment='流通市值')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    __table_args__ = (
        db.UniqueConstraint('ts_code', 'trade_date', name='uk_ts_code_trade_date'),
    )

    def as_dict(self):
        """返回字典格式，日期字段格式化为YYYY-MM-DD"""
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            
            # 格式化日期字段
            if isinstance(value, datetime):
                result[c.name] = value.strftime('%Y-%m-%d')
            elif isinstance(value, db.Date):
                result[c.name] = value.strftime('%Y-%m-%d') if value else None
            else:
                result[c.name] = value
                
        return result