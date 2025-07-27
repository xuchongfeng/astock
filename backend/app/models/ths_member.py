from app import db

class ThsMember(db.Model):
    __tablename__ = 'ths_member'

    id = db.Column(db.Integer, primary_key=True)
    ts_code = db.Column(db.String(16), nullable=False, comment='板块指数代码')
    con_code = db.Column(db.String(16), nullable=False, comment='股票代码')
    con_name = db.Column(db.String(64), comment='股票名称')
    weight = db.Column(db.Float, comment='权重')
    in_date = db.Column(db.Date, comment='纳入日期')
    out_date = db.Column(db.Date, comment='剔除日期')
    is_new = db.Column(db.String(2), comment='是否最新Y是N否')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    __table_args__ = (
        db.UniqueConstraint('ts_code', 'con_code', name='uk_ths_member'),
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}