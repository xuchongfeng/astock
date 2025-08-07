import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from app.third_party.deepseek_client import deepseek_service
from app.services.prompt_service import prompt_service
from app.services.deepseek_service import create_deepseek_record, get_deepseek_by_ts_code_and_analysis_type
from app.services import stock_daily_service
from app.services.stock_daily_basic_service import StockDailyBasicService
from app.models.stock_company import StockCompany
from app.models.deepseek import DeepSeek

logger = logging.getLogger(__name__)

class DeepSeekAnalysisService:
    """DeepSeek分析服务类"""
    
    def __init__(self):
        """初始化分析服务"""
        self.stock_daily_basic_service = StockDailyBasicService()
    
    def _get_cached_analysis(self, ts_code: str, analysis_type: str, analysis_date: date = None) -> Optional[Dict]:
        """
        获取缓存的分析结果
        :param ts_code: 股票代码
        :param analysis_type: 分析类型
        :param analysis_date: 分析日期
        :return: 缓存的分析结果
        """
        try:
            cached_record = get_deepseek_by_ts_code_and_analysis_type(ts_code, analysis_type, analysis_date)
            if cached_record:
                logger.info(f"找到缓存的分析结果: {ts_code} - {analysis_type}")
                return {
                    'success': True,
                    'cached': True,
                    'analysis': cached_record.content,
                    'created_at': cached_record.created_at.isoformat() if cached_record.created_at else None
                }
            return None
        except Exception as e:
            logger.error(f"获取缓存分析结果失败: {str(e)}")
            return None
    
    def _get_existing_deepseek_record(self, ts_code: str, analysis_type: str, analysis_date: date = None) -> Optional[DeepSeek]:
        """
        从deepseek表中获取现有记录
        :param ts_code: 股票代码
        :param analysis_type: 分析类型
        :param analysis_date: 分析日期
        :return: DeepSeek记录
        """
        try:
            if analysis_date is None:
                analysis_date = date.today()

            # 构建session_id
            session_id = f"{ts_code}_{analysis_type}_{analysis_date.strftime('%Y%m%d')}"

            # 查询记录
            record = DeepSeek.query.filter_by(
                session_id=session_id,
                type='个股'
            ).first()
            
            if record:
                logger.info(f"找到现有记录: {ts_code} - {analysis_type} - {analysis_date}")
                return record
            
            return None
        except Exception as e:
            logger.error(f"查询现有记录失败: {str(e)}")
            return None
    
    def _create_session_id(self, ts_code: str, analysis_type: str, analysis_date: date = None) -> str:
        """
        创建session_id
        :param ts_code: 股票代码
        :param analysis_type: 分析类型
        :param analysis_date: 分析日期
        :return: session_id
        """
        if analysis_date is None:
            analysis_date = date.today()
        return f"{ts_code}_{analysis_type}_{analysis_date.strftime('%Y%m%d')}"
    
    def analyze_stock_basic_info(self, ts_code: str, session_id: str = None) -> Dict:
        """
        分析个股基本信息
        :param ts_code: 股票代码
        :param session_id: 会话ID
        :return: 分析结果
        """
        try:
            # 首先检查现有记录
            existing_record = self._get_existing_deepseek_record(ts_code, 'basic_info')
            if existing_record:
                return {
                    'success': True,
                    'cached': True,
                    'from_db': True,
                    'stock_code': ts_code,
                    'analysis': existing_record.content,
                    'created_at': existing_record.created_at.isoformat() if existing_record.created_at else None,
                    'updated_at': existing_record.updated_at.isoformat() if existing_record.updated_at else None
                }
            
            # 获取股票基本信息
            stock_company = StockCompany.query.filter_by(ts_code=ts_code).first()
            if not stock_company:
                raise ValueError(f"未找到股票信息: {ts_code}")
            
            # 生成提示词
            prompt = prompt_service.get_stock_analysis_prompt(
                'basic_info',
                stock_name=stock_company.name,
                stock_code=ts_code
            )
            
            # 调用DeepSeek API
            response = deepseek_service.create_conversation(prompt)
            
            # 创建session_id
            if not session_id:
                session_id = self._create_session_id(ts_code, 'basic_info')
            
            # 保存记录
            create_deepseek_record(
                session_id=session_id,
                type='个股',
                content=response.get('choices', [{}])[0].get('message', {}).get('content', ''),
                record_date=date.today()
            )
            
            return {
                'success': True,
                'cached': False,
                'from_db': False,
                'stock_name': stock_company.name,
                'stock_code': ts_code,
                'analysis': response.get('choices', [{}])[0].get('message', {}).get('content', ''),
                'raw_response': response
            }
            
        except Exception as e:
            logger.error(f"分析个股基本信息失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_stock_daily(self, ts_code: str, analysis_date: date = None, 
                           session_id: str = None) -> Dict:
        """
        分析个股每日走势
        :param ts_code: 股票代码
        :param analysis_date: 分析日期
        :param session_id: 会话ID
        :return: 分析结果
        """
        try:
            # 首先检查现有记录
            existing_record = self._get_existing_deepseek_record(ts_code, 'daily_analysis', analysis_date)
            if existing_record:
                return {
                    'success': True,
                    'cached': True,
                    'from_db': True,
                    'stock_code': ts_code,
                    'analysis_date': (analysis_date or date.today()).isoformat(),
                    'analysis': existing_record.content,
                    'created_at': existing_record.created_at.isoformat() if existing_record.created_at else None,
                    'updated_at': existing_record.updated_at.isoformat() if existing_record.updated_at else None
                }
            
            # 获取股票基本信息
            stock_company = StockCompany.query.filter_by(ts_code=ts_code).first()
            if not stock_company:
                raise ValueError(f"未找到股票信息: {ts_code}")
            
            # 获取当日数据
            if analysis_date:
                # 使用函数式服务获取数据
                daily_data = stock_daily_service.get_all_daily({'ts_code': ts_code, 'trade_date': analysis_date})
                daily_data = daily_data[0] if daily_data else None
            else:
                # 获取最新数据
                daily_data = stock_daily_service.get_latest_stock_price(ts_code)
            
            # 生成提示词
            prompt = prompt_service.get_stock_analysis_prompt(
                'daily_analysis',
                stock_name=stock_company.name,
                stock_code=ts_code,
                daily_data=daily_data,
                analysis_date=analysis_date or date.today()
            )
            
            # 调用DeepSeek API
            response = deepseek_service.create_conversation(prompt)
            
            # 创建session_id
            if not session_id:
                session_id = self._create_session_id(ts_code, 'daily_analysis', analysis_date)
            
            # 保存记录
            create_deepseek_record(
                session_id=session_id,
                type='个股',
                content=response.get('choices', [{}])[0].get('message', {}).get('content', ''),
                record_date=analysis_date or date.today()
            )
            
            return {
                'success': True,
                'cached': False,
                'from_db': False,
                'stock_name': stock_company.name,
                'stock_code': ts_code,
                'analysis_date': (analysis_date or date.today()).isoformat(),
                'analysis': response.get('choices', [{}])[0].get('message', {}).get('content', ''),
                'raw_response': response
            }
            
        except Exception as e:
            logger.error(f"分析个股每日走势失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_stock_trend(self, ts_code: str, period: str = "近期", 
                           session_id: str = None) -> Dict:
        """
        分析个股趋势
        :param ts_code: 股票代码
        :param period: 分析周期
        :param session_id: 会话ID
        :return: 分析结果
        """
        try:
            # 首先检查现有记录
            existing_record = self._get_existing_deepseek_record(ts_code, 'trend_analysis')
            if existing_record:
                return {
                    'success': True,
                    'cached': True,
                    'from_db': True,
                    'stock_code': ts_code,
                    'period': period,
                    'analysis': existing_record.content,
                    'created_at': existing_record.created_at.isoformat() if existing_record.created_at else None,
                    'updated_at': existing_record.updated_at.isoformat() if existing_record.updated_at else None
                }
            
            # 获取股票基本信息
            stock_company = StockCompany.query.filter_by(ts_code=ts_code).first()
            if not stock_company:
                raise ValueError(f"未找到股票信息: {ts_code}")
            
            # 获取趋势数据（最近30天）
            from datetime import timedelta
            end_date = date.today()
            start_date = end_date - timedelta(days=30)
            
            # 使用函数式服务获取数据
            trend_data = stock_daily_service.get_all_daily({
                'ts_code': ts_code
            })
            # 过滤日期范围
            trend_data = [data for data in trend_data if start_date <= data.trade_date <= end_date]
            
            # 生成提示词
            prompt = prompt_service.get_stock_analysis_prompt(
                'trend_analysis',
                stock_name=stock_company.name,
                stock_code=ts_code,
                trend_data=[{
                    'trade_date': data.trade_date.isoformat(),
                    'open': float(data.open) if data.open else None,
                    'close': float(data.close) if data.close else None,
                    'high': float(data.high) if data.high else None,
                    'low': float(data.low) if data.low else None,
                    'vol': float(data.vol) if data.vol else None,
                    'pct_chg': float(data.pct_chg) if data.pct_chg else None
                } for data in trend_data] if trend_data else None,
                period=period
            )
            
            # 调用DeepSeek API
            response = deepseek_service.create_conversation(prompt)
            
            # 创建session_id
            if not session_id:
                session_id = self._create_session_id(ts_code, 'trend_analysis')
            
            # 保存记录
            create_deepseek_record(
                session_id=session_id,
                type='个股',
                content=response.get('choices', [{}])[0].get('message', {}).get('content', ''),
                record_date=date.today()
            )
            
            return {
                'success': True,
                'cached': False,
                'from_db': False,
                'stock_name': stock_company.name,
                'stock_code': ts_code,
                'period': period,
                'analysis': response.get('choices', [{}])[0].get('message', {}).get('content', ''),
                'raw_response': response
            }
            
        except Exception as e:
            logger.error(f"分析个股趋势失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_market_overview(self, analysis_date: date = None, 
                               session_id: str = None) -> Dict:
        """
        分析大盘概况
        :param analysis_date: 分析日期
        :param session_id: 会话ID
        :return: 分析结果
        """
        try:
            # 生成提示词
            prompt = prompt_service.get_market_analysis_prompt(
                'market_overview',
                analysis_date=analysis_date or date.today()
            )
            
            # 调用DeepSeek API
            response = deepseek_service.create_conversation(prompt)
            
            # 创建session_id
            if not session_id:
                session_id = f"market_overview_{analysis_date.strftime('%Y%m%d') if analysis_date else date.today().strftime('%Y%m%d')}"
            
            # 保存记录
            create_deepseek_record(
                session_id=session_id,
                type='大盘',
                content=response.get('choices', [{}])[0].get('message', {}).get('content', ''),
                record_date=analysis_date or date.today()
            )
            
            return {
                'success': True,
                'cached': False,
                'from_db': False,
                'analysis_date': (analysis_date or date.today()).isoformat(),
                'analysis': response.get('choices', [{}])[0].get('message', {}).get('content', ''),
                'raw_response': response
            }
            
        except Exception as e:
            logger.error(f"分析大盘概况失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_industry(self, industry_name: str, analysis_date: date = None,
                        session_id: str = None) -> Dict:
        """
        分析行业
        :param industry_name: 行业名称
        :param analysis_date: 分析日期
        :param session_id: 会话ID
        :return: 分析结果
        """
        try:
            # 生成提示词
            prompt = prompt_service.get_market_analysis_prompt(
                'industry_analysis',
                industry_name=industry_name,
                analysis_date=analysis_date or date.today()
            )
            
            # 调用DeepSeek API
            response = deepseek_service.create_conversation(prompt)
            
            # 创建session_id
            if not session_id:
                session_id = f"industry_{industry_name}_{analysis_date.strftime('%Y%m%d') if analysis_date else date.today().strftime('%Y%m%d')}"
            
            # 保存记录
            create_deepseek_record(
                session_id=session_id,
                type='行业',
                content=response.get('choices', [{}])[0].get('message', {}).get('content', ''),
                record_date=analysis_date or date.today()
            )
            
            return {
                'success': True,
                'cached': False,
                'from_db': False,
                'industry_name': industry_name,
                'analysis_date': (analysis_date or date.today()).isoformat(),
                'analysis': response.get('choices', [{}])[0].get('message', {}).get('content', ''),
                'raw_response': response
            }
            
        except Exception as e:
            logger.error(f"分析行业失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_analysis_types(self) -> Dict:
        """
        获取支持的分析类型
        :return: 分析类型列表
        """
        return {
            'stock_analysis': {
                'basic_info': '个股基本信息分析',
                'daily_analysis': '个股每日走势分析',
                'trend_analysis': '个股趋势分析'
            },
            'market_analysis': {
                'market_overview': '大盘概况分析',
                'industry_analysis': '行业分析'
            }
        }

# 创建全局服务实例
deepseek_analysis_service = DeepSeekAnalysisService() 