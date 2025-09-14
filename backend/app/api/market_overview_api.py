from flask import Blueprint, request, jsonify
from app.services.index_daily_service import IndexDailyService
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

market_overview_bp = Blueprint('market_overview', __name__, url_prefix='/api')

@market_overview_bp.route('/market_overview/indices', methods=['GET'])
def get_market_indices():
    """获取市场主要指数概览数据"""
    try:
        # 获取三个主要指数的最新数据
        indices = [
            {'ts_code': '000001.SH', 'name': '上证指数'},
            {'ts_code': '399107.SZ', 'name': '深圳成指'},
            {'ts_code': '399006.SZ', 'name': '创业板指'}
        ]
        
        result = []
        for index in indices:
            # 获取最新数据
            latest_data = IndexDailyService.get_latest_index_daily(index['ts_code'])
            if latest_data:
                # 获取前一个交易日数据用于计算涨跌
                previous_data = IndexDailyService.get_index_daily_by_ts_code(
                    index['ts_code'], limit=2
                )
                
                if len(previous_data) >= 2:
                    prev_close = previous_data[1]['close']
                    current_close = latest_data['close']
                    change = current_close - prev_close
                    change_pct = (change / prev_close) * 100 if prev_close else 0
                else:
                    change = latest_data.get('change', 0)
                    change_pct = latest_data.get('pct_chg', 0)
                
                result.append({
                    'ts_code': index['ts_code'],
                    'name': index['name'],
                    'current_price': latest_data['close'],
                    'change': change,
                    'change_pct': change_pct,
                    'volume': latest_data.get('vol', 0),
                    'amount': latest_data.get('amount', 0),
                    'trade_date': latest_data['trade_date']
                })
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': result
        })
        
    except Exception as e:
        logger.error(f"获取市场指数概览失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@market_overview_bp.route('/market_overview/indices/<ts_code>/chart', methods=['GET'])
def get_index_chart_data(ts_code):
    """获取指定指数的图表数据"""
    try:
        # 获取参数
        days = request.args.get('days', 30, type=int)
        if days <= 0:
            days = 30
        
        # 计算日期范围
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # 获取指数数据
        daily_data = IndexDailyService.get_index_daily_by_date_range(
            ts_code, start_date, end_date
        )
        
        if not daily_data:
            return jsonify({
                'code': 404,
                'message': '未找到该指数的数据'
            }), 404
        
        # 格式化图表数据
        chart_data = {
            'dates': [item['trade_date'] for item in daily_data],
            'prices': [float(item['close']) for item in daily_data],
            'volumes': [float(item['vol']) for item in daily_data],
            'amounts': [float(item['amount']) for item in daily_data]
        }
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': chart_data
        })
        
    except Exception as e:
        logger.error(f"获取指数图表数据失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500

@market_overview_bp.route('/market_overview/indices/statistics', methods=['GET'])
def get_market_statistics():
    """获取市场统计信息"""
    try:
        # 获取参数
        days = request.args.get('days', 30, type=int)
        if days <= 0:
            days = 30
        
        indices = ['000001.SH', '399107.SZ', '399006.SZ']
        statistics = []
        
        for ts_code in indices:
            stats = IndexDailyService.get_index_daily_statistics(ts_code, days)
            if stats:
                statistics.append(stats)
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': statistics
        })
        
    except Exception as e:
        logger.error(f"获取市场统计信息失败: {e}")
        return jsonify({
            'code': 500,
            'message': '获取失败',
            'error': str(e)
        }), 500
