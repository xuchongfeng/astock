from flask import Blueprint, request, jsonify
import logging
from datetime import datetime, date
from app.services.deepseek_analysis_service import deepseek_analysis_service

bp = Blueprint('deepseek_analysis', __name__, url_prefix='/api/deepseek_analysis')

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bp.route('/stock/basic_info/<ts_code>', methods=['GET'])
def analyze_stock_basic_info(ts_code):
    """
    分析个股基本信息
    GET /api/deepseek_analysis/stock/basic_info/<ts_code>?session_id=xxx
    """
    try:
        session_id = request.args.get('session_id')
        result = deepseek_analysis_service.analyze_stock_basic_info(ts_code, session_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"分析个股基本信息失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/stock/daily/<ts_code>', methods=['GET'])
def analyze_stock_daily(ts_code):
    """
    分析个股每日走势
    GET /api/deepseek_analysis/stock/daily/<ts_code>?date=2024-01-15&session_id=xxx
    """
    try:
        date_str = request.args.get('date')
        session_id = request.args.get('session_id')
        
        analysis_date = None
        if date_str:
            try:
                analysis_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
        
        result = deepseek_analysis_service.analyze_stock_daily(ts_code, analysis_date, session_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"分析个股每日走势失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/stock/trend/<ts_code>', methods=['GET'])
def analyze_stock_trend(ts_code):
    """
    分析个股趋势
    GET /api/deepseek_analysis/stock/trend/<ts_code>?period=近期&session_id=xxx
    """
    try:
        period = request.args.get('period', '近期')
        session_id = request.args.get('session_id')
        
        result = deepseek_analysis_service.analyze_stock_trend(ts_code, period, session_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"分析个股趋势失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/market/overview', methods=['GET'])
def analyze_market_overview():
    """
    分析大盘概况
    GET /api/deepseek_analysis/market/overview?date=2024-01-15&session_id=xxx
    """
    try:
        date_str = request.args.get('date')
        session_id = request.args.get('session_id')
        
        analysis_date = None
        if date_str:
            try:
                analysis_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
        
        result = deepseek_analysis_service.analyze_market_overview(analysis_date, session_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"分析大盘概况失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/industry/<industry_name>', methods=['GET'])
def analyze_industry(industry_name):
    """
    分析行业
    GET /api/deepseek_analysis/industry/科技?date=2024-01-15&session_id=xxx
    """
    try:
        date_str = request.args.get('date')
        session_id = request.args.get('session_id')
        
        analysis_date = None
        if date_str:
            try:
                analysis_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
        
        result = deepseek_analysis_service.analyze_industry(industry_name, analysis_date, session_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"分析行业失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/analysis_types', methods=['GET'])
def get_analysis_types():
    """
    获取支持的分析类型
    GET /api/deepseek_analysis/analysis_types
    """
    try:
        types = deepseek_analysis_service.get_analysis_types()
        return jsonify({
            'success': True,
            'analysis_types': types
        })
    except Exception as e:
        logger.error(f"获取分析类型失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/stock/<ts_code>/comprehensive', methods=['GET'])
def analyze_stock_comprehensive(ts_code):
    """
    综合分析个股（包含基本信息、每日走势、趋势分析）
    GET /api/deepseek_analysis/stock/<ts_code>/comprehensive?session_id=xxx
    """
    try:
        session_id = request.args.get('session_id')
        
        # 执行三种分析
        basic_result = deepseek_analysis_service.analyze_stock_basic_info(ts_code, session_id)
        daily_result = deepseek_analysis_service.analyze_stock_daily(ts_code, None, session_id)
        trend_result = deepseek_analysis_service.analyze_stock_trend(ts_code, "近期", session_id)
        
        return jsonify({
            'success': True,
            'stock_code': ts_code,
            'comprehensive_analysis': {
                'basic_info': basic_result,
                'daily_analysis': daily_result,
                'trend_analysis': trend_result
            }
        })
    except Exception as e:
        logger.error(f"综合分析个股失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/market/comprehensive', methods=['GET'])
def analyze_market_comprehensive():
    """
    综合分析市场（包含大盘概况和主要行业分析）
    GET /api/deepseek_analysis/market/comprehensive?session_id=xxx
    """
    try:
        session_id = request.args.get('session_id')
        
        # 分析大盘概况
        market_result = deepseek_analysis_service.analyze_market_overview(None, session_id)
        
        # 分析主要行业（这里可以预设几个主要行业）
        main_industries = ['科技', '金融', '医药', '消费', '新能源']
        industry_results = {}
        
        for industry in main_industries:
            try:
                industry_result = deepseek_analysis_service.analyze_industry(industry, None, session_id)
                industry_results[industry] = industry_result
            except Exception as e:
                logger.warning(f"分析行业 {industry} 失败: {str(e)}")
                industry_results[industry] = {'success': False, 'error': str(e)}
        
        return jsonify({
            'success': True,
            'comprehensive_analysis': {
                'market_overview': market_result,
                'industry_analysis': industry_results
            }
        })
    except Exception as e:
        logger.error(f"综合分析市场失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500 