from app.models.ths_index import ThsIndex
from app import db

def get_all_ths_index(query_only=False):
    query = ThsIndex.query
    if query_only:
        return query
    return query.all()

def get_ths_index_by_id(idx_id):
    return ThsIndex.query.get(idx_id)

def create_ths_index(data):
    ths_index = ThsIndex(**data)
    db.session.add(ths_index)
    db.session.commit()
    return ths_index

def update_ths_index(idx_id, data):
    ths_index = ThsIndex.query.get(idx_id)
    if not ths_index:
        return None
    for key, value in data.items():
        setattr(ths_index, key, value)
    db.session.commit()
    return ths_index

def delete_ths_index(idx_id):
    ths_index = ThsIndex.query.get(idx_id)
    if not ths_index:
        return False
    db.session.delete(ths_index)
    db.session.commit()
    return True 