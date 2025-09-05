from flask import Blueprint, request, jsonify
from app.services.ths_member_service import (
    get_all_ths_member, 
    get_ths_member_by_id, 
    create_ths_member, 
    update_ths_member, 
    delete_ths_member,
    get_ths_member_with_daily_data
)
from app import db
from datetime import datetime
from sqlalchemy import desc, asc

bp = Blueprint('ths_member', __name__, url_prefix='/api/ths_member')

@bp.route('/', methods=['GET'])
def list_ths_member():
    filters = {}
    for key in ['ts_code', 'con_code', 'is_new']:
        value = request.args.get(key)
        if value is not None:
            filters[key] = value
    
    # 获取trade_date参数
    trade_date_str = request.args.get('trade_date')
    trade_date = None
    if trade_date_str:
        try:
            trade_date = datetime.strptime(trade_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid trade_date format. Expected YYYY-MM-DD format.'}), 400
    
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 20))
    sort_fields = request.args.get('sortFields')
    
    # 如果有trade_date参数，使用新的服务函数获取带涨幅的数据
    if trade_date:
        query = get_ths_member_with_daily_data(filters if filters else None, trade_date, query_only=True)
        total = query.count()
        
        # 应用分页
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        
        # 格式化返回数据
        result_data = []
        for item in items:
            # item是一个元组，包含ThsMember对象和StockDaily字段
            member = item[0]  # ThsMember对象
            member_dict = member.as_dict()
            
            # 添加涨幅相关字段
            member_dict['pct_chg'] = float(item[1]) if item[1] is not None else None
            member_dict['change'] = float(item[2]) if item[2] is not None else None
            member_dict['close'] = float(item[3]) if item[3] is not None else None
            member_dict['pre_close'] = float(item[4]) if item[4] is not None else None
            member_dict['vol'] = int(item[5]) if item[5] is not None else None
            member_dict['amount'] = float(item[6]) if item[6] is not None else None
            member_dict['turnover_rate'] = float(item[7]) if item[7] is not None else None
            
            result_data.append(member_dict)
        
        return jsonify({
            'data': result_data,
            'total': total,
            'trade_date': trade_date_str
        })
    else:
        # 原有的逻辑，不包含涨幅信息
        query = get_all_ths_member(filters if filters else None, query_only=True)
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

@bp.route('/<int:member_id>', methods=['GET'])
def get_ths_member(member_id):
    member = get_ths_member_by_id(member_id)
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    return jsonify(member.as_dict())

@bp.route('/', methods=['POST'])
def create_member():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        member = create_ths_member(data)
        return jsonify(member.as_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    member = update_ths_member(member_id, data)
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    
    return jsonify(member.as_dict())

@bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    success = delete_ths_member(member_id)
    if not success:
        return jsonify({'error': 'Member not found'}), 404
    
    return jsonify({'message': 'Member deleted successfully'})