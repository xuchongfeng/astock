from app import db

class IndustryStats(db.Model):
    __tablename__ = 'industry_stats'

    id = db.Column(db.Integer, primary_key=True)
    industry_id = db.Column(db.Integer, nullable=False, comment='行业ID')
    stat_date = db.Column(db.Date, nullable=False, comment='统计日期')
    company_count = db.Column(db.Integer, nullable=False, comment='行业下公司总数')
    total_amount = db.Column(db.Numeric(24, 4), nullable=False, comment='行业公司当日成交总额（元）')
    up_count = db.Column(db.Integer, nullable=False, comment='上涨公司数')
    down_count = db.Column(db.Integer, nullable=False, comment='下跌公司数')
    flat_count = db.Column(db.Integer, nullable=False, comment='平盘公司数')
    created_at = db.Column(db.DateTime, default=db.func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')

    __table_args__ = (
        db.UniqueConstraint('industry_id', 'stat_date', name='uk_industry_date'),
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 