from app import db

class Concept(db.Model):
    __tablename__ = 'concept'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    code = db.Column(db.String(16), nullable=False, comment='概念分类ID')
    name = db.Column(db.String(100), nullable=False, comment='概念分类名称')
    src = db.Column(db.String(10), default='ts', comment='来源')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    __table_args__ = (
        db.UniqueConstraint('code', name='uk_code'),
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 