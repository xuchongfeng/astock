from app import db

class StockDailyBasic(db.Model):
    __tablename__ = 'stock_daily_basic'

    id = db.Column(db.BigInteger, primary_key=True)
    ts_code = db.Column(db.String(16), nullable=False, index=True, comment='TS股票代码')
    trade_date = db.Column(db.Date, nullable=False, index=True, comment='交易日期')
    close = db.Column(db.Numeric(12, 4), comment='当日收盘价')
    turnover_rate = db.Column(db.Numeric(8, 4), comment='换手率（%）')
    turnover_rate_f = db.Column(db.Numeric(8, 4), comment='换手率（自由流通股）')
    volume_ratio = db.Column(db.Numeric(8, 4), comment='量比')
    pe = db.Column(db.Numeric(12, 4), comment='市盈率（总市值/净利润，亏损的PE为空）')
    pe_ttm = db.Column(db.Numeric(12, 4), comment='市盈率（TTM，亏损的PE为空）')
    pb = db.Column(db.Numeric(12, 4), comment='市净率（总市值/净资产）')
    ps = db.Column(db.Numeric(12, 4), comment='市销率')
    ps_ttm = db.Column(db.Numeric(12, 4), comment='市销率（TTM）')
    dv_ratio = db.Column(db.Numeric(8, 4), comment='股息率（%）')
    dv_ttm = db.Column(db.Numeric(8, 4), comment='股息率（TTM）（%）')
    total_share = db.Column(db.Numeric(20, 4), comment='总股本（万股）')
    float_share = db.Column(db.Numeric(20, 4), comment='流通股本（万股）')
    free_share = db.Column(db.Numeric(20, 4), comment='自由流通股本（万）')
    total_mv = db.Column(db.Numeric(20, 4), comment='总市值（万元）')
    circ_mv = db.Column(db.Numeric(20, 4), comment='流通市值（万元）')

    __table_args__ = (
        db.UniqueConstraint('ts_code', 'trade_date', name='uk_stock_daily_basic_ts_code_trade_date'),
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 