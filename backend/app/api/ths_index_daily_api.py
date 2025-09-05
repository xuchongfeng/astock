from flask import Blueprint, request, jsonify
from app.services.ths_index_daily_service import (
    get_all_ths_index_daily, get_ths_index_daily_by_id, create_ths_index_daily,
    update_ths_index_daily, delete_ths_index_daily, get_all_ths_index_daily_with_name
)
from sqlalchemy import desc, asc
from app.models.ths_index_daily import ThsIndexDaily
from datetime import datetime

bp = Blueprint('ths_index_daily', __name__, url_prefix='/api/ths_index_daily')

@bp.route('/', methods=['GET'])
def list_ths_index_daily():
    filters = {}
    for key in ['ts_code', 'trade_date']:
        value = request.args.get(key)
        if value:
            # 处理日期参数，将YYYY-MM-DD格式转换为date对象
            if key == 'trade_date':
                try:
                    # 尝试解析YYYY-MM-DD格式的日期
                    date_obj = datetime.strptime(value, '%Y-%m-%d').date()
                    filters[key] = date_obj
                except ValueError:
                    # 如果解析失败，返回错误信息
                    return jsonify({'error': f'Invalid date format for {key}. Expected YYYY-MM-DD format.'}), 400
            else:
                filters[key] = value
    
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    sort_fields = request.args.get('sort_fields')
    
    # 使用新的服务方法获取包含指数名称的数据
    query = get_all_ths_index_daily_with_name(filters if filters else None, query_only=True)
    total = query.count()
    
    if sort_fields:
        for field in sort_fields.split(','):
            field = field.strip()
            if not field:
                continue
            if field.startswith('-'):
                # 降序排序
                field_name = field[1:]
                if field_name in ['ts_code', 'trade_date', 'close', 'open', 'high', 'low', 'pre_close', 'avg_price', 'change', 'pct_change', 'vol', 'turnover_rate', 'total_mv', 'float_mv']:
                    query = query.order_by(desc(getattr(ThsIndexDaily, field_name)))
                else:
                    query = query.order_by(desc(field_name))
            else:
                # 升序排序
                if field in ['ts_code', 'trade_date', 'close', 'open', 'high', 'low', 'pre_close', 'avg_price', 'change', 'pct_change', 'vol', 'turnover_rate', 'total_mv', 'float_mv']:
                    query = query.order_by(asc(getattr(ThsIndexDaily, field)))
                else:
                    query = query.order_by(asc(field))
    
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # 格式化返回数据，包含指数名称
    result_data = []
    for i, item in enumerate(items):
        daily_data = item[0].as_dict()  # ThsIndexDaily 数据
        index_name = item[1]  # 指数名称
        daily_data['name'] = index_name  # 指数名称
        
        result_data.append(daily_data)
    
    return jsonify({
        'data': result_data,
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