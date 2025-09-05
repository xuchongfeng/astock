from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.services.dc_hot_service import DcHotService
from app.config import Config
import tushare as ts
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

dc_hot_bp = Blueprint('dc_hot', __name__, url_prefix='/api')

@dc_hot_bp.route('/dc_hot/list', methods=['GET'])
@cross_origin()
def get_dc_hot_list():
    """
    获取东方财富热榜数据列表
    """
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        trade_date = request.args.get('trade_date', '')
        ts_code = request.args.get('ts_code', '')
        market = request.args.get('market', '')
        hot_type = request.args.get('hot_type', '')
        search = request.args.get('search', '')
        
        # 参数验证
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 20
        
        # 过滤空字符串
        trade_date = trade_date if trade_date else None
        ts_code = ts_code if ts_code else None
        market = market if market else None
        hot_type = hot_type if hot_type else None
        search = search if search else None
        
        # 使用数据库连接
        dc_hot_service = DcHotService()
        
        # 获取数据
        result = dc_hot_service.get_dc_hot_list(
            page=page,
            page_size=page_size,
            trade_date=trade_date,
            ts_code=ts_code,
            market=market,
            hot_type=hot_type,
            search=search
        )
        
        # 转换数据为可序列化格式
        data_list = []
        for item in result['data']:
            data_list.append({
                'id': item.id,
                'trade_date': item.trade_date,
                'data_type': item.data_type,
                'ts_code': item.ts_code,
                'ts_name': item.ts_name,
                'rank': item.rank,
                'pct_change': item.pct_change,
                'current_price': item.current_price,
                'rank_time': item.rank_time,
                'market': item.market,
                'hot_type': item.hot_type,
                'is_new': item.is_new,
                'created_at': item.created_at.isoformat() if item.created_at else None,
                'updated_at': item.updated_at.isoformat() if item.updated_at else None
            })
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'data': data_list,
                'total': result['total'],
                'page': result['page'],
                'page_size': result['page_size']
            }
        })
        
    except Exception as e:
        logger.error(f"获取东方财富热榜数据失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'获取数据失败: {str(e)}',
            'data': None
        }), 500

@dc_hot_bp.route('/dc_hot/sync', methods=['POST'])
@cross_origin()
def sync_dc_hot():
    """从Tushare同步东方财富App热榜数据到本地表 dc_hot"""
    try:
        body = request.get_json() or {}
        trade_date = body.get('trade_date')  # 例如 '20240415' 或 '2024-04-15'
        market = body.get('market', 'A股市场')
        hot_type = body.get('hot_type', '人气榜')
        is_new = body.get('is_new', 'Y')

        # 规范 trade_date 为 YYYYMMDD
        if trade_date and '-' in trade_date:
            trade_date = trade_date.replace('-', '')

        # 初始化 Tushare
        ts.set_token(os.getenv('TUSHARE_TOKEN', ''))
        pro = ts.pro_api()

        params = {
            'market': market,
            'hot_type': hot_type,
            'is_new': is_new
        }
        if trade_date:
            params['trade_date'] = trade_date

        df = pro.dc_hot(**params, fields='trade_date,ts_code,ts_name,rank,pct_change,current_price,rank_time')

        # 写入数据库
        svc = DcHotService()
        inserted = 0
        for _, row in df.iterrows():
            data = {
                'trade_date': row['trade_date'],
                'data_type': '热榜',
                'ts_code': row['ts_code'],
                'ts_name': row['ts_name'],
                'rank': int(row['rank']) if not pd.isna(row['rank']) else None,
                'pct_change': float(row['pct_change']) if not pd.isna(row['pct_change']) else None,
                'current_price': float(row['current_price']) if not pd.isna(row['current_price']) else None,
                'rank_time': row['rank_time'] if not pd.isna(row['rank_time']) else None,
                'market': market,
                'hot_type': hot_type,
                'is_new': is_new
            }
            svc.create_dc_hot(data)
            inserted += 1

        return jsonify({
            'code': 200,
            'message': '同步完成',
            'data': {
                'inserted': inserted
            }
        })
    except Exception as e:
        logger.error(f"同步东方财富热榜失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'同步失败: {str(e)}',
            'data': None
        }), 500

@dc_hot_bp.route('/dc_hot/latest', methods=['GET'])
@cross_origin()
def get_latest_dc_hot():
    """
    获取最新的东方财富热榜数据
    """
    try:
        market = request.args.get('market', 'A股市场')
        hot_type = request.args.get('hot_type', '人气榜')
        
        # 使用数据库连接
        dc_hot_service = DcHotService()
        
        # 获取最新数据
        data = dc_hot_service.get_latest_dc_hot(market=market, hot_type=hot_type)
        
        # 转换数据为可序列化格式
        data_list = []
        for item in data:
            data_list.append({
                'id': item.id,
                'trade_date': item.trade_date,
                'data_type': item.data_type,
                'ts_code': item.ts_code,
                'ts_name': item.ts_name,
                'rank': item.rank,
                'pct_change': item.pct_change,
                'current_price': item.current_price,
                'rank_time': item.rank_time,
                'market': item.market,
                'hot_type': item.hot_type,
                'is_new': item.is_new
            })
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': data_list
        })
        
    except Exception as e:
        logger.error(f"获取最新东方财富热榜数据失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'获取数据失败: {str(e)}',
            'data': None
        }), 500

