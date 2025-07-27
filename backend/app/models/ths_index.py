from app import db

class ThsIndex(db.Model):
    __tablename__ = 'ths_index'

    id = db.Column(db.Integer, primary_key=True)
    ts_code = db.Column(db.String(16), unique=True, nullable=False, comment='指数代码')
    name = db.Column(db.String(64), nullable=False, comment='指数名称')
    count = db.Column(db.Integer, comment='成分个数')
    exchange = db.Column(db.String(8), comment='交易所')
    list_date = db.Column(db.Date, comment='上市日期')
    type = db.Column(db.String(8), comment='指数类型')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 