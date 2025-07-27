from app import db

class StockDaily(db.Model):
    __tablename__ = 'stock_daily'

    id = db.Column(db.BigInteger, primary_key=True)
    ts_code = db.Column(db.String(16), nullable=False, index=True, comment='股票代码（如 000001.SZ）')
    trade_date = db.Column(db.Date, nullable=False, index=True, comment='交易日期')
    open = db.Column(db.Numeric(12, 4), comment='开盘价')
    high = db.Column(db.Numeric(12, 4), comment='最高价')
    low = db.Column(db.Numeric(12, 4), comment='最低价')
    close = db.Column(db.Numeric(12, 4), comment='收盘价')
    pre_close = db.Column(db.Numeric(12, 4), comment='昨收价')
    change = db.Column(db.Numeric(12, 4), comment='涨跌额')
    pct_chg = db.Column(db.Numeric(8, 4), comment='涨跌幅（%）')
    vol = db.Column(db.BigInteger, comment='成交量（手）')
    amount = db.Column(db.Numeric(20, 4), comment='成交额（元）')
    turnover_rate = db.Column(db.Numeric(8, 4), comment='换手率（%）')

    __table_args__ = (
        db.UniqueConstraint('ts_code', 'trade_date', name='uk_ts_code_trade_date'),
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 