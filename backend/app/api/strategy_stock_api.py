from flask import Blueprint, request, jsonify
from app.services.strategy_stock_service import (
    get_all_strategy_stocks, get_strategy_stock_by_id, create_strategy_stock, update_strategy_stock, delete_strategy_stock
)
from app.models.stock_company import StockCompany
from app.models.strategy_stock import StrategyStock

bp = Blueprint('strategy_stock', __name__, url_prefix='/api/strategy_stock')

@bp.route('/', methods=['GET'])
def list_strategy_stocks():
    filters = {}
    for key in ['strategy_id', 'ts_code', 'date']:
        value = request.args.get(key)
        if value:
            filters[key] = value
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    sort_field = request.args.get('sort_field')
    query = get_all_strategy_stocks(filters if filters else None, query_only=True)
    total = query.count()
    # 支持sort_field=-avg_amount_5d、rating等
    if sort_field:
        desc = False
        field = sort_field
        if sort_field.startswith('-'):
            desc = True
            field = sort_field[1:]
        if field == 'avg_amount_5d':
            if desc:
                query = query.order_by(StrategyStock.avg_amount_5d.desc())
            else:
                query = query.order_by(StrategyStock.avg_amount_5d.asc())
        elif field == 'rating':
            if desc:
                query = query.order_by(StrategyStock.rating.desc())
            else:
                query = query.order_by(StrategyStock.rating.asc())
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    result = []
    for i in items:
        d = i.as_dict()
        company = StockCompany.query.filter_by(ts_code=i.ts_code).first()
        d['stock_info'] = company.as_dict() if company else None
        result.append(d)
    return jsonify({'data': result, 'total': total})

@bp.route('/<int:stock_id>', methods=['GET'])
def get_strategy_stock(stock_id):
    stock = get_strategy_stock_by_id(stock_id)
    if not stock:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(stock.as_dict())

@bp.route('/', methods=['POST'])
def add_strategy_stock():
    data = request.json
    stock = create_strategy_stock(data)
    return jsonify(stock.as_dict()), 201

@bp.route('/<int:stock_id>', methods=['PUT'])
def edit_strategy_stock(stock_id):
    data = request.json
    stock = update_strategy_stock(stock_id, data)
    if not stock:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(stock.as_dict())

@bp.route('/<int:stock_id>', methods=['DELETE'])
def remove_strategy_stock(stock_id):
    success = delete_strategy_stock(stock_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 