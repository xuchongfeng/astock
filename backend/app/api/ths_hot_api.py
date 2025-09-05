from flask import Blueprint, request, jsonify
from app.services.ths_hot_service import *
from app.models.ths_hot import ThsHot
from datetime import datetime
from sqlalchemy import desc, asc

bp = Blueprint('ths_hot', __name__, url_prefix='/api/ths_hot')

@bp.route('/', methods=['GET'])
def list_hot_data():
    """获取热榜数据列表"""
    # 获取查询参数
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 20))
    sort_fields = request.args.get('sortFields')
    
    # 过滤参数
    filters = {}
    for key in ['trade_date', 'ts_code', 'data_type']:
        value = request.args.get(key)
        if value:
            filters[key] = value
    
    # 日期范围过滤
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date:
        try:
            filters['start_date'] = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    if end_date:
        try:
            filters['end_date'] = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    # 搜索过滤
    search = request.args.get('search')
    if search:
        filters['search'] = search
    
    # 获取查询对象
    query = get_all_hot_data(filters, query_only=True)
    
    # 排序
    if sort_fields:
        for field in sort_fields.split(','):
            field = field.strip()
            if not field:
                continue
            if field.startswith('-'):
                query = query.order_by(desc(field[1:]))
            else:
                query = query.order_by(asc(field))
    else:
        # 默认按日期和排行排序
        query = query.order_by(desc(ThsHot.trade_date), asc(ThsHot.rank))
    
    # 分页
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return jsonify({
        'data': [item.as_dict() for item in items],
        'total': total,
        'page': page,
        'pageSize': page_size
    })

@bp.route('/<int:hot_id>', methods=['GET'])
def get_hot_data(hot_id):
    """根据ID获取热榜数据"""
    hot_data = get_hot_data_by_id(hot_id)
    if not hot_data:
        return jsonify({'error': '热榜数据不存在'}), 404
    
    return jsonify(hot_data.as_dict())

@bp.route('/', methods=['POST'])
def create_hot_data_api():
    """创建热榜数据"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['trade_date', 'data_type', 'ts_code', 'ts_name', 'rank']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'字段 {field} 不能为空'}), 400
        
        # 转换日期格式
        if isinstance(data['trade_date'], str):
            try:
                data['trade_date'] = datetime.strptime(data['trade_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': '日期格式错误，应为 YYYY-MM-DD'}), 400
        
        hot_data = create_hot_data(data)
        return jsonify(hot_data.as_dict()), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:hot_id>', methods=['PUT'])
def update_hot_data_api(hot_id):
    """更新热榜数据"""
    try:
        data = request.get_json()
        
        # 移除不允许更新的字段
        if 'id' in data:
            del data['id']
        if 'created_at' in data:
            del data['created_at']
        
        # 转换日期格式
        if 'trade_date' in data and isinstance(data['trade_date'], str):
            try:
                data['trade_date'] = datetime.strptime(data['trade_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': '日期格式错误，应为 YYYY-MM-DD'}), 400
        
        hot_data = update_hot_data(hot_id, data)
        if not hot_data:
            return jsonify({'error': '热榜数据不存在'}), 404
        
        return jsonify(hot_data.as_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:hot_id>', methods=['DELETE'])
def delete_hot_data_api(hot_id):
    """删除热榜数据"""
    try:
        success = delete_hot_data(hot_id)
        if not success:
            return jsonify({'error': '热榜数据不存在'}), 404
        
        return jsonify({'message': '删除成功'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/latest', methods=['GET'])
def get_latest_hot_data_api():
    """获取最新热榜数据"""
    data_type = request.args.get('data_type')
    limit = int(request.args.get('limit', 100))
    
    hot_data_list = get_latest_hot_data(data_type, limit)
    
    return jsonify({
        'data': [item.as_dict() for item in hot_data_list],
        'count': len(hot_data_list)
    })

@bp.route('/by-date-type', methods=['GET'])
def get_hot_data_by_date_type_api():
    """根据日期和数据类型获取热榜数据"""
    trade_date = request.args.get('trade_date')
    data_type = request.args.get('data_type')
    
    if not trade_date or not data_type:
        return jsonify({'error': 'trade_date 和 data_type 参数不能为空'}), 400
    
    try:
        trade_date = datetime.strptime(trade_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': '日期格式错误，应为 YYYY-MM-DD'}), 400
    
    hot_data_list = get_hot_data_by_date_and_type(trade_date, data_type)
    
    return jsonify({
        'data': [item.as_dict() for item in hot_data_list],
        'count': len(hot_data_list),
        'trade_date': trade_date.strftime('%Y-%m-%d'),
        'data_type': data_type
    })

@bp.route('/by-ts-code/<ts_code>', methods=['GET'])
def get_hot_data_by_ts_code_api(ts_code):
    """根据股票代码获取热榜历史数据"""
    limit = int(request.args.get('limit', 50))
    
    hot_data_list = get_hot_data_by_ts_code(ts_code, limit)
    
    return jsonify({
        'data': [item.as_dict() for item in hot_data_list],
        'count': len(hot_data_list),
        'ts_code': ts_code
    })

@bp.route('/statistics', methods=['GET'])
def get_hot_data_statistics_api():
    """获取热榜数据统计信息"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # 转换日期格式
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'start_date 格式错误，应为 YYYY-MM-DD'}), 400
    
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'end_date 格式错误，应为 YYYY-MM-DD'}), 400
    
    statistics = get_hot_data_statistics(start_date, end_date)
    
    return jsonify(statistics)

@bp.route('/types', methods=['GET'])
def get_data_types():
    """获取所有数据类型"""
    types = db.session.query(ThsHot.data_type).distinct().all()
    return jsonify({
        'data_types': [t[0] for t in types if t[0]]
    }) 