@dc_hot_bp.route('/dc_hot/markets', methods=['GET'])
@cross_origin()
def get_markets():
    """
    获取可用的市场类型列表
    """
    try:
        # 使用数据库连接
        dc_hot_service = DcHotService()
        
        # 获取市场类型列表
        markets = dc_hot_service.get_markets()
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'markets': markets
            }
        })
        
    except Exception as e:
        logger.error(f"获取市场类型列表失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'获取数据失败: {str(e)}',
            'data': None
        }), 500

@dc_hot_bp.route('/dc_hot/hot_types', methods=['GET'])
@cross_origin()
def get_hot_types():
    """
    获取可用的热点类型列表
    """
    try:
        # 使用数据库连接
        dc_hot_service = DcHotService()
        
        # 获取热点类型列表
        hot_types = dc_hot_service.get_hot_types()
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': {
                'hot_types': hot_types
            }
        })
        
    except Exception as e:
        logger.error(f"获取热点类型列表失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'获取数据失败: {str(e)}',
            'data': None
        }), 500

@dc_hot_bp.route('/dc_hot', methods=['POST'])
@cross_origin()
def create_dc_hot():
    """
    创建东方财富热榜数据
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求数据不能为空',
                'data': None
            }), 400
        
        # 使用数据库连接
        dc_hot_service = DcHotService()
        
        # 创建数据
        dc_hot = dc_hot_service.create_dc_hot(data)
        
        return jsonify({
            'code': 200,
            'message': '创建成功',
            'data': {
                'id': dc_hot.id,
                'ts_code': dc_hot.ts_code,
                'ts_name': dc_hot.ts_name
            }
        })
        
    except Exception as e:
        logger.error(f"创建东方财富热榜数据失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'创建失败: {str(e)}',
            'data': None
        }), 500

@dc_hot_bp.route('/dc_hot/<int:dc_hot_id>', methods=['PUT'])
@cross_origin()
def update_dc_hot(dc_hot_id):
    """
    更新东方财富热榜数据
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求数据不能为空',
                'data': None
            }), 400
        
        # 使用数据库连接
        dc_hot_service = DcHotService()
        
        # 更新数据
        dc_hot = dc_hot_service.update_dc_hot(dc_hot_id, data)
        
        if not dc_hot:
            return jsonify({
                'code': 404,
                'message': '数据不存在',
                'data': None
            }), 404
        
        return jsonify({
            'code': 200,
            'message': '更新成功',
            'data': {
                'id': dc_hot.id,
                'ts_code': dc_hot.ts_code,
                'ts_name': dc_hot.ts_name
            }
        })
        
    except Exception as e:
        logger.error(f"更新东方财富热榜数据失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'更新失败: {str(e)}',
            'data': None
        }), 500

@dc_hot_bp.route('/dc_hot/<int:dc_hot_id>', methods=['DELETE'])
@cross_origin()
def delete_dc_hot(dc_hot_id):
    """
    删除东方财富热榜数据
    """
    try:
        # 使用数据库连接
        dc_hot_service = DcHotService()
        
        # 删除数据
        success = dc_hot_service.delete_dc_hot(dc_hot_id)
        
        if not success:
            return jsonify({
                'code': 404,
                'message': '数据不存在',
                'data': None
            }), 404
        
        return jsonify({
            'code': 200,
            'message': '删除成功',
            'data': None
        })
        
    except Exception as e:
        logger.error(f"删除东方财富热榜数据失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'删除失败: {str(e)}',
            'data': None
        }), 500

@dc_hot_bp.route('/dc_hot/<int:dc_hot_id>', methods=['GET'])
@cross_origin()
def get_dc_hot_by_id(dc_hot_id):
    """
    根据ID获取东方财富热榜数据
    """
    try:
        # 使用数据库连接
        dc_hot_service = DcHotService()
        
        # 获取数据
        dc_hot = dc_hot_service.get_dc_hot_by_id(dc_hot_id)
        
        if not dc_hot:
            return jsonify({
                'code': 404,
                'message': '数据不存在',
                'data': None
            }), 404
        
        # 转换数据为可序列化格式
        data = {
            'id': dc_hot.id,
            'trade_date': dc_hot.trade_date,
            'data_type': dc_hot.data_type,
            'ts_code': dc_hot.ts_code,
            'ts_name': dc_hot.ts_name,
            'rank': dc_hot.rank,
            'pct_change': dc_hot.pct_change,
            'current_price': dc_hot.current_price,
            'rank_time': dc_hot.rank_time,
            'market': dc_hot.market,
            'hot_type': dc_hot.hot_type,
            'is_new': dc_hot.is_new,
            'created_at': dc_hot.created_at.isoformat() if dc_hot.created_at else None,
            'updated_at': dc_hot.updated_at.isoformat() if dc_hot.updated_at else None
        }
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': data
        })
        
    except Exception as e:
        logger.error(f"根据ID获取东方财富热榜数据失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'获取数据失败: {str(e)}',
            'data': None
        }), 500
