from flask import Blueprint, request, jsonify
from typing import Dict, Any
from datetime import date
from app.services import tag_service

# 创建蓝图
tag_bp = Blueprint('tag', __name__, url_prefix='/api/tags')


@tag_bp.route('/', methods=['GET'])
def get_tags():
    """获取所有标签"""
    try:
        
        category = request.args.get('category')
        tags = tag_service.get_all_tags(category=category)
        
        return jsonify({
            'code': 200,
            'message': '获取标签列表成功',
            'data': [tag.to_dict() for tag in tags]
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取标签列表失败: {str(e)}',
            'data': None
        })


@tag_bp.route('/', methods=['POST'])
def create_tag():
    """创建标签"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        color = data.get('color', '#1890ff')
        category = data.get('category', 'trend')
        
        if not name:
            return jsonify({
                'code': 400,
                'message': '标签名称不能为空',
                'data': None
            })
        
        # 检查标签是否已存在
        existing_tag = tag_service.get_tag_by_name(name)
        if existing_tag:
            return jsonify({
                'code': 400,
                'message': '标签名称已存在',
                'data': None
            })
        
        tag = tag_service.create_tag(
            name=name,
            description=description,
            color=color,
            category=category
        )
        
        return jsonify({
            'code': 200,
            'message': '创建标签成功',
            'data': tag.to_dict()
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'创建标签失败: {str(e)}',
            'data': None
        })


@tag_bp.route('/<int:tag_id>', methods=['GET'])
def get_tag(tag_id: int):
    """获取单个标签"""
    try:
        tag = tag_service.get_tag_by_id(tag_id)
        if not tag:
            return jsonify({
                'code': 404,
                'message': '标签不存在',
                'data': None
            })
        
        return jsonify({
            'code': 200,
            'message': '获取标签成功',
            'data': tag.to_dict()
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取标签失败: {str(e)}',
            'data': None
        })


@tag_bp.route('/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id: int):
    """更新标签"""
    try:
        data = request.get_json()
        tag = tag_service.update_tag(tag_id, **data)
        if not tag:
            return jsonify({
                'code': 404,
                'message': '标签不存在',
                'data': None
            })
        
        return jsonify({
            'code': 200,
            'message': '更新标签成功',
            'data': tag.to_dict()
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新标签失败: {str(e)}',
            'data': None
        })


@tag_bp.route('/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id: int):
    """删除标签"""
    try:
        success = tag_service.delete_tag(tag_id)
        if not success:
            return jsonify({
                'code': 404,
                'message': '标签不存在',
                'data': None
            })
        
        return jsonify({
            'code': 200,
            'message': '删除标签成功',
            'data': None
        })
    except ValueError as e:
        return jsonify({
            'code': 400,
            'message': str(e),
            'data': None
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'删除标签失败: {str(e)}',
            'data': None
        })


@tag_bp.route('/popular', methods=['GET'])
def get_popular_tags():
    """获取热门标签"""
    try:
        limit = request.args.get('limit', 10, type=int)
        popular_tags = tag_service.get_popular_tags(limit=limit)
        
        return jsonify({
            'code': 200,
            'message': '获取热门标签成功',
            'data': popular_tags
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取热门标签失败: {str(e)}',
            'data': None
        })


@tag_bp.route('/stocks/<ts_code>/tags', methods=['GET'])
def get_stock_tags(ts_code: str):
    """获取股票的标签"""
    try:
        user_id = request.args.get('user_id', type=int)
        include_expired = request.args.get('include_expired', 'true').lower() == 'true'
        
        stock_tags = tag_service.get_stock_tags(
            ts_code=ts_code,
            user_id=user_id,
            include_expired=include_expired
        )
        
        return jsonify({
            'code': 200,
            'message': '获取股票标签成功',
            'data': [stock_tag.to_dict() for stock_tag in stock_tags]
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取股票标签失败: {str(e)}',
            'data': None
        })


@tag_bp.route('/stocks/<ts_code>/tags', methods=['POST'])
def add_stock_tag(ts_code: str):
    """为股票添加标签"""
    try:
        data = request.get_json()
        tag_id = data.get('tag_id')
        user_id = data.get('user_id')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        note = data.get('note')
        
        if not tag_id:
            return jsonify({
                'code': 400,
                'message': '标签ID不能为空',
                'data': None
            })
        
        # 转换日期
        start_date = None
        end_date = None
        if start_date_str:
            start_date = date.fromisoformat(start_date_str)
        if end_date_str:
            end_date = date.fromisoformat(end_date_str)
        
        stock_tag = tag_service.add_stock_tag(
            ts_code=ts_code,
            tag_id=tag_id,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            note=note
        )
        
        return jsonify({
            'code': 200,
            'message': '添加股票标签成功',
            'data': stock_tag.to_dict()
        })
    except ValueError as e:
        return jsonify({
            'code': 400,
            'message': str(e),
            'data': None
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'添加股票标签失败: {str(e)}',
            'data': None
        })


@tag_bp.route('/stocks/<ts_code>/tags/<int:tag_id>', methods=['DELETE'])
def remove_stock_tag(ts_code: str, tag_id: int):
    """移除股票的标签"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        success = tag_service.remove_stock_tag(
            ts_code=ts_code,
            tag_id=tag_id,
            user_id=user_id
        )
        
        if not success:
            return jsonify({
                'code': 404,
                'message': '股票标签关联不存在',
                'data': None
            })
        
        return jsonify({
            'code': 200,
            'message': '移除股票标签成功',
            'data': None
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'移除股票标签失败: {str(e)}',
            'data': None
        })


@tag_bp.route('/stocks/<ts_code>/summary', methods=['GET'])
def get_stock_tag_summary(ts_code: str):
    """获取股票的标签摘要"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        summary = tag_service.get_stock_tag_summary(
            ts_code=ts_code,
            user_id=user_id
        )
        
        return jsonify({
            'code': 200,
            'message': '获取股票标签摘要成功',
            'data': summary
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取股票标签摘要失败: {str(e)}',
            'data': None
        })


@tag_bp.route('/tags/<int:tag_id>/stocks', methods=['GET'])
def get_stocks_by_tag(tag_id: int):
    """根据标签获取股票列表"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        stocks = tag_service.get_stocks_by_tag(tag_id=tag_id, user_id=user_id)
        
        return jsonify({
            'code': 200,
            'message': '获取标签股票列表成功',
            'data': stocks
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取标签股票列表失败: {str(e)}',
            'data': None
        }) 