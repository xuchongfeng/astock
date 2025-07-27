from flask import Blueprint, request, jsonify
from app.services.strategy_service import (
    get_all_strategies, get_strategy_by_id, create_strategy, update_strategy, delete_strategy
)

bp = Blueprint('strategy', __name__, url_prefix='/api/strategy')

@bp.route('/', methods=['GET'])
def list_strategies():
    filters = {}
    for key in ['name']:
        value = request.args.get(key)
        if value:
            filters[key] = value
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    query = get_all_strategies(filters if filters else None, query_only=True)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return jsonify({'data': [i.as_dict() for i in items], 'total': total})

@bp.route('/<int:strategy_id>', methods=['GET'])
def get_strategy(strategy_id):
    strategy = get_strategy_by_id(strategy_id)
    if not strategy:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(strategy.as_dict())

@bp.route('/', methods=['POST'])
def add_strategy():
    data = request.json
    strategy = create_strategy(data)
    return jsonify(strategy.as_dict()), 201

@bp.route('/<int:strategy_id>', methods=['PUT'])
def edit_strategy(strategy_id):
    data = request.json
    strategy = update_strategy(strategy_id, data)
    if not strategy:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(strategy.as_dict())

@bp.route('/<int:strategy_id>', methods=['DELETE'])
def remove_strategy(strategy_id):
    success = delete_strategy(strategy_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 