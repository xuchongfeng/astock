from flask import Blueprint, request, jsonify
from app.services.deepseek_service import (
    create_deepseek_record, get_deepseek_by_id, get_deepseek_by_session_id,
    get_deepseek_by_type, get_deepseek_by_date, get_deepseek_by_date_range,
    get_all_deepseek_records, update_deepseek_record, delete_deepseek_record,
    search_deepseek_records, get_deepseek_statistics
)
from app.third_party.deepseek_client import deepseek_service
import logging
from datetime import datetime, date

bp = Blueprint('deepseek', __name__, url_prefix='/api/deepseek')

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bp.route('/balance', methods=['GET'])
def get_user_balance():
    """
    查询用户余额
    GET /api/deepseek/balance
    """
    try:
        result = deepseek_service.get_user_balance()
        return jsonify(result)
    except Exception as e:
        logger.error(f"查询余额失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/chat', methods=['POST'])
def chat_completion():
    """
    发送对话请求
    POST /api/deepseek/chat
    {
        "messages": [
            {"role": "user", "content": "你好"}
        ],
        "model": "deepseek-chat",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    """
    try:
        data = request.get_json()
        if not data or 'messages' not in data:
            return jsonify({'error': '缺少messages参数'}), 400
        
        messages = data['messages']
        model = data.get('model', 'deepseek-chat')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)
        
        result = deepseek_service.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"对话请求失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/chat/single', methods=['POST'])
