from app.models.stock_company import StockCompany
from app import db

def get_all_companies(query_only=False):
    query = StockCompany.query
    if query_only:
        return query
    return query.all()

def get_company_by_id(company_id):
    return StockCompany.query.get(company_id)

def get_company_by_ts_code(ts_code):
    return StockCompany.query.filter_by(ts_code=ts_code).first()

def create_company(data):
    company = StockCompany(**data)
    db.session.add(company)
    db.session.commit()
    return company

def update_company(company_id, data):
    company = StockCompany.query.get(company_id)
    if not company:
        return None
    for key, value in data.items():
        setattr(company, key, value)
    db.session.commit()
    return company

def delete_company(company_id):
    company = StockCompany.query.get(company_id)
    if not company:
        return False
    db.session.delete(company)
    db.session.commit()
    return True