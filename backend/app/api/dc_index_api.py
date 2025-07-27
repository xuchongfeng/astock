from flask import Blueprint, request, jsonify
from app.services.dc_index_service import (
    get_all_dc_index, get_dc_index_by_id, create_dc_index, update_dc_index, delete_dc_index
)
from sqlalchemy import desc, asc

bp = Blueprint('dc_index', __name__, url_prefix='/api/dc_index')

@bp.route('/', methods=['GET'])
def list_dc_index():
    filters = {}
    for key in ['ts_code', 'name']:
        value = request.args.get(key)
        if value is not None:
            filters[key] = value
    
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 20))
    sort_fields = request.args.get('sortFields')
    
    query = get_all_dc_index(filters if filters else None, query_only=True)
    
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
def get_dc_index(idx_id):
    dc_index = get_dc_index_by_id(idx_id)
    if not dc_index:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(dc_index.as_dict())

@bp.route('/', methods=['POST'])
def add_dc_index():
    data = request.json
    dc_index = create_dc_index(data)
    return jsonify(dc_index.as_dict()), 201

@bp.route('/<int:idx_id>', methods=['PUT'])
def edit_dc_index(idx_id):
    data = request.json
    dc_index = update_dc_index(idx_id, data)
    if not dc_index:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(dc_index.as_dict())

@bp.route('/<int:idx_id>', methods=['DELETE'])
def remove_dc_index(idx_id):
    success = delete_dc_index(idx_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 