from app import db

class DcIndex(db.Model):
    __tablename__ = 'dc_index'

    id = db.Column(db.Integer, primary_key=True)
    ts_code = db.Column(db.String(16), nullable=False, unique=True, comment='概念代码')
    name = db.Column(db.String(64), nullable=False, comment='概念名称')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 