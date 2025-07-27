from flask import Blueprint, request, jsonify
from app.services.ths_member_service import (
    get_all_ths_member, get_ths_member_by_id, create_ths_member, update_ths_member, delete_ths_member
)
from sqlalchemy import desc, asc

bp = Blueprint('ths_member', __name__, url_prefix='/api/ths_member')

@bp.route('/', methods=['GET'])
def list_ths_member():
    filters = {}
    for key in ['ts_code', 'con_code', 'is_new']:
        value = request.args.get(key)
        if value is not None:
            filters[key] = value
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 20))
    sort_fields = request.args.get('sortFields')
    query = get_all_ths_member(filters if filters else None, query_only=True)
    total = query.count()
    if sort_fields:
        for field in sort_fields.split(','):
            field = field.strip()
            if not field:
                continue
            if field.startswith('-'):
                query = query.order_by(desc(field[1:]))
            else:
                query = query.order_by(asc(field))
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return jsonify({
        'data': [i.as_dict() for i in items],
        'total': total
    })

@bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = get_ths_member_by_id(member_id)
    if not member:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(member.as_dict())

@bp.route('/', methods=['POST'])
def add_member():
    data = request.json
    member = create_ths_member(data)
    return jsonify(member.as_dict()), 201

@bp.route('/<int:member_id>', methods=['PUT'])
def edit_member(member_id):
    data = request.json
    member = update_ths_member(member_id, data)
    if not member:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(member.as_dict())

@bp.route('/<int:member_id>', methods=['DELETE'])
def remove_member(member_id):
    success = delete_ths_member(member_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'})