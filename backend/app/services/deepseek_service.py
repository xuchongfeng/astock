import requests
import json
import logging
from typing import Dict, List, Optional, Any
from app.config import Config
from app import db
from app.models.deepseek import DeepSeek
from datetime import datetime, date

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

def create_deepseek_record(session_id: str, type: str, content: str, record_date: date = None, 
                          ts_code: str = None, analysis_type: str = None) -> DeepSeek:
    """
    创建DeepSeek记录
    :param session_id: 会话ID
    :param type: 类型 (个股/大盘/行业)
    :param content: 返回内容
    :param record_date: 日期，默认为今天
    :param ts_code: 股票代码（可选）
    :param analysis_type: 分析类型（可选）
    :return: DeepSeek记录
    """
    if record_date is None:
        record_date = date.today()
    
    record = DeepSeek(
        session_id=session_id,
        type=type,
        content=content,
        date=record_date
    )
    db.session.add(record)
    db.session.commit()
    return record

def get_deepseek_by_id(record_id: int) -> Optional[DeepSeek]:
    """
    根据ID获取DeepSeek记录
    :param record_id: 记录ID
    :return: DeepSeek记录
    """
    return DeepSeek.query.get(record_id)

def get_deepseek_by_session_id(session_id: str) -> List[DeepSeek]:
    """
    根据会话ID获取DeepSeek记录列表
    :param session_id: 会话ID
    :return: DeepSeek记录列表
    """
    return DeepSeek.query.filter_by(session_id=session_id).order_by(DeepSeek.created_at.desc()).all()

def get_deepseek_by_type(type: str, limit: int = 100) -> List[DeepSeek]:
    """
    根据类型获取DeepSeek记录列表
    :param type: 类型 (个股/大盘/行业)
    :param limit: 限制数量
    :return: DeepSeek记录列表
    """
    return DeepSeek.query.filter_by(type=type).order_by(DeepSeek.created_at.desc()).limit(limit).all()

def get_deepseek_by_date(record_date: date, limit: int = 100) -> List[DeepSeek]:
    """
    根据日期获取DeepSeek记录列表
    :param record_date: 日期
    :param limit: 限制数量
    :return: DeepSeek记录列表
    """
    return DeepSeek.query.filter_by(date=record_date).order_by(DeepSeek.created_at.desc()).limit(limit).all()

def get_deepseek_by_date_range(start_date: date, end_date: date, limit: int = 100) -> List[DeepSeek]:
    """
    根据日期范围获取DeepSeek记录列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param limit: 限制数量
    :return: DeepSeek记录列表
    """
    return DeepSeek.query.filter(
        DeepSeek.date >= start_date,
        DeepSeek.date <= end_date
    ).order_by(DeepSeek.created_at.desc()).limit(limit).all()

def get_deepseek_by_ts_code_and_analysis_type(ts_code: str, analysis_type: str, 
                                             record_date: date = None) -> Optional[DeepSeek]:
    """
    根据股票代码和分析类型获取DeepSeek记录
    :param ts_code: 股票代码
    :param analysis_type: 分析类型
    :param record_date: 日期，默认为今天
    :return: DeepSeek记录
    """
    if record_date is None:
        record_date = date.today()
    
    # 构建session_id作为查询条件
    session_id = f"{ts_code}_{analysis_type}_{record_date.strftime('%Y%m%d')}"
    
    return DeepSeek.query.filter_by(session_id=session_id, type='个股').first()

def get_all_deepseek_records(page: int = 1, page_size: int = 20) -> Dict:
    """
    获取所有DeepSeek记录（分页）
    :param page: 页码
    :param page_size: 每页数量
    :return: 包含记录列表和总数的字典
    """
    query = DeepSeek.query.order_by(DeepSeek.created_at.desc())
    total = query.count()
    records = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        'records': [record.as_dict() for record in records],
        'total': total,
        'page': page,
        'page_size': page_size
    }

def update_deepseek_record(record_id: int, content: str, record_date: date = None) -> Optional[DeepSeek]:
    """
    更新DeepSeek记录
    :param record_id: 记录ID
    :param content: 新的返回内容
    :param record_date: 新的日期，可选
    :return: 更新后的DeepSeek记录
    """
    record = get_deepseek_by_id(record_id)
    if record:
        record.content = content
        if record_date:
            record.date = record_date
        record.updated_at = datetime.now()
        db.session.commit()
    return record

def delete_deepseek_record(record_id: int) -> bool:
    """
    删除DeepSeek记录
    :param record_id: 记录ID
    :return: 是否删除成功
    """
    record = get_deepseek_by_id(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()
        return True
    return False

def search_deepseek_records(keyword: str, page: int = 1, page_size: int = 20) -> Dict:
    """
    搜索DeepSeek记录
    :param keyword: 搜索关键词
    :param page: 页码
    :param page_size: 每页数量
    :return: 包含记录列表和总数的字典
    """
    query = DeepSeek.query.filter(
        DeepSeek.content.like(f'%{keyword}%')
    ).order_by(DeepSeek.created_at.desc())
    
    total = query.count()
    records = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        'records': [record.as_dict() for record in records],
        'total': total,
        'page': page,
        'page_size': page_size
    }

def get_deepseek_statistics() -> Dict:
    """
    获取DeepSeek记录统计信息
    :return: 统计信息字典
    """
    total_records = DeepSeek.query.count()
    
    # 按类型统计
    type_stats = db.session.query(
        DeepSeek.type,
        db.func.count(DeepSeek.id).label('count')
    ).group_by(DeepSeek.type).all()
    
    # 按日期统计（最近7天）
    from datetime import timedelta
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_records = DeepSeek.query.filter(
        DeepSeek.created_at >= seven_days_ago
    ).count()
    
    # 按日期统计
    date_stats = db.session.query(
        DeepSeek.date,
        db.func.count(DeepSeek.id).label('count')
    ).group_by(DeepSeek.date).order_by(DeepSeek.date.desc()).limit(30).all()
    
    return {
        'total_records': total_records,
        'recent_records': recent_records,
        'type_statistics': {stat.type: stat.count for stat in type_stats},
        'date_statistics': {stat.date.isoformat(): stat.count for stat in date_stats}
    } 