from app import db

class StockNote(db.Model):
    __tablename__ = 'stock_note'

    id = db.Column(db.Integer, primary_key=True)
    ts_code = db.Column(db.String(16), nullable=False, comment='股票代码')
    note_date = db.Column(db.Date, nullable=False, comment='记录日期')
    comment = db.Column(db.Text, nullable=True, comment='评论')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 