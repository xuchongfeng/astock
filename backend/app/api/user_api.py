from flask import Blueprint, request, jsonify
from app.services.user_service import (
    get_all_users, get_user_by_id, get_user_by_username, get_user_by_email,
    create_user, update_user, delete_user
)
from sqlalchemy import desc, asc

bp = Blueprint('user', __name__, url_prefix='/api/user')

@bp.route('/', methods=['GET'])
def list_users():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    sort_fields = request.args.get('sort_fields')
    query = get_all_users(query_only=True)
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
        'data': [u.as_dict() for u in items],
        'total': total
    })

@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(user.as_dict())

@bp.route('/', methods=['POST'])
def add_user():
    data = request.json
    user = create_user(data)
    return jsonify(user.as_dict()), 201

@bp.route('/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    data = request.json
    user = update_user(user_id, data)
    if not user:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(user.as_dict())

@bp.route('/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    success = delete_user(user_id)
    if not success:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'result': 'success'}) 