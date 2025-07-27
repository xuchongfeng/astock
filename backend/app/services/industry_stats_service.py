from app.models.industry_stats import IndustryStats
from app import db

def get_all_industry_stats(filters=None, query_only=False):
    query = IndustryStats.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(IndustryStats, attr) == value)
    if query_only:
        return query
    return query.all()

def get_industry_stats_by_id(stats_id):
    return IndustryStats.query.get(stats_id)

def create_industry_stats(data):
    stats = IndustryStats(**data)
    db.session.add(stats)
    db.session.commit()
    return stats

def update_industry_stats(stats_id, data):
    stats = IndustryStats.query.get(stats_id)
    if not stats:
        return None
    for key, value in data.items():
        setattr(stats, key, value)
    db.session.commit()
    return stats

def delete_industry_stats(stats_id):
    stats = IndustryStats.query.get(stats_id)
    if not stats:
        return False
    db.session.delete(stats)
    db.session.commit()
    return True 