from flask import Blueprint, request, jsonify, make_response
from app.services.stock_note_service import (
    get_all_notes, get_note_by_id, create_note, update_note, delete_note
)

bp = Blueprint('stock_note', __name__, url_prefix='/api/stock_note')

@bp.route('/', methods=['GET'])
def list_notes():
    filters = {}
    for key in ['ts_code', 'note_date']:
        value = request.args.get(key)
        if value:
            filters[key] = value
    notes = get_all_notes(filters if filters else None)
    return jsonify([n.as_dict() for n in notes])

@bp.route('/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = get_note_by_id(note_id)
    if not note:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(note.as_dict())

@bp.route('/', methods=['POST'])
def add_note():
    data = request.json
    note = create_note(data)
    return jsonify(note.as_dict()), 201

@bp.route('/<int:note_id>', methods=['PUT'])
def edit_note(note_id):
    data = request.json
    note = update_note(note_id, data)
    if not note:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(note.as_dict())

@bp.route('/<int:note_id>', methods=['DELETE'])
def remove_note(note_id):
    success = delete_note(note_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 