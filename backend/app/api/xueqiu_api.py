from flask import Blueprint, request, jsonify
from app.services.xueqiu_service import xueqiu_service
import logging

bp = Blueprint('xueqiu', __name__, url_prefix='/api/xueqiu')

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bp.route('/portfolio/groups', methods=['GET'])
def get_portfolio_groups():
    """
    获取用户的个股分组列表
    GET /api/xueqiu/portfolio/groups?user_id=12345
    """
    try:
        user_id = request.args.get('user_id')
        result = xueqiu_service.get_portfolio_groups(user_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取分组列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/portfolio/groups/<group_id>/stocks', methods=['GET'])
def get_group_stocks(group_id):
    """
    获取分组的股票列表
    GET /api/xueqiu/portfolio/groups/<group_id>/stocks
    """
    try:
        result = xueqiu_service.get_group_stocks(group_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取分组股票列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/portfolio/groups', methods=['POST'])
def create_portfolio_group():
    """
    创建新的分组
    POST /api/xueqiu/portfolio/groups
    {
        "name": "分组名称",
        "description": "分组描述"
    }
    """
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': '缺少分组名称'}), 400
        
        result = xueqiu_service.create_portfolio_group(
            name=data['name'],
            description=data.get('description')
        )
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"创建分组失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/portfolio/groups/<group_id>/stocks', methods=['POST'])
def add_stock_to_group(group_id):
    """
    向分组添加股票
    POST /api/xueqiu/portfolio/groups/<group_id>/stocks
    {
        "stock_code": "股票代码",
        "stock_name": "股票名称"
    }
    """
    try:
        data = request.get_json()
        if not data or 'stock_code' not in data:
            return jsonify({'error': '缺少股票代码'}), 400
        
        result = xueqiu_service.add_stock_to_group(
            group_name=data['group_name'],
            stock_code=data['stock_code'],
            stock_name=data.get('stock_name')
        )
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"添加股票到分组失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/portfolio/groups/<group_id>/stocks/<stock_code>', methods=['DELETE'])
def remove_stock_from_group(group_id, stock_code):
    """
    从分组移除股票
    DELETE /api/xueqiu/portfolio/groups/<group_id>/stocks/<stock_code>
    """
    try:
        result = xueqiu_service.remove_stock_from_group(group_id, stock_code)
        return jsonify(result)
    except Exception as e:
        logger.error(f"从分组移除股票失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/portfolio/groups/<group_id>', methods=['PUT'])
def update_portfolio_group(group_id):
    """
    更新分组信息
    PUT /api/xueqiu/portfolio/groups/<group_id>
    {
        "name": "新分组名称",
        "description": "新分组描述"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '缺少更新数据'}), 400
        
        result = xueqiu_service.update_portfolio_group(
            group_id=group_id,
            name=data.get('name'),
            description=data.get('description')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"更新分组失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/portfolio/groups/<group_id>', methods=['DELETE'])
def delete_portfolio_group(group_id):
    """
    删除分组
    DELETE /api/xueqiu/portfolio/groups/<group_id>
    """
    try:
        result = xueqiu_service.delete_portfolio_group(group_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"删除分组失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/stocks/<stock_code>', methods=['GET'])
def get_stock_info(stock_code):
    """
    获取股票基本信息
    GET /api/xueqiu/stocks/<stock_code>
    """
    try:
        result = xueqiu_service.get_stock_info(stock_code)
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取股票信息失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/stocks/search', methods=['GET'])
def search_stocks():
    """
    搜索股票
    GET /api/xueqiu/stocks/search?keyword=关键词
    """
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            return jsonify({'error': '缺少搜索关键词'}), 400
        
        result = xueqiu_service.search_stocks(keyword)
        return jsonify(result)
    except Exception as e:
        logger.error(f"搜索股票失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/user/info', methods=['GET'])
def get_user_info():
    """
    获取用户信息
    GET /api/xueqiu/user/info
    """
    try:
        result = xueqiu_service.get_user_info()
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    """
    登录雪球账户
    POST /api/xueqiu/login
    {
        "username": "用户名",
        "password": "密码"
    }
    """
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': '缺少用户名或密码'}), 400
        
        result = xueqiu_service.login(data['username'], data['password'])
        return jsonify(result)
    except Exception as e:
        logger.error(f"登录失败: {str(e)}")
        return jsonify({'error': str(e)}), 500 