from flask import Blueprint, request, jsonify
from app.services.user_position_service import (
    get_all_positions, get_position_by_id, create_position, update_position, delete_position
)
from app.models.stock_company import StockCompany

bp = Blueprint('user_position', __name__, url_prefix='/api/user_position')

@bp.route('/<int:user_id>', methods=['GET'])
def list_positions(user_id):
    filters = {'user_id': user_id}
    ts_code = request.args.get('ts_code')
    if ts_code:
        filters['ts_code'] = ts_code
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    query = get_all_positions(filters, query_only=True)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    result = []
    for i in items:
        d = i.as_dict()
        company = StockCompany.query.filter_by(ts_code=i.ts_code).first()
        d['stock_info'] = company.as_dict() if company else None
        result.append(d)
    return jsonify({'data': result, 'total': total})

@bp.route('/<int:user_id>/<int:position_id>', methods=['GET'])
def get_position(user_id, position_id):
    position = get_position_by_id(position_id)
    if not position or position.user_id != user_id:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(position.as_dict())

@bp.route('/<int:user_id>', methods=['POST'])
def add_position(user_id):
    data = request.json
    data['user_id'] = user_id
    position = create_position(data)
    return jsonify(position.as_dict()), 201

@bp.route('/<int:user_id>/<int:position_id>', methods=['PUT'])
def edit_position(user_id, position_id):
    position = get_position_by_id(position_id)
    if not position or position.user_id != user_id:
        return jsonify({'error': 'Not found'}), 404
    data = request.json
    position = update_position(position_id, data)
    if not position:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(position.as_dict())

@bp.route('/<int:user_id>/<int:position_id>', methods=['DELETE'])
def remove_position(user_id, position_id):
    position = get_position_by_id(position_id)
    if not position or position.user_id != user_id:
        return jsonify({'error': 'Not found'}), 404
    success = delete_position(position_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 