def create_single_conversation():
    """
    创建单轮对话
    POST /api/deepseek/chat/single
    {
        "message": "你好",
        "model": "deepseek-chat",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': '缺少message参数'}), 400
        
        user_message = data['message']
        model = data.get('model', 'deepseek-chat')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)
        
        result = deepseek_service.create_conversation(
            user_message=user_message,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"单轮对话失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/chat/continue', methods=['POST'])
def continue_conversation():
    """
    继续多轮对话
    POST /api/deepseek/chat/continue
    {
        "conversation_history": [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！有什么可以帮助你的吗？"}
        ],
        "message": "请介绍一下自己",
        "model": "deepseek-chat",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    """
    try:
        data = request.get_json()
        if not data or 'conversation_history' not in data or 'message' not in data:
            return jsonify({'error': '缺少conversation_history或message参数'}), 400
        
        conversation_history = data['conversation_history']
        user_message = data['message']
        model = data.get('model', 'deepseek-chat')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)
        
        result = deepseek_service.continue_conversation(
            conversation_history=conversation_history,
            user_message=user_message,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"多轮对话失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/models', methods=['GET'])
def get_available_models():
    """
    获取可用的模型列表
    GET /api/deepseek/models
    """
    try:
        # 这里可以返回预定义的模型列表，或者调用DeepSeek的模型列表API
        models = [
            {
                "id": "deepseek-chat",
                "name": "DeepSeek Chat",
                "description": "通用对话模型"
            },
            {
                "id": "deepseek-coder",
                "name": "DeepSeek Coder", 
                "description": "代码生成模型"
            },
            {
                "id": "deepseek-reasoner",
                "name": "DeepSeek Reasoner",
                "description": "推理模型"
            }
        ]
        return jsonify({"models": models})
    except Exception as e:
        logger.error(f"获取模型列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/records', methods=['GET'])
def list_records():
    """获取DeepSeek记录列表"""
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    session_id = request.args.get('session_id')
    type = request.args.get('type')
    record_date = request.args.get('date')
    
    if session_id:
        records = get_deepseek_by_session_id(session_id)
        return jsonify({
            'records': [record.as_dict() for record in records],
            'total': len(records)
        })
    elif type:
        records = get_deepseek_by_type(type)
        return jsonify({
            'records': [record.as_dict() for record in records],
            'total': len(records)
        })
    elif record_date:
        try:
            date_obj = datetime.strptime(record_date, '%Y-%m-%d').date()
            records = get_deepseek_by_date(date_obj)
            return jsonify({
                'records': [record.as_dict() for record in records],
                'total': len(records)
            })
        except ValueError:
            return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    else:
        result = get_all_deepseek_records(page, page_size)
        return jsonify(result)

@bp.route('/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    """获取单个DeepSeek记录"""
    record = get_deepseek_by_id(record_id)
    if not record:
        return jsonify({'error': '记录不存在'}), 404
    return jsonify(record.as_dict())

@bp.route('/records', methods=['POST'])
def create_record():
    """创建DeepSeek记录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少请求数据'}), 400
    
    session_id = data.get('session_id')
    type = data.get('type')
    content = data.get('content')
    record_date = data.get('date')
    
    if not session_id or not type or not content:
        return jsonify({'error': '缺少必要参数'}), 400
    
    # 验证类型
    valid_types = ['个股', '大盘', '行业']
    if type not in valid_types:
        return jsonify({'error': f'无效的类型，必须是: {", ".join(valid_types)}'}), 400
    
    # 处理日期
    date_obj = None
    if record_date:
        try:
            date_obj = datetime.strptime(record_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    
    try:
        record = create_deepseek_record(session_id, type, content, date_obj)
        return jsonify(record.as_dict()), 201
    except Exception as e:
        return jsonify({'error': f'创建记录失败: {str(e)}'}), 500

@bp.route('/records/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    """更新DeepSeek记录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少请求数据'}), 400
    
    content = data.get('content')
    record_date = data.get('date')
    
    if not content and not record_date:
        return jsonify({'error': '缺少content或date参数'}), 400
    
    # 处理日期
    date_obj = None
    if record_date:
        try:
            date_obj = datetime.strptime(record_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    
    try:
        record = update_deepseek_record(record_id, content, date_obj)
        if not record:
            return jsonify({'error': '记录不存在'}), 404
        return jsonify(record.as_dict())
    except Exception as e:
        return jsonify({'error': f'更新记录失败: {str(e)}'}), 500

@bp.route('/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """删除DeepSeek记录"""
    try:
        success = delete_deepseek_record(record_id)
        if not success:
            return jsonify({'error': '记录不存在'}), 404
        return jsonify({'message': '删除成功'})
    except Exception as e:
        return jsonify({'error': f'删除记录失败: {str(e)}'}), 500

@bp.route('/records/search', methods=['GET'])
def search_records():
    """搜索DeepSeek记录"""
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': '缺少keyword参数'}), 400
    
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    try:
        result = search_deepseek_records(keyword, page, page_size)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'搜索失败: {str(e)}'}), 500

@bp.route('/records/date/<date_str>', methods=['GET'])
def get_records_by_date(date_str):
    """根据日期获取DeepSeek记录"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        limit = int(request.args.get('limit', 100))
        records = get_deepseek_by_date(date_obj, limit)
        return jsonify({
            'records': [record.as_dict() for record in records],
            'total': len(records),
            'date': date_str
        })
    except ValueError:
        return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    except Exception as e:
        return jsonify({'error': f'获取记录失败: {str(e)}'}), 500

@bp.route('/records/date_range', methods=['GET'])
def get_records_by_date_range():
    """根据日期范围获取DeepSeek记录"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({'error': '缺少start_date或end_date参数'}), 400
    
    try:
        start_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        limit = int(request.args.get('limit', 100))
        records = get_deepseek_by_date_range(start_obj, end_obj, limit)
        return jsonify({
            'records': [record.as_dict() for record in records],
            'total': len(records),
            'start_date': start_date,
            'end_date': end_date
        })
    except ValueError:
        return jsonify({'error': '日期格式错误，请使用YYYY-MM-DD格式'}), 400
    except Exception as e:
        return jsonify({'error': f'获取记录失败: {str(e)}'}), 500

@bp.route('/statistics', methods=['GET'])
def get_statistics():
    """获取DeepSeek记录统计信息"""
    try:
        stats = get_deepseek_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': f'获取统计信息失败: {str(e)}'}), 500

@bp.route('/types', methods=['GET'])
def get_types():
    """获取支持的类型列表"""
    return jsonify({
        'types': ['个股', '大盘', '行业']
    }) 