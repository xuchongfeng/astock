from flask import Blueprint, request, jsonify
from app.services.stock_company_service import (
    get_all_companies, get_company_by_id, create_company, update_company, delete_company
)
from sqlalchemy import desc, asc, or_
from app.models.stock_company import StockCompany

bp = Blueprint('stock_company', __name__, url_prefix='/api/stock_company')

@bp.route('/', methods=['GET'])
def list_companies():
    # 解析分页和排序参数
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    sort_fields = request.args.get('sort_fields')  # 例："name,-id"
    search = request.args.get('search')  # 搜索关键词，支持name和ts_code

    query = get_all_companies(query_only=True)
    
    # 搜索功能：支持name和ts_code模糊搜索
    if search:
        query = query.filter(
            or_(
                StockCompany.name.like(f'%{search}%'),
                StockCompany.ts_code.like(f'%{search}%')
            )
        )
    
    total = query.count()

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

    # 分页
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return jsonify({
        'data': [c.as_dict() for c in items],
        'total': total
    })

@bp.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
    company = get_company_by_id(company_id)
    if not company:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(company.as_dict())

@bp.route('/', methods=['POST'])
def add_company():
    data = request.json
    company = create_company(data)
    return jsonify(company.as_dict()), 201

@bp.route('/<int:company_id>', methods=['PUT'])
def edit_company(company_id):
    data = request.json
    company = update_company(company_id, data)
    if not company:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(company.as_dict())

@bp.route('/<int:company_id>', methods=['DELETE'])
def remove_company(company_id):
    success = delete_company(company_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'})