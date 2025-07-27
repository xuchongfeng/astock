from flask import Blueprint, request, jsonify
from app.services.stock_daily_service import (
    get_all_daily, get_daily_by_id, create_daily, update_daily, delete_daily,
    calc_n_day_pct_chg
)
from sqlalchemy import desc, asc
from app.models.stock_daily import StockDaily
from app.models.stock_company import StockCompany
from datetime import datetime

bp = Blueprint('stock_daily', __name__, url_prefix='/api/stock_daily')

@bp.route('/', methods=['GET'])
def list_daily():
    # 支持通过查询参数过滤，如 ts_code, start_date, end_date
    filters = {}
    for key in ['ts_code', 'trade_date']:
        value = request.args.get(key)
        if value:
            filters[key] = value
    
    # 日期范围过滤
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    sort_fields = request.args.get('sort_fields')
    
    # 如果提供了日期范围，计算日期差作为page_size
    if start_date and end_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            date_diff = (end_dt - start_dt).days + 1
            page_size = max(date_diff, 1)  # 确保至少为1
        except ValueError:
            # 如果日期格式错误，使用默认page_size
            pass
    
    query = get_all_daily(filters if filters else None, query_only=True)
    
    # 添加日期范围过滤
    if start_date:
        query = query.filter(StockDaily.trade_date >= start_date)
    if end_date:
        query = query.filter(StockDaily.trade_date <= end_date)
    
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
    
    # 获取股票名称并添加到返回数据中
    result_data = []
    user_id = 1
    for item in items:
        item_dict = item.as_dict()
        # 查询对应的股票名称
        company = StockCompany.query.filter_by(ts_code=item.ts_code).first()
        if company:
            item_dict['stock_name'] = company.name
        else:
            item_dict['stock_name'] = None
        # 计算涨幅
        try:
            trade_date = item.trade_date if isinstance(item.trade_date, datetime) else datetime.strptime(str(item.trade_date), '%Y-%m-%d')
        except Exception:
            trade_date = None
        if trade_date:
            for n in [3, 5, 15, 30, 60]:
                pct = calc_n_day_pct_chg(item.ts_code, trade_date, n)
                item_dict[f'pct_chg_{n}d'] = pct
        # 增加user_stock的rating
        if user_id:
            from app.models.user_stock import UserStock
            user_stock = UserStock.query.filter_by(user_id=user_id, ts_code=item.ts_code).first()
            item_dict['rating'] = user_stock.rating if user_stock else None
        result_data.append(item_dict)
    
    return jsonify({
        'data': result_data,
        'total': total
    })

@bp.route('/<int:daily_id>', methods=['GET'])
def get_daily(daily_id):
    daily = get_daily_by_id(daily_id)
    if not daily:
        return jsonify({'error': 'Not found'}), 404
    
    # 获取股票名称
    result_dict = daily.as_dict()
    company = StockCompany.query.filter_by(ts_code=daily.ts_code).first()
    if company:
        result_dict['stock_name'] = company.name
    else:
        result_dict['stock_name'] = None
    
    return jsonify(result_dict)

@bp.route('/', methods=['POST'])
def add_daily():
    data = request.json
    daily = create_daily(data)
    return jsonify(daily.as_dict()), 201

@bp.route('/<int:daily_id>', methods=['PUT'])
def edit_daily(daily_id):
    data = request.json
    daily = update_daily(daily_id, data)
    if not daily:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(daily.as_dict())

@bp.route('/<int:daily_id>', methods=['DELETE'])
def remove_daily(daily_id):
    success = delete_daily(daily_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 