from app import db
from datetime import datetime

class ThsHot(db.Model):
    """同花顺热榜数据表"""
    __tablename__ = 'ths_hot'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    trade_date = db.Column(db.Date, nullable=False, comment='交易日期')
    data_type = db.Column(db.String(50), nullable=False, comment='数据类型')
    ts_code = db.Column(db.String(20), nullable=False, comment='股票代码')
    ts_name = db.Column(db.String(100), nullable=False, comment='股票名称')
    rank = db.Column(db.Integer, nullable=False, comment='排行')
    pct_change = db.Column(db.Float, comment='涨跌幅%')
    current_price = db.Column(db.Float, comment='当前价格')
    concept = db.Column(db.Text, comment='标签')
    rank_reason = db.Column(db.Text, comment='上榜解读')
    hot = db.Column(db.Float, comment='热度值')
    rank_time = db.Column(db.String(20), comment='排行榜获取时间')
    
    # 时间戳
    created_at = db.Column(db.TIMESTAMP, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 索引
    __table_args__ = (
        db.Index('idx_trade_date', 'trade_date'),
        db.Index('idx_ts_code', 'ts_code'),
        db.Index('idx_data_type', 'data_type'),
        db.Index('idx_rank', 'rank'),
        db.Index('idx_trade_date_data_type', 'trade_date', 'data_type'),
    )
    
    def as_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'trade_date': self.trade_date.strftime('%Y-%m-%d') if self.trade_date else None,
            'data_type': self.data_type,
            'ts_code': self.ts_code,
            'ts_name': self.ts_name,
            'rank': self.rank,
            'pct_change': self.pct_change,
            'current_price': self.current_price,
            'concept': self.concept,
            'rank_reason': self.rank_reason,
            'hot': self.hot,
            'rank_time': self.rank_time,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 