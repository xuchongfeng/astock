from app import db
from datetime import datetime

class IndexBasic(db.Model):
    __tablename__ = 'index_basic'

    id = db.Column(db.Integer, primary_key=True)
    ts_code = db.Column(db.String(16), unique=True, nullable=False, comment='TS代码')
    name = db.Column(db.String(64), nullable=False, comment='简称')
    fullname = db.Column(db.String(128), comment='指数全称')
    market = db.Column(db.String(16), comment='市场')
    publisher = db.Column(db.String(32), comment='发布方')
    index_type = db.Column(db.String(32), comment='指数风格')
    category = db.Column(db.String(32), comment='指数类别')
    base_date = db.Column(db.String(8), comment='基期')
    base_point = db.Column(db.Numeric(12, 2), comment='基点')
    list_date = db.Column(db.String(8), comment='发布日期')
    weight_rule = db.Column(db.String(32), comment='加权方式')
    desc = db.Column(db.Text, comment='描述')
    exp_date = db.Column(db.String(8), comment='终止日期')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    def as_dict(self):
        """返回字典格式，日期字段格式化为YYYY-MM-DD"""
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            
            # 格式化日期字段
            if isinstance(value, datetime):
                result[c.name] = value.strftime('%Y-%m-%d')
            elif isinstance(value, db.Date):
                result[c.name] = value.strftime('%Y-%m-%d') if value else None
            else:
                result[c.name] = value
                
        return result
