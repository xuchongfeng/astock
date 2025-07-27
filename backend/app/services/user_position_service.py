from app.models.user_position import UserPosition
from app import db

def get_all_positions(filters=None, query_only=False):
    query = UserPosition.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(UserPosition, attr) == value)
    if query_only:
        return query
    return query.all()

def get_position_by_id(position_id):
    return UserPosition.query.get(position_id)

def create_position(data):
    position = UserPosition(**data)
    db.session.add(position)
    db.session.commit()
    return position

def update_position(position_id, data):
    position = UserPosition.query.get(position_id)
    if not position:
        return None
    for key, value in data.items():
        setattr(position, key, value)
    db.session.commit()
    return position

def delete_position(position_id):
    position = UserPosition.query.get(position_id)
    if not position:
        return False
    db.session.delete(position)
    db.session.commit()
    return True 