from flask import Blueprint, request, jsonify
from app.services.user_stock_service import (
    get_user_stocks, get_user_stock_by_id, get_user_stock_by_user_and_code,
    create_user_stock, update_user_stock, delete_user_stock, delete_user_stock_by_user_and_code,
    delete_user_stock_by_user_and_id
)
from app.services.stock_company_service import get_company_by_ts_code
from app.services.stock_daily_service import calc_n_day_pct_chg
from datetime import datetime
from app.models.stock_daily import StockDaily
from app.models.ths_index_daily import ThsIndexDaily
from app import db
from sqlalchemy import desc, asc

bp = Blueprint('user_stock', __name__, url_prefix='/api/user_stock')

@bp.route('/<int:user_id>', methods=['GET'])
def list_user_stocks(user_id):
    sort_field = request.args.get('sort_field')
    user_stocks = get_user_stocks(user_id)
    # 支持按rating和created_at排序
    if sort_field:
        desc = False
        field = sort_field
        if sort_field.startswith('-'):
            desc = True
            field = sort_field[1:]
        if field == 'rating':
            user_stocks = sorted(user_stocks, key=lambda x: (x.rating is None, x.rating), reverse=desc)
        elif field == 'created_at':
            user_stocks = sorted(user_stocks, key=lambda x: (x.created_at is None, x.created_at), reverse=desc)
    result = []
    for s in user_stocks:
        stock_info = get_company_by_ts_code(s.ts_code)
        stock_dict = stock_info.as_dict() if stock_info else {}
        # 获取user_stock的rating字段
        stock_dict['rating'] = s.rating
        # 获取最新一条日线数据的trade_date
        latest_daily = StockDaily.query.filter_by(ts_code=s.ts_code).order_by(StockDaily.trade_date.desc()).first()
        if latest_daily:
            trade_date = latest_daily.trade_date if isinstance(latest_daily.trade_date, datetime) else datetime.strptime(str(latest_daily.trade_date), '%Y-%m-%d')
            for n in [3, 5, 15, 30, 60]:
                pct = calc_n_day_pct_chg(s.ts_code, trade_date, n)
                stock_dict[f'pct_chg_{n}d'] = pct
        result.append(stock_dict)
    return jsonify(result)

@bp.route('/<int:user_id>/<path:stock_code>', methods=['GET'])
def get_user_stock(user_id, stock_code):
    user_stock = get_user_stock_by_user_and_code(user_id, stock_code)
    if not user_stock:
        return jsonify("{}")
    return jsonify(user_stock.as_dict())

@bp.route('/', methods=['POST'])
def add_user_stock():
    data = request.json
    user_stock = create_user_stock(data)
    return jsonify(user_stock.as_dict()), 201

@bp.route('/<int:stock_id>', methods=['PUT'])
def edit_user_stock(stock_id):
    data = request.json
    user_stock = update_user_stock(stock_id, data)
    if not user_stock:
        return jsonify("{}")
    return jsonify(user_stock.as_dict())

@bp.route('/<int:user_id>/<path:stock_code>/rating', methods=['PUT'])
def update_user_stock_rating(user_id, stock_code):
    data = request.json
    rating = data.get('rating')
    if rating is None:
        return jsonify({'error': 'Missing rating'}), 400
    user_stock = get_user_stock_by_user_and_code(user_id, stock_code)
    from app import db
    if not user_stock:
        # 新增记录
        user_stock = create_user_stock({'user_id': user_id, 'ts_code': stock_code, 'rating': rating})
        db.session.commit()
        return jsonify({'result': 'created', 'rating': user_stock.rating})
    else:
        user_stock.rating = rating
        db.session.commit()
        return jsonify({'result': 'success', 'rating': user_stock.rating})

@bp.route('/<int:user_id>/<path:stock_code>', methods=['DELETE'])
def remove_user_stock(user_id, stock_code):
    success = delete_user_stock_by_user_and_code(user_id, stock_code)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 
