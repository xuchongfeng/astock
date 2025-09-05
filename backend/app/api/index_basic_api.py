from flask import Blueprint, request, jsonify
from app.services.index_basic_service import IndexBasicService
import logging

logger = logging.getLogger(__name__)

index_basic_bp = Blueprint('index_basic', __name__)

@index_basic_bp.route('/index_basic', methods=['GET'])
def get_all_index_basic():
    """获取所有指数基本信息"""
    try:
        indices = IndexBasicService.get_all_index_basic()
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': indices
        })
    except Exception as e:
        logger.error(f"获取所有指数基本信息失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@index_basic_bp.route('/index_basic/<ts_code>', methods=['GET'])
def get_index_basic_by_ts_code(ts_code):
    """根据TS代码获取指数基本信息"""
    try:
        index = IndexBasicService.get_index_basic_by_ts_code(ts_code)
        if index:
            return jsonify({
                'code': 200,
                'message': '获取成功',
                'data': index
            })
        else:
            return jsonify({
                'code': 404,
                'message': '指数不存在'
            }), 404
    except Exception as e:
        logger.error(f"根据TS代码获取指数基本信息失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@index_basic_bp.route('/index_basic/market/<market>', methods=['GET'])
def get_index_basic_by_market(market):
    """根据市场获取指数基本信息"""
    try:
        indices = IndexBasicService.get_index_basic_by_market(market)
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': indices
        })
    except Exception as e:
        logger.error(f"根据市场获取指数基本信息失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@index_basic_bp.route('/index_basic/publisher/<publisher>', methods=['GET'])
def get_index_basic_by_publisher(publisher):
    """根据发布方获取指数基本信息"""
    try:
        indices = IndexBasicService.get_index_basic_by_publisher(publisher)
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': indices
        })
    except Exception as e:
        logger.error(f"根据发布方获取指数基本信息失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@index_basic_bp.route('/index_basic/category/<category>', methods=['GET'])
def get_index_basic_by_category(category):
    """根据指数类别获取指数基本信息"""
    try:
        indices = IndexBasicService.get_index_basic_by_category(category)
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': indices
        })
    except Exception as e:
        logger.error(f"根据指数类别获取指数基本信息失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@index_basic_bp.route('/index_basic/search', methods=['GET'])
def search_index_basic():
    """搜索指数基本信息"""
    try:
        keyword = request.args.get('keyword', '')
        if not keyword:
            return jsonify({
                'code': 400,
                'message': '搜索关键词不能为空'
            }), 400
        
        indices = IndexBasicService.search_index_basic(keyword)
        return jsonify({
            'code': 200,
            'message': '搜索成功',
            'data': indices
        })
    except Exception as e:
        logger.error(f"搜索指数基本信息失败: {e}")
        return jsonify({
            'code': 500,
            'message': '搜索失败',
            'error': str(e)
        }), 500

@index_basic_bp.route('/index_basic', methods=['POST'])
def create_index_basic():
    """创建指数基本信息"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求数据不能为空'
            }), 400
        
        index = IndexBasicService.create_index_basic(data)
        if index:
            return jsonify({
                'code': 201,
                'message': '创建成功',
                'data': index
            }), 201
        else:
            return jsonify({
                'code': 500,
                'message': '创建失败'
            }), 500
    except Exception as e:
        logger.error(f"创建指数基本信息失败: {e}")
        return jsonify({
            'code': 500,
            'message': '创建失败',
            'error': str(e)
        }), 500

@index_basic_bp.route('/index_basic/<ts_code>', methods=['PUT'])
def update_index_basic(ts_code):
    """更新指数基本信息"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求数据不能为空'
            }), 400
        
        index = IndexBasicService.update_index_basic(ts_code, data)
        if index:
            return jsonify({
                'code': 200,
                'message': '更新成功',
                'data': index
            })
        else:
            return jsonify({
                'code': 404,
                'message': '指数不存在'
            }), 404
    except Exception as e:
        logger.error(f"更新指数基本信息失败: {e}")
        return jsonify({
            'code': 500,
            'message': '更新失败',
            'error': str(e)
        }), 500

@index_basic_bp.route('/index_basic/<ts_code>', methods=['DELETE'])
def delete_index_basic(ts_code):
    """删除指数基本信息"""
    try:
        success = IndexBasicService.delete_index_basic(ts_code)
        if success:
            return jsonify({
                'code': 200,
                'message': '删除成功'
            })
        else:
            return jsonify({
                'code': 404,
                'message': '指数不存在'
            }), 404
    except Exception as e:
        logger.error(f"删除指数基本信息失败: {e}")
        return jsonify({
            'code': 500,
            'message': '删除失败',
            'error': str(e)
        }), 500
