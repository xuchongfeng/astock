import requests
import json
import logging
from typing import Dict, List, Optional, Any
from app.config import Config

logger = logging.getLogger(__name__)

class DeepSeekService:
    """DeepSeek API服务类"""
    
    def __init__(self):
        """初始化服务"""
        self.api_key = Config.DEEPSEEK_API_KEY
        self.base_url = Config.DEEPSEEK_BASE_URL
        self.session = requests.Session()
        
        # 设置默认请求头
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
    
    def get_user_balance(self) -> Dict:
        """
        获取用户余额
        :return: 余额信息
        """
        url = f"{self.base_url}/v1/user/balance"
        return self._make_request('GET', url)
    
    def chat_completion(self, messages: List[Dict], model: str = "deepseek-chat", 
                       temperature: float = 0.7, max_tokens: int = 1000) -> Dict:
        """
        发送聊天完成请求
        :param messages: 消息列表
        :param model: 模型名称
        :param temperature: 温度参数
        :param max_tokens: 最大token数
        :return: 响应结果
        """
        url = f"{self.base_url}/v1/chat/completions"
        data = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        return self._make_request('POST', url, data=data)
    
    def create_conversation(self, user_message: str, model: str = "deepseek-chat",
                          temperature: float = 0.7, max_tokens: int = 1000) -> Dict:
        """
        创建单轮对话
        :param user_message: 用户消息
        :param model: 模型名称
        :param temperature: 温度参数
        :param max_tokens: 最大token数
        :return: 响应结果
        """
        messages = [{"role": "user", "content": user_message}]
        return self.chat_completion(messages, model, temperature, max_tokens)
    
    def continue_conversation(self, conversation_history: List[Dict], user_message: str,
                            model: str = "deepseek-chat", temperature: float = 0.7,
                            max_tokens: int = 1000) -> Dict:
        """
        继续多轮对话
        :param conversation_history: 对话历史
        :param user_message: 用户消息
        :param model: 模型名称
        :param temperature: 温度参数
        :param max_tokens: 最大token数
        :return: 响应结果
        """
        messages = conversation_history + [{"role": "user", "content": user_message}]
        return self.chat_completion(messages, model, temperature, max_tokens)
    
    def _make_request(self, method: str, url: str, data: Dict = None) -> Dict:
        """
        发送HTTP请求
        :param method: HTTP方法
        :param url: 请求URL
        :param data: 请求数据
        :return: 响应数据
        """
        try:
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON解析失败: {str(e)}")

# 创建全局服务实例
deepseek_service = DeepSeekService() 