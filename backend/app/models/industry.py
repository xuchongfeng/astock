from app import db

class Industry(db.Model):
    __tablename__ = 'industry'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, comment='行业名称')
    description = db.Column(db.String(255), comment='行业描述')
    parent_id = db.Column(db.Integer, db.ForeignKey('industry.id'), nullable=True, comment='父行业ID')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 