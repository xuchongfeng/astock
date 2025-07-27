from app import db

class UserTrade(db.Model):
    __tablename__ = 'user_trade'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, comment='用户ID')
    ts_code = db.Column(db.String(16), nullable=False, comment='股票代码')
    trade_type = db.Column(db.String(8), nullable=False, comment='交易类型：buy/sell')
    quantity = db.Column(db.Integer, nullable=False, comment='交易数量')
    price = db.Column(db.Numeric(12, 4), nullable=False, comment='交易价格')
    trade_date = db.Column(db.Date, nullable=False, comment='交易日期')
    profit_loss = db.Column(db.Numeric(12, 4), nullable=True, comment='盈利/亏损')
    note = db.Column(db.Text, nullable=True, comment='笔记')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 