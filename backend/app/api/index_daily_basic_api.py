from flask import Blueprint, request, jsonify
from app.services.index_daily_basic_service import index_daily_basic_service
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('index_daily_basic', __name__, url_prefix='/api/index_daily_basic')

@bp.route('/<ts_code>', methods=['GET'])
def get_index_by_ts_code(ts_code):
    """
    根据TS代码获取指数数据
    GET /api/index_daily_basic/<ts_code>?limit=100
    """
    try:
        limit = int(request.args.get('limit', 100))
        data = index_daily_basic_service.get_by_ts_code(ts_code, limit)
        return jsonify({
            'success': True,
            'ts_code': ts_code,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except Exception as e:
        logger.error(f"获取指数数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<ts_code>/latest', methods=['GET'])
def get_latest_index(ts_code):
    """
    获取指定指数的最新数据
    GET /api/index_daily_basic/<ts_code>/latest
    """
    try:
        data = index_daily_basic_service.get_latest_by_ts_code(ts_code)
        if data:
            return jsonify({
                'success': True,
                'ts_code': ts_code,
                'data': data.as_dict()
            })
        else:
            return jsonify({
                'success': False,
                'error': f'未找到指数数据: {ts_code}'
            }), 404
    except Exception as e:
        logger.error(f"获取最新指数数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/date/<trade_date>', methods=['GET'])
def get_index_by_date(trade_date):
    """
    根据交易日期获取指数数据
    GET /api/index_daily_basic/date/2024-01-15?limit=100
    """
    try:
        limit = int(request.args.get('limit', 100))
        date_obj = datetime.strptime(trade_date, '%Y-%m-%d').date()
        data = index_daily_basic_service.get_by_trade_date(date_obj, limit)
        return jsonify({
            'success': True,
            'trade_date': trade_date,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    except Exception as e:
        logger.error(f"获取指数数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<ts_code>/date_range', methods=['GET'])
def get_index_by_date_range(ts_code):
    """
    根据日期范围获取指数数据
    GET /api/index_daily_basic/<ts_code>/date_range?start_date=2024-01-01&end_date=2024-01-31
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        if not start_date_str or not end_date_str:
            return jsonify({'error': '缺少start_date或end_date参数'}), 400
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        data = index_daily_basic_service.get_by_date_range(ts_code, start_date, end_date)
        return jsonify({
            'success': True,
            'ts_code': ts_code,
            'start_date': start_date_str,
            'end_date': end_date_str,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    except Exception as e:
        logger.error(f"获取指数数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/pe_range', methods=['GET'])
def get_index_by_pe_range():
    """
    根据市盈率范围获取指数数据
    GET /api/index_daily_basic/pe_range?min_pe=10&max_pe=20&trade_date=2024-01-15
    """
    try:
        min_pe = float(request.args.get('min_pe', 0))
        max_pe = float(request.args.get('max_pe', 999))
        trade_date_str = request.args.get('trade_date')
        
        trade_date = None
        if trade_date_str:
            trade_date = datetime.strptime(trade_date_str, '%Y-%m-%d').date()
        
        data = index_daily_basic_service.get_by_pe_range(min_pe, max_pe, trade_date)
        return jsonify({
            'success': True,
            'min_pe': min_pe,
            'max_pe': max_pe,
            'trade_date': trade_date_str,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': '参数格式错误'}), 400
    except Exception as e:
        logger.error(f"获取指数数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/pb_range', methods=['GET'])
def get_index_by_pb_range():
    """
    根据市净率范围获取指数数据
    GET /api/index_daily_basic/pb_range?min_pb=1&max_pb=3&trade_date=2024-01-15
    """
    try:
        min_pb = float(request.args.get('min_pb', 0))
        max_pb = float(request.args.get('max_pb', 999))
        trade_date_str = request.args.get('trade_date')
        
        trade_date = None
        if trade_date_str:
            trade_date = datetime.strptime(trade_date_str, '%Y-%m-%d').date()
        
        data = index_daily_basic_service.get_by_pb_range(min_pb, max_pb, trade_date)
        return jsonify({
            'success': True,
            'min_pb': min_pb,
            'max_pb': max_pb,
            'trade_date': trade_date_str,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': '参数格式错误'}), 400
    except Exception as e:
        logger.error(f"获取指数数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/turnover_rate', methods=['GET'])
def get_index_by_turnover_rate():
    """
    根据换手率范围获取指数数据
    GET /api/index_daily_basic/turnover_rate?min_rate=0.5&max_rate=2.0&trade_date=2024-01-15
    """
    try:
        min_rate = float(request.args.get('min_rate', 0))
        max_rate = float(request.args.get('max_rate', 999))
        trade_date_str = request.args.get('trade_date')
        
        trade_date = None
        if trade_date_str:
            trade_date = datetime.strptime(trade_date_str, '%Y-%m-%d').date()
        
        data = index_daily_basic_service.get_by_turnover_rate(min_rate, max_rate, trade_date)
        return jsonify({
            'success': True,
            'min_rate': min_rate,
            'max_rate': max_rate,
            'trade_date': trade_date_str,
            'data': [item.as_dict() for item in data],
            'total': len(data)
        })
    except ValueError:
        return jsonify({'error': '参数格式错误'}), 400
    except Exception as e:
        logger.error(f"获取指数数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/market_summary', methods=['GET'])
def get_market_summary():
    """
    获取市场概况
    GET /api/index_daily_basic/market_summary?trade_date=2024-01-15
    """
    try:
        trade_date_str = request.args.get('trade_date')
        trade_date = None
        if trade_date_str:
            trade_date = datetime.strptime(trade_date_str, '%Y-%m-%d').date()
        
        summary = index_daily_basic_service.get_market_summary(trade_date)
        return jsonify({
            'success': True,
            'summary': summary
        })
    except ValueError:
        return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    except Exception as e:
        logger.error(f"获取市场概况失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/fields', methods=['GET'])
def get_fields():
    """
    获取字段信息
    GET /api/index_daily_basic/fields
    """
    fields = {
        'ts_code': 'TS代码',
        'trade_date': '交易日期',
        'total_mv': '当日总市值（元）',
        'float_mv': '当日流通市值（元）',
        'total_share': '当日总股本（股）',
        'float_share': '当日流通股本（股）',
        'free_share': '当日自由流通股本（股）',
        'turnover_rate': '换手率',
        'turnover_rate_f': '换手率(基于自由流通股本)',
        'pe': '市盈率',
        'pe_ttm': '市盈率TTM',
        'pb': '市净率'
    }
    return jsonify({
        'success': True,
        'fields': fields
    })

@bp.route('/', methods=['POST'])
def create_index_data():
    """
    创建指数数据
    POST /api/index_daily_basic/
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请求体不能为空'}), 400
        
        result = index_daily_basic_service.create_or_update(data)
        if result:
            return jsonify({
                'success': True,
                'message': '指数数据创建成功',
                'data': result.as_dict()
            })
        else:
            return jsonify({'error': '指数数据创建失败'}), 500
    except Exception as e:
        logger.error(f"创建指数数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/batch', methods=['POST'])
def batch_create_index_data():
    """
    批量创建指数数据
    POST /api/index_daily_basic/batch
    """
    try:
        data_list = request.get_json()
        if not data_list or not isinstance(data_list, list):
            return jsonify({'error': '请求体必须是数组格式'}), 400
        
        success_count = index_daily_basic_service.batch_create_or_update(data_list)
        return jsonify({
            'success': True,
            'message': f'批量处理完成，成功: {success_count}/{len(data_list)}',
            'total': len(data_list),
            'success_count': success_count
        })
    except Exception as e:
        logger.error(f"批量创建指数数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500 