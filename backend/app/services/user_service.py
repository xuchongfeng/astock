from app.models.user import User
from app import db

def get_all_users(query_only=False):
    query = User.query
    if query_only:
        return query
    return query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def create_user(data):
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return None
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True 