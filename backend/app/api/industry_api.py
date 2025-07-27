from flask import Blueprint, request, jsonify
from app.services.industry_service import (
    get_all_industries, get_industry_by_id, create_industry, update_industry, delete_industry
)
from sqlalchemy import desc, asc

bp = Blueprint('industry', __name__, url_prefix='/api/industry')

@bp.route('/', methods=['GET'])
def list_industries():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    sort_fields = request.args.get('sort_fields')
    query = get_all_industries(query_only=True)
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

@bp.route('/<int:industry_id>', methods=['GET'])
def get_industry(industry_id):
    industry = get_industry_by_id(industry_id)
    if not industry:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(industry.as_dict())

@bp.route('/', methods=['POST'])
def add_industry():
    data = request.json
    industry = create_industry(data)
    return jsonify(industry.as_dict()), 201

@bp.route('/<int:industry_id>', methods=['PUT'])
def edit_industry(industry_id):
    data = request.json
    industry = update_industry(industry_id, data)
    if not industry:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(industry.as_dict())

@bp.route('/<int:industry_id>', methods=['DELETE'])
def remove_industry(industry_id):
    success = delete_industry(industry_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 