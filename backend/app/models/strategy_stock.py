from app import db

class StrategyStock(db.Model):
    __tablename__ = 'strategy_stock'

    id = db.Column(db.Integer, primary_key=True)
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=False, comment='策略ID')
    ts_code = db.Column(db.String(16), nullable=False, comment='股票代码')
    date = db.Column(db.Date, nullable=True, comment='关联日期')
    rating = db.Column(db.Integer, nullable=True, comment='评级')
    avg_amount_5d = db.Column(db.Numeric(20, 4), nullable=True, comment='最近5日平均交易额')
    hit_count_5d = db.Column(db.Integer, nullable=True, comment='最近5日命中策略次数')
    hit_count_15d = db.Column(db.Integer, nullable=True, comment='最近15日命中策略次数')
    hit_count_30d = db.Column(db.Integer, nullable=True, comment='最近30日命中策略次数')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 