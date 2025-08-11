from flask import Blueprint, request, jsonify
from app.services.stock_minute_service import stock_minute_service
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('stock_minute', __name__, url_prefix='/api/stock_minute')

@bp.route('/<ts_code>', methods=['GET'])
def get_minute_by_ts_code(ts_code):
    """
    根据TS代码获取分钟行情数据
    GET /api/stock_minute/<ts_code>?start_time=2024-01-15 09:30:00&end_time=2024-01-15 15:00:00&limit=1000
    """
    try:
        start_time_str = request.args.get('start_time')
        end_time_str = request.args.get('end_time')
        limit = int(request.args.get('limit', 1000))
        
        start_time = None
        end_time = None
        
        if start_time_str:
            start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        if end_time_str:
            end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
        
        data = stock_minute_service.get_by_ts_code(ts_code, start_time, end_time, limit)
        return jsonify({
            'success': True,
            'ts_code': ts_code,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': '时间格式错误，请使用YYYY-MM-DD HH:MM:SS格式'}), 400
    except Exception as e:
        logger.error(f"获取分钟行情数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<ts_code>/latest', methods=['GET'])
def get_latest_minute(ts_code):
    """
    获取指定股票的最新分钟数据
    GET /api/stock_minute/<ts_code>/latest
    """
    try:
        data = stock_minute_service.get_latest_by_ts_code(ts_code)
        if data:
            return jsonify({
                'success': True,
                'ts_code': ts_code,
                'data': data.as_dict()
            })
        else:
            return jsonify({
                'success': False,
                'error': f'未找到分钟数据: {ts_code}'
            }), 404
    except Exception as e:
        logger.error(f"获取最新分钟数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<ts_code>/date/<trade_date>', methods=['GET'])
def get_minute_by_date(ts_code, trade_date):
    """
    根据日期获取分钟行情数据
    GET /api/stock_minute/<ts_code>/date/2024-01-15
    """
    try:
        date_obj = datetime.strptime(trade_date, '%Y-%m-%d').date()
        data = stock_minute_service.get_by_date(ts_code, date_obj)
        return jsonify({
            'success': True,
            'ts_code': ts_code,
            'trade_date': trade_date,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    except Exception as e:
        logger.error(f"获取分钟行情数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<ts_code>/time_range', methods=['GET'])
def get_minute_by_time_range(ts_code):
    """
    根据时间范围获取分钟行情数据
    GET /api/stock_minute/<ts_code>/time_range?start_time=2024-01-15 09:30:00&end_time=2024-01-15 15:00:00
    """
    try:
        start_time_str = request.args.get('start_time')
        end_time_str = request.args.get('end_time')
        
        if not start_time_str or not end_time_str:
            return jsonify({'error': '缺少start_time或end_time参数'}), 400
        
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
        
        data = stock_minute_service.get_by_time_range(ts_code, start_time, end_time)
        return jsonify({
            'success': True,
            'ts_code': ts_code,
            'start_time': start_time_str,
            'end_time': end_time_str,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': '时间格式错误，请使用YYYY-MM-DD HH:MM:SS格式'}), 400
    except Exception as e:
        logger.error(f"获取分钟行情数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<ts_code>/recent', methods=['GET'])
def get_recent_minutes(ts_code):
    """
    获取最近N分钟的行情数据
    GET /api/stock_minute/<ts_code>/recent?minutes=60
    """
    try:
        minutes = int(request.args.get('minutes', 60))
        data = stock_minute_service.get_recent_minutes(ts_code, minutes)
        return jsonify({
            'success': True,
            'ts_code': ts_code,
            'minutes': minutes,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': 'minutes参数必须是整数'}), 400
    except Exception as e:
        logger.error(f"获取最近分钟数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/pct_chg_range', methods=['GET'])
def get_minute_by_pct_chg_range():
    """
    根据涨跌幅范围获取分钟行情数据
    GET /api/stock_minute/pct_chg_range?min_pct=-5&max_pct=5&trade_date=2024-01-15
    """
    try:
        min_pct = float(request.args.get('min_pct', -10))
        max_pct = float(request.args.get('max_pct', 10))
        trade_date_str = request.args.get('trade_date')
        
        trade_date = None
        if trade_date_str:
            trade_date = datetime.strptime(trade_date_str, '%Y-%m-%d').date()
        
        data = stock_minute_service.get_by_pct_chg_range(min_pct, max_pct, trade_date)
        return jsonify({
            'success': True,
            'min_pct': min_pct,
            'max_pct': max_pct,
            'trade_date': trade_date_str,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': '参数格式错误'}), 400
    except Exception as e:
        logger.error(f"获取分钟行情数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/vol_range', methods=['GET'])
def get_minute_by_vol_range():
    """
    根据成交量范围获取分钟行情数据
    GET /api/stock_minute/vol_range?min_vol=1000&max_vol=10000&trade_date=2024-01-15
    """
    try:
        min_vol = int(request.args.get('min_vol', 0))
        max_vol = int(request.args.get('max_vol', 999999))
        trade_date_str = request.args.get('trade_date')
        
        trade_date = None
        if trade_date_str:
            trade_date = datetime.strptime(trade_date_str, '%Y-%m-%d').date()
        
        data = stock_minute_service.get_by_vol_range(min_vol, max_vol, trade_date)
        return jsonify({
            'success': True,
            'min_vol': min_vol,
            'max_vol': max_vol,
            'trade_date': trade_date_str,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': '参数格式错误'}), 400
    except Exception as e:
        logger.error(f"获取分钟行情数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_minute_data():
    """
    创建分钟行情数据
    POST /api/stock_minute/
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求体不能为空'}), 400
        
        result = stock_minute_service.create_or_update(data)
        if result:
            return jsonify({
                'success': True,
                'message': '分钟行情数据创建成功',
                'data': result.as_dict()
            })
        else:
            return jsonify({'error': '分钟行情数据创建失败'}), 500
    except Exception as e:
        logger.error(f"创建分钟行情数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/batch', methods=['POST'])
def batch_create_minute_data():
    """
    批量创建分钟行情数据
    POST /api/stock_minute/batch
    """
    try:
        data_list = request.get_json()
        if not data_list or not isinstance(data_list, list):
            return jsonify({'error': '请求体必须是数组格式'}), 400
        
        success_count = stock_minute_service.batch_create_or_update(data_list)
        return jsonify({
            'success': True,
            'message': f'批量处理完成，成功: {success_count}/{len(data_list)}',
            'total': len(data_list),
            'success_count': success_count
        })
    except Exception as e:
        logger.error(f"批量创建分钟行情数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500 