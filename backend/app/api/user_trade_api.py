from flask import Blueprint, request, jsonify
from app.services.user_trade_service import (
    get_all_trades, get_trade_by_id, create_trade, update_trade, delete_trade
)
from app.models.stock_company import StockCompany

bp = Blueprint('user_trade', __name__, url_prefix='/api/user_trade')

@bp.route('/<int:user_id>', methods=['GET'])
def list_trades(user_id):
    filters = {'user_id': user_id}
    for key in ['ts_code', 'trade_type', 'trade_date']:
        value = request.args.get(key)
        if value:
            filters[key] = value
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    query = get_all_trades(filters, query_only=True)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    result = []
    for i in items:
        d = i.as_dict()
        company = StockCompany.query.filter_by(ts_code=i.ts_code).first()
        d['stock_info'] = company.as_dict() if company else None
        result.append(d)
    return jsonify({'data': result, 'total': total})

@bp.route('/<int:user_id>/<int:trade_id>', methods=['GET'])
def get_trade(user_id, trade_id):
    trade = get_trade_by_id(trade_id)
    if not trade or trade.user_id != user_id:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(trade.as_dict())

@bp.route('/<int:user_id>', methods=['POST'])
def add_trade(user_id):
    data = request.json
    data['user_id'] = user_id
    trade = create_trade(data)
    return jsonify(trade.as_dict()), 201

@bp.route('/<int:user_id>/<int:trade_id>', methods=['PUT'])
def edit_trade(user_id, trade_id):
    trade = get_trade_by_id(trade_id)
    if not trade or trade.user_id != user_id:
        return jsonify({'error': 'Not found'}), 404
    data = request.json
    trade = update_trade(trade_id, data)
    if not trade:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(trade.as_dict())

@bp.route('/<int:user_id>/<int:trade_id>', methods=['DELETE'])
def remove_trade(user_id, trade_id):
    trade = get_trade_by_id(trade_id)
    if not trade or trade.user_id != user_id:
        return jsonify({'error': 'Not found'}), 404
    success = delete_trade(trade_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 