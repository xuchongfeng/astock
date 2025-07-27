from flask import Blueprint, request, jsonify
from app.services.ths_index_daily_service import (
    get_all_ths_index_daily, get_ths_index_daily_by_id, create_ths_index_daily,
    update_ths_index_daily, delete_ths_index_daily
)
from sqlalchemy import desc, asc
from app.models.ths_index_daily import ThsIndexDaily

bp = Blueprint('ths_index_daily', __name__, url_prefix='/api/ths_index_daily')

@bp.route('/', methods=['GET'])
def list_ths_index_daily():
    filters = {}
    for key in ['ts_code', 'trade_date']:
        value = request.args.get(key)
        if value:
            filters[key] = value
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    sort_fields = request.args.get('sort_fields')
    query = get_all_ths_index_daily(filters if filters else None, query_only=True)
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

@bp.route('/<int:daily_id>', methods=['GET'])
def get_ths_index_daily(daily_id):
    daily = get_ths_index_daily_by_id(daily_id)
    if not daily:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(daily.as_dict())

@bp.route('/', methods=['POST'])
def add_ths_index_daily():
    data = request.json
    daily = create_ths_index_daily(data)
    return jsonify(daily.as_dict()), 201

@bp.route('/<int:daily_id>', methods=['PUT'])
def edit_ths_index_daily(daily_id):
    data = request.json
    daily = update_ths_index_daily(daily_id, data)
    if not daily:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(daily.as_dict())

@bp.route('/<int:daily_id>', methods=['DELETE'])
def remove_ths_index_daily(daily_id):
    success = delete_ths_index_daily(daily_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'})