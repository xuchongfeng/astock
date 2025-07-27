from app.models.ths_member import ThsMember
from app import db

def get_all_ths_member(filters=None, query_only=False):
    query = ThsMember.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(ThsMember, attr) == value)
    if query_only:
        return query
    return query.all()

def get_ths_member_by_id(member_id):
    return ThsMember.query.get(member_id)

def create_ths_member(data):
    member = ThsMember(**data)
    db.session.add(member)
    db.session.commit()
    return member

def update_ths_member(member_id, data):
    member = ThsMember.query.get(member_id)
    if not member:
        return None
    for key, value in data.items():
        setattr(member, key, value)
    db.session.commit()
    return member

def delete_ths_member(member_id):
    member = ThsMember.query.get(member_id)
    if not member:
        return False
    db.session.delete(member)
    db.session.commit()
    return True