from flask import Blueprint, request, jsonify
from app.services.stock_daily_basic_service import stock_daily_basic_service
import logging

bp = Blueprint('stock_daily_basic', __name__, url_prefix='/api/stock_daily_basic')

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bp.route('/<ts_code>', methods=['GET'])
def get_stock_daily_basic(ts_code):
    """
    获取指定股票的每日指标数据
    GET /api/stock_daily_basic/<ts_code>?start_date=2024-01-01&end_date=2024-01-31
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        result = stock_daily_basic_service.get_by_ts_code(
            ts_code=ts_code,
            start_date=start_date,
            end_date=end_date
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取股票 {ts_code} 每日指标失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<ts_code>/latest', methods=['GET'])
def get_latest_stock_daily_basic(ts_code):
    """
    获取指定股票的最新每日指标数据
    GET /api/stock_daily_basic/<ts_code>/latest
    """
    try:
        result = stock_daily_basic_service.get_latest_by_ts_code(ts_code)
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': '未找到数据'}), 404
    except Exception as e:
        logger.error(f"获取股票 {ts_code} 最新每日指标失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/date/<trade_date>', methods=['GET'])
def get_daily_basic_by_date(trade_date):
    """
    根据交易日期获取所有股票的每日指标数据
    GET /api/stock_daily_basic/date/2024-01-15
    """
    try:
        result = stock_daily_basic_service.get_by_trade_date(trade_date)
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取日期 {trade_date} 每日指标失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/pe_range', methods=['GET'])
def get_by_pe_range():
    """
    根据市盈率范围获取股票数据
    GET /api/stock_daily_basic/pe_range?min_pe=10&max_pe=20&trade_date=2024-01-15
    """
    try:
        min_pe = request.args.get('min_pe', type=float)
        max_pe = request.args.get('max_pe', type=float)
        trade_date = request.args.get('trade_date')
        
        if min_pe is None or max_pe is None:
            return jsonify({'error': '请提供min_pe和max_pe参数'}), 400
        
        result = stock_daily_basic_service.get_by_pe_range(
            min_pe=min_pe,
            max_pe=max_pe,
            trade_date=trade_date
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"根据市盈率范围获取股票失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/pb_range', methods=['GET'])
def get_by_pb_range():
    """
    根据市净率范围获取股票数据
    GET /api/stock_daily_basic/pb_range?min_pb=1&max_pb=3&trade_date=2024-01-15
    """
    try:
        min_pb = request.args.get('min_pb', type=float)
        max_pb = request.args.get('max_pb', type=float)
        trade_date = request.args.get('trade_date')
        
        if min_pb is None or max_pb is None:
            return jsonify({'error': '请提供min_pb和max_pb参数'}), 400
        
        result = stock_daily_basic_service.get_by_pb_range(
            min_pb=min_pb,
            max_pb=max_pb,
            trade_date=trade_date
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"根据市净率范围获取股票失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/turnover_rate', methods=['GET'])
def get_by_turnover_rate():
    """
    根据换手率范围获取股票数据
    GET /api/stock_daily_basic/turnover_rate?min_rate=1&max_rate=5&trade_date=2024-01-15
    """
    try:
        min_rate = request.args.get('min_rate', type=float)
        max_rate = request.args.get('max_rate', type=float)
        trade_date = request.args.get('trade_date')
        
        if min_rate is None or max_rate is None:
            return jsonify({'error': '请提供min_rate和max_rate参数'}), 400
        
        result = stock_daily_basic_service.get_by_turnover_rate(
            min_rate=min_rate,
            max_rate=max_rate,
            trade_date=trade_date
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"根据换手率范围获取股票失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/market_summary', methods=['GET'])
def get_market_summary():
    """
    获取市场概况统计
    GET /api/stock_daily_basic/market_summary?trade_date=2024-01-15
    """
    try:
        trade_date = request.args.get('trade_date')
        result = stock_daily_basic_service.get_market_summary(trade_date)
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取市场概况失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/fields', methods=['GET'])
def get_available_fields():
    """
    获取可用的字段信息
    GET /api/stock_daily_basic/fields
    """
    fields = {
        'ts_code': 'TS股票代码',
        'trade_date': '交易日期',
        'close': '当日收盘价',
        'turnover_rate': '换手率（%）',
        'turnover_rate_f': '换手率（自由流通股）',
        'volume_ratio': '量比',
        'pe': '市盈率（总市值/净利润，亏损的PE为空）',
        'pe_ttm': '市盈率（TTM，亏损的PE为空）',
        'pb': '市净率（总市值/净资产）',
        'ps': '市销率',
        'ps_ttm': '市销率（TTM）',
        'dv_ratio': '股息率（%）',
        'dv_ttm': '股息率（TTM）（%）',
        'total_share': '总股本（万股）',
        'float_share': '流通股本（万股）',
        'free_share': '自由流通股本（万）',
        'total_mv': '总市值（万元）',
        'circ_mv': '流通市值（万元）'
    }
    return jsonify(fields) 