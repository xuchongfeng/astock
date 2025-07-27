from app.models.stock_note import StockNote
from app import db

def get_all_notes(filters=None, query_only=False):
    query = StockNote.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(StockNote, attr) == value)
    if query_only:
        return query
    return query.all()

def get_note_by_id(note_id):
    return StockNote.query.get(note_id)

def create_note(data):
    note = StockNote(**data)
    db.session.add(note)
    db.session.commit()
    return note

def update_note(note_id, data):
    note = StockNote.query.get(note_id)
    if not note:
        return None
    for key, value in data.items():
        setattr(note, key, value)
    db.session.commit()
    return note

def delete_note(note_id):
    note = StockNote.query.get(note_id)
    if not note:
        return False
    db.session.delete(note)
    db.session.commit()
    return True 