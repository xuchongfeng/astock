from flask import Blueprint, request, jsonify
from app.services.industry_stats_service import (
    get_all_industry_stats, get_industry_stats_by_id, create_industry_stats, update_industry_stats, delete_industry_stats
)
from sqlalchemy import desc, asc
from app.models.industry_stats import IndustryStats
from datetime import datetime

bp = Blueprint('industry_stats', __name__, url_prefix='/api/industry_stats')

@bp.route('/', methods=['GET'])
def list_industry_stats():
    filters = {}
    for key in ['industry_id', 'stat_date']:
        value = request.args.get(key)
        if value is not None:
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
    
    query = get_all_industry_stats(filters if filters else None, query_only=True)
    
    # 添加日期范围过滤
    if start_date:
        query = query.filter(IndustryStats.stat_date >= start_date)
    if end_date:
        query = query.filter(IndustryStats.stat_date <= end_date)
    
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
        'data': [s.as_dict() for s in items],
        'total': total
    })

@bp.route('/<int:stats_id>', methods=['GET'])
def get_stats(stats_id):
    stats = get_industry_stats_by_id(stats_id)
    if not stats:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(stats.as_dict())

@bp.route('/', methods=['POST'])
def add_stats():
    data = request.json
    stats = create_industry_stats(data)
    return jsonify(stats.as_dict()), 201

@bp.route('/<int:stats_id>', methods=['PUT'])
def edit_stats(stats_id):
    data = request.json
    stats = update_industry_stats(stats_id, data)
    if not stats:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(stats.as_dict())

@bp.route('/<int:stats_id>', methods=['DELETE'])
def remove_stats(stats_id):
    success = delete_industry_stats(stats_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 