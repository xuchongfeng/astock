from app import db

class UserPosition(db.Model):
    __tablename__ = 'user_position'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, comment='用户ID')
    ts_code = db.Column(db.String(16), nullable=False, comment='股票代码')
    quantity = db.Column(db.Integer, nullable=False, comment='持仓数量')
    avg_price = db.Column(db.Numeric(12, 4), nullable=False, comment='平均成本')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 