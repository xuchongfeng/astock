from flask import Blueprint, request, jsonify
from app.services.ths_index_service import (
    get_all_ths_index, get_ths_index_by_id, create_ths_index, update_ths_index, delete_ths_index
)
from sqlalchemy import desc, asc

bp = Blueprint('ths_index', __name__, url_prefix='/api/ths_index')

@bp.route('/', methods=['GET'])
def list_ths_index():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 20))
    sort_fields = request.args.get('sortFields')
    query = get_all_ths_index(query_only=True)
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

@bp.route('/<int:idx_id>', methods=['GET'])
def get_ths_index(idx_id):
    ths_index = get_ths_index_by_id(idx_id)
    if not ths_index:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(ths_index.as_dict())

@bp.route('/', methods=['POST'])
def add_ths_index():
    data = request.json
    ths_index = create_ths_index(data)
    return jsonify(ths_index.as_dict()), 201

@bp.route('/<int:idx_id>', methods=['PUT'])
def edit_ths_index(idx_id):
    data = request.json
    ths_index = update_ths_index(idx_id, data)
    if not ths_index:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(ths_index.as_dict())

@bp.route('/<int:idx_id>', methods=['DELETE'])
def remove_ths_index(idx_id):
    success = delete_ths_index(idx_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 