from flask import Blueprint, request, jsonify
from app.services.index_daily_service import IndexDailyService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

index_daily_bp = Blueprint('index_daily', __name__)

@index_daily_bp.route('/index_daily', methods=['GET'])
def get_all_index_daily():
    """获取所有指数日线行情"""
    try:
        daily_data = IndexDailyService.get_all_index_daily()
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': daily_data
        })
    except Exception as e:
        logger.error(f"获取所有指数日线行情失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@index_daily_bp.route('/index_daily/<ts_code>', methods=['GET'])
def get_index_daily_by_ts_code(ts_code):
    """根据TS代码获取指数日线行情"""
    try:
        limit = request.args.get('limit', type=int)
        daily_data = IndexDailyService.get_index_daily_by_ts_code(ts_code, limit)
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': daily_data
        })
    except Exception as e:
        logger.error(f"根据TS代码获取指数日线行情失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@index_daily_bp.route('/index_daily/<ts_code>/range', methods=['GET'])
def get_index_daily_by_date_range(ts_code):
    """根据日期范围获取指数日线行情"""
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        if not start_date_str or not end_date_str:
            return jsonify({
                'code': 400,
                'message': '开始日期和结束日期不能为空'
            }), 400
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'code': 400,
                'message': '日期格式错误，请使用YYYY-MM-DD格式'
            }), 400
        
        daily_data = IndexDailyService.get_index_daily_by_date_range(ts_code, start_date, end_date)
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': daily_data
        })
    except Exception as e:
        logger.error(f"根据日期范围获取指数日线行情失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@index_daily_bp.route('/index_daily/date/<trade_date>', methods=['GET'])
def get_index_daily_by_trade_date(trade_date):
    """根据交易日期获取所有指数日线行情"""
    try:
        try:
            trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'code': 400,
                'message': '日期格式错误，请使用YYYY-MM-DD格式'
            }), 400
        
        daily_data = IndexDailyService.get_index_daily_by_trade_date(trade_date_obj)
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': daily_data
        })
    except Exception as e:
        logger.error(f"根据交易日期获取指数日线行情失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@index_daily_bp.route('/index_daily/<ts_code>/latest', methods=['GET'])
def get_latest_index_daily(ts_code):
    """获取指定指数的最新日线行情"""
    try:
        latest_data = IndexDailyService.get_latest_index_daily(ts_code)
        if latest_data:
            return jsonify({
                'code': 200,
                'message': '获取成功',
                'data': latest_data
            })
        else:
            return jsonify({
                'code': 404,
                'message': '未找到该指数的日线行情数据'
            }), 404
    except Exception as e:
        logger.error(f"获取指定指数的最新日线行情失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@index_daily_bp.route('/index_daily/<ts_code>/statistics', methods=['GET'])
def get_index_daily_statistics(ts_code):
    """获取指定指数的统计信息"""
    try:
        days = request.args.get('days', 30, type=int)
        if days <= 0:
            days = 30
        
        stats = IndexDailyService.get_index_daily_statistics(ts_code, days)
        if stats:
            return jsonify({
                'code': 200,
                'message': '获取成功',
                'data': stats
            })
        else:
            return jsonify({
                'code': 404,
                'message': '未找到该指数的统计数据'
            }), 404
    except Exception as e:
        logger.error(f"获取指定指数的统计信息失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@index_daily_bp.route('/index_daily', methods=['POST'])
def create_index_daily():
    """创建指数日线行情"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求数据不能为空'
            }), 400
        
        daily_data = IndexDailyService.create_index_daily(data)
        if daily_data:
            return jsonify({
                'code': 201,
                'message': '创建成功',
                'data': daily_data
            }), 201
        else:
            return jsonify({
                'code': 500,
                'message': '创建失败'
            }), 500
    except Exception as e:
        logger.error(f"创建指数日线行情失败: {e}")
        return jsonify({
            'code': 500,
            'message': '创建失败',
            'error': str(e)
        }), 500

@index_daily_bp.route('/index_daily/batch', methods=['POST'])
def batch_create_index_daily():
    """批量创建指数日线行情"""
    try:
        data_list = request.get_json()
        if not data_list or not isinstance(data_list, list):
            return jsonify({
                'code': 400,
                'message': '请求数据必须是数组格式'
            }), 400
        
        success = IndexDailyService.batch_create_index_daily(data_list)
        if success:
            return jsonify({
                'code': 201,
                'message': '批量创建成功'
            }), 201
        else:
            return jsonify({
                'code': 500,
                'message': '批量创建失败'
            }), 500
    except Exception as e:
        logger.error(f"批量创建指数日线行情失败: {e}")
        return jsonify({
            'code': 500,
            'message': '批量创建失败',
            'error': str(e)
        }), 500

@index_daily_bp.route('/index_daily/<ts_code>/<trade_date>', methods=['PUT'])
def update_index_daily(ts_code, trade_date):
    """更新指数日线行情"""
    try:
        try:
            trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'code': 400,
                'message': '日期格式错误，请使用YYYY-MM-DD格式'
            }), 400
        
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求数据不能为空'
            }), 400
        
        daily_data = IndexDailyService.update_index_daily(ts_code, trade_date_obj, data)
        if daily_data:
            return jsonify({
                'code': 200,
                'message': '更新成功',
                'data': daily_data
            })
        else:
            return jsonify({
                'code': 404,
                'message': '未找到该指数的日线行情数据'
            }), 404
    except Exception as e:
        logger.error(f"更新指数日线行情失败: {e}")
        return jsonify({
            'code': 500,
            'message': '更新失败',
            'error': str(e)
        }), 500

@index_daily_bp.route('/index_daily/<ts_code>/<trade_date>', methods=['DELETE'])
def delete_index_daily(ts_code, trade_date):
    """删除指数日线行情"""
    try:
        try:
            trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'code': 400,
                'message': '日期格式错误，请使用YYYY-MM-DD格式'
            }), 400
        
        success = IndexDailyService.delete_index_daily(ts_code, trade_date_obj)
        if success:
            return jsonify({
                'code': 200,
                'message': '删除成功'
            })
        else:
            return jsonify({
                'code': 404,
                'message': '未找到该指数的日线行情数据'
            }), 404
    except Exception as e:
        logger.error(f"删除指数日线行情失败: {e}")
        return jsonify({
            'code': 500,
            'message': '删除失败',
            'error': str(e)
        }), 500
