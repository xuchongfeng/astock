from flask import Blueprint, request, jsonify
from app.services.trade_calendar_service import trade_calendar_service
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('trade_calendar', __name__, url_prefix='/api/trade_calendar')

@bp.route('/<exchange>', methods=['GET'])
def get_calendar_by_exchange(exchange):
    """
    根据交易所获取交易日历
    GET /api/trade_calendar/<exchange>?start_date=2024-01-01&end_date=2024-12-31
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        data = trade_calendar_service.get_by_exchange(exchange, start_date, end_date)
        return jsonify({
            'success': True,
            'exchange': exchange,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    except Exception as e:
        logger.error(f"获取交易日历失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<exchange>/trading_days', methods=['GET'])
def get_trading_days(exchange):
    """
    获取交易日列表
    GET /api/trade_calendar/<exchange>/trading_days?start_date=2024-01-01&end_date=2024-12-31
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        data = trade_calendar_service.get_trading_days(exchange, start_date, end_date)
        return jsonify({
            'success': True,
            'exchange': exchange,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    except Exception as e:
        logger.error(f"获取交易日失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<exchange>/is_trading_day', methods=['GET'])
def is_trading_day(exchange):
    """
    判断是否为交易日
    GET /api/trade_calendar/<exchange>/is_trading_day?date=2024-01-15
    """
    try:
        date_str = request.args.get('date')
        if not date_str:
            return jsonify({'error': '缺少date参数'}), 400
        
        check_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        is_trading = trade_calendar_service.is_trading_day(exchange, check_date)
        
        return jsonify({
            'success': True,
            'exchange': exchange,
            'date': date_str,
            'is_trading_day': is_trading
        })
    except ValueError:
        return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    except Exception as e:
        logger.error(f"判断交易日失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<exchange>/next_trading_day', methods=['GET'])
def get_next_trading_day(exchange):
    """
    获取下一个交易日
    GET /api/trade_calendar/<exchange>/next_trading_day?from_date=2024-01-15
    """
    try:
        from_date_str = request.args.get('from_date')
        if not from_date_str:
            return jsonify({'error': '缺少from_date参数'}), 400
        
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        next_day = trade_calendar_service.get_next_trading_day(exchange, from_date)
        
        if next_day:
            return jsonify({
                'success': True,
                'exchange': exchange,
                'from_date': from_date_str,
                'next_trading_day': next_day.as_dict()
            })
        else:
            return jsonify({
                'success': False,
                'error': '未找到下一个交易日'
            }), 404
    except ValueError:
        return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    except Exception as e:
        logger.error(f"获取下一个交易日失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<exchange>/prev_trading_day', methods=['GET'])
def get_prev_trading_day(exchange):
    """
    获取上一个交易日
    GET /api/trade_calendar/<exchange>/prev_trading_day?from_date=2024-01-15
    """
    try:
        from_date_str = request.args.get('from_date')
        if not from_date_str:
            return jsonify({'error': '缺少from_date参数'}), 400
        
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        prev_day = trade_calendar_service.get_prev_trading_day(exchange, from_date)
        
        if prev_day:
            return jsonify({
                'success': True,
                'exchange': exchange,
                'from_date': from_date_str,
                'prev_trading_day': prev_day.as_dict()
            })
        else:
            return jsonify({
                'success': False,
                'error': '未找到上一个交易日'
            }), 404
    except ValueError:
        return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    except Exception as e:
        logger.error(f"获取上一个交易日失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_calendar():
    """
    创建交易日历
    POST /api/trade_calendar/
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求体不能为空'}), 400
        
        result = trade_calendar_service.create_or_update(data)
        if result:
            return jsonify({
                'success': True,
                'message': '交易日历创建成功',
                'data': result.as_dict()
            })
        else:
            return jsonify({'error': '交易日历创建失败'}), 500
    except Exception as e:
        logger.error(f"创建交易日历失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/batch', methods=['POST'])
def batch_create_calendar():
    """
    批量创建交易日历
    POST /api/trade_calendar/batch
    """
    try:
        data_list = request.get_json()
        if not data_list or not isinstance(data_list, list):
            return jsonify({'error': '请求体必须是数组格式'}), 400
        
        success_count = trade_calendar_service.batch_create_or_update(data_list)
        return jsonify({
            'success': True,
            'message': f'批量处理完成，成功: {success_count}/{len(data_list)}',
            'total': len(data_list),
            'success_count': success_count
        })
    except Exception as e:
        logger.error(f"批量创建交易日历失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500 