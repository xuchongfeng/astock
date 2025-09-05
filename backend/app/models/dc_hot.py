from app import db
from datetime import datetime


class DcHot(db.Model):
    """东方财富热榜数据表"""
    __tablename__ = 'dc_hot'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    trade_date = db.Column(db.String(8), nullable=False, comment='交易日期')
    data_type = db.Column(db.String(50), nullable=False, comment='数据类型')
    ts_code = db.Column(db.String(20), nullable=False, comment='股票代码')
    ts_name = db.Column(db.String(100), nullable=False, comment='股票名称')
    rank = db.Column(db.Integer, nullable=False, comment='排行或者热度')
    pct_change = db.Column(db.Float, comment='涨跌幅%')
    current_price = db.Column(db.Float, comment='当前价')
    rank_time = db.Column(db.String(20), comment='排行榜获取时间')
    market = db.Column(db.String(50), comment='类型(A股市场、ETF基金、港股市场、美股市场)')
    hot_type = db.Column(db.String(50), comment='热点类型(人气榜、飙升榜)')
    is_new = db.Column(db.String(1), default='Y', comment='是否最新')

    created_at = db.Column(db.TIMESTAMP, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    __table_args__ = (
        db.Index('idx_trade_date', 'trade_date'),
        db.Index('idx_ts_code', 'ts_code'),
        db.Index('idx_market', 'market'),
        db.Index('idx_hot_type', 'hot_type'),
        db.Index('idx_rank', 'rank'),
    )

    def as_dict(self):
        return {
            'id': self.id,
            'trade_date': self.trade_date,
            'data_type': self.data_type,
            'ts_code': self.ts_code,
            'ts_name': self.ts_name,
            'rank': self.rank,
            'pct_change': self.pct_change,
            'current_price': self.current_price,
            'rank_time': self.rank_time,
            'market': self.market,
            'hot_type': self.hot_type,
            'is_new': self.is_new,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
        }


