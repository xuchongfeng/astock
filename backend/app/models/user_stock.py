from app import db

class UserStock(db.Model):
    __tablename__ = 'user_stock'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, comment='用户ID')
    ts_code = db.Column(db.String(16), nullable=False, comment='股票代码')
    rating = db.Column(db.Integer, nullable=True, comment='评级')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='关注时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'ts_code', name='uk_user_stock'),
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 