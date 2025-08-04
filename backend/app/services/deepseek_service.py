import requests
import json
from typing import Dict, List, Optional, Any
from app.config import Config


class DeepSeekService:
    """DeepSeek API服务类"""
    
    def __init__(self, api_key: str = None):
        """
        初始化DeepSeek服务
        :param api_key: DeepSeek API密钥
        """
        self.api_key = api_key or Config.DEEPSEEK_API_KEY
        self.base_url = Config.DEEPSEEK_BASE_URL
        self.session = requests.Session()
        
        # 设置基础headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        })

    def _make_request(self, method: str, url: str, data: Dict = None, headers: Dict = None) -> Dict:
        """
        发送HTTP请求
        :param method: HTTP方法
        :param url: 请求URL
        :param data: 请求数据
        :param headers: 请求头
        :return: 响应数据
        """
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON解析失败: {str(e)}")

    def get_user_balance(self) -> Dict:
        """
        查询用户余额
        :return: 余额信息
        """
        url = f"{self.base_url}/user/balance"
        return self._make_request('GET', url)

    def chat_completion(self, messages: List[Dict], model: str = "deepseek-chat", 
                       temperature: float = 0.7, max_tokens: int = 1000) -> Dict:
        """
        发送对话请求
        :param messages: 对话消息列表
        :param model: 模型名称
        :param temperature: 温度参数
        :param max_tokens: 最大token数
        :return: 对话响应
        """
        url = f"{self.base_url}/chat/completions"
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
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
        :return: 对话响应
        """
        messages = [{"role": "user", "content": user_message}]
        return self.chat_completion(messages, model, temperature, max_tokens)

    def continue_conversation(self, conversation_history: List[Dict], user_message: str, 
                            model: str = "deepseek-chat", temperature: float = 0.7, 
                            max_tokens: int = 1000) -> Dict:
        """
        继续多轮对话
        :param conversation_history: 对话历史
        :param user_message: 用户新消息
        :param model: 模型名称
        :param temperature: 温度参数
        :param max_tokens: 最大token数
        :return: 对话响应
        """
        # 复制对话历史并添加新消息
        messages = conversation_history.copy()
        messages.append({"role": "user", "content": user_message})
        
        response = self.chat_completion(messages, model, temperature, max_tokens)
        
        # 将助手的回复也添加到历史中
        if response.get('choices') and len(response['choices']) > 0:
            assistant_message = response['choices'][0]['message']
            messages.append(assistant_message)
            response['updated_conversation_history'] = messages
        
        return response


# 创建全局服务实例
deepseek_service = DeepSeekService() 