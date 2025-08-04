from flask import Blueprint, request, jsonify
from app.services.deepseek_service import deepseek_service
import logging

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