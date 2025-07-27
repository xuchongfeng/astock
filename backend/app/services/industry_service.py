from app.models.industry import Industry
from app import db

def get_all_industries(query_only=False):
    query = Industry.query
    if query_only:
        return query
    return query.all()

def get_industry_by_id(industry_id):
    return Industry.query.get(industry_id)

def create_industry(data):
    industry = Industry(**data)
    db.session.add(industry)
    db.session.commit()
    return industry

def update_industry(industry_id, data):
    industry = Industry.query.get(industry_id)
    if not industry:
        return None
    for key, value in data.items():
        setattr(industry, key, value)
    db.session.commit()
    return industry

def delete_industry(industry_id):
    industry = Industry.query.get(industry_id)
    if not industry:
        return False
    db.session.delete(industry)
    db.session.commit()
    return True 