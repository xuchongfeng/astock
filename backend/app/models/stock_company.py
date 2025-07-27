from app import db



class StockCompany(db.Model):
    __tablename__ = 'stock_company'

    id = db.Column(db.Integer, primary_key=True)
    ts_code = db.Column(db.String(16), unique=True, nullable=False)
    symbol = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    area = db.Column(db.String(32))
    industry = db.Column(db.String(64))
    fullname = db.Column(db.String(128))
    enname = db.Column(db.String(128))
    market = db.Column(db.String(16))
    list_date = db.Column(db.Date)
    exchange = db.Column(db.String(8))
    chairman = db.Column(db.String(32))
    manager = db.Column(db.String(32))
    secretary = db.Column(db.String(32))
    reg_capital = db.Column(db.Numeric(20,2))
    setup_date = db.Column(db.Date)
    province = db.Column(db.String(32))
    website = db.Column(db.String(128))
    email = db.Column(db.String(64))
    employees = db.Column(db.Integer)
    main_business = db.Column(db.Text)
    business_scope = db.Column(db.Text)
    status = db.Column(db.String(16))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}