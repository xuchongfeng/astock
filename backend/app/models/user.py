from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, comment='用户名')
    email = db.Column(db.String(120), unique=True, nullable=False, comment='邮箱')
    password_hash = db.Column(db.String(128), nullable=False, comment='密码哈希')
    nickname = db.Column(db.String(64), comment='昵称')
    avatar = db.Column(db.String(255), comment='头像URL')
    status = db.Column(db.String(16), default='active', comment='状态：active/inactive')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 