from app import db
from app.models.index_daily_basic import IndexDailyBasic
from datetime import datetime, date
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class IndexDailyBasicService:
    """大盘指数每日指标服务类"""
    
    @staticmethod
    def get_by_ts_code(ts_code: str, limit: int = 100) -> List[IndexDailyBasic]:
        """
        根据TS代码获取指数数据
        :param ts_code: TS代码
        :param limit: 限制数量
        :return: 指数数据列表
        """
        try:
            return IndexDailyBasic.query.filter_by(ts_code=ts_code)\
                .order_by(IndexDailyBasic.trade_date.desc())\
                .limit(limit).all()
        except Exception as e:
            logger.error(f"获取指数数据失败: {str(e)}")
            return []
    
    @staticmethod
    def get_by_trade_date(trade_date: date, limit: int = 100) -> List[IndexDailyBasic]:
        """
        根据交易日期获取指数数据
        :param trade_date: 交易日期
        :param limit: 限制数量
        :return: 指数数据列表
        """
        try:
            return IndexDailyBasic.query.filter_by(trade_date=trade_date)\
                .order_by(IndexDailyBasic.ts_code)\
                .limit(limit).all()
        except Exception as e:
            logger.error(f"获取指数数据失败: {str(e)}")
            return []
    
    @staticmethod
    def get_latest_by_ts_code(ts_code: str) -> Optional[IndexDailyBasic]:
        """
        获取指定指数的最新数据
        :param ts_code: TS代码
        :return: 最新指数数据
        """
        try:
            return IndexDailyBasic.query.filter_by(ts_code=ts_code)\
                .order_by(IndexDailyBasic.trade_date.desc())\
                .first()
        except Exception as e:
            logger.error(f"获取最新指数数据失败: {str(e)}")
            return None
    
    @staticmethod
    def get_by_date_range(ts_code: str, start_date: date, end_date: date) -> List[IndexDailyBasic]:
        """
        根据日期范围获取指数数据
        :param ts_code: TS代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: 指数数据列表
        """
        try:
            return IndexDailyBasic.query.filter(
                IndexDailyBasic.ts_code == ts_code,
                IndexDailyBasic.trade_date >= start_date,
                IndexDailyBasic.trade_date <= end_date
            ).order_by(IndexDailyBasic.trade_date.desc()).all()
        except Exception as e:
            logger.error(f"获取指数数据失败: {str(e)}")
            return []
    
    @staticmethod
    def get_by_pe_range(min_pe: float, max_pe: float, trade_date: date = None) -> List[IndexDailyBasic]:
        """
        根据市盈率范围获取指数数据
        :param min_pe: 最小市盈率
        :param max_pe: 最大市盈率
        :param trade_date: 交易日期
        :return: 指数数据列表
        """
        try:
            query = IndexDailyBasic.query.filter(
                IndexDailyBasic.pe >= min_pe,
                IndexDailyBasic.pe <= max_pe
            )
            if trade_date:
                query = query.filter(IndexDailyBasic.trade_date == trade_date)
            return query.order_by(IndexDailyBasic.pe).all()
        except Exception as e:
            logger.error(f"获取指数数据失败: {str(e)}")
            return []
    
    @staticmethod
    def get_by_pb_range(min_pb: float, max_pb: float, trade_date: date = None) -> List[IndexDailyBasic]:
        """
        根据市净率范围获取指数数据
        :param min_pb: 最小市净率
        :param max_pb: 最大市净率
        :param trade_date: 交易日期
        :return: 指数数据列表
        """
        try:
            query = IndexDailyBasic.query.filter(
                IndexDailyBasic.pb >= min_pb,
                IndexDailyBasic.pb <= max_pb
            )
            if trade_date:
                query = query.filter(IndexDailyBasic.trade_date == trade_date)
            return query.order_by(IndexDailyBasic.pb).all()
        except Exception as e:
            logger.error(f"获取指数数据失败: {str(e)}")
            return []
    
    @staticmethod
    def get_by_turnover_rate(min_rate: float, max_rate: float, trade_date: date = None) -> List[IndexDailyBasic]:
        """
        根据换手率范围获取指数数据
        :param min_rate: 最小换手率
        :param max_rate: 最大换手率
        :param trade_date: 交易日期
        :return: 指数数据列表
        """
        try:
            query = IndexDailyBasic.query.filter(
                IndexDailyBasic.turnover_rate >= min_rate,
                IndexDailyBasic.turnover_rate <= max_rate
            )
            if trade_date:
                query = query.filter(IndexDailyBasic.trade_date == trade_date)
            return query.order_by(IndexDailyBasic.turnover_rate.desc()).all()
        except Exception as e:
            logger.error(f"获取指数数据失败: {str(e)}")
            return []
    
    @staticmethod
    def get_market_summary(trade_date: date = None) -> Dict[str, Any]:
        """
        获取市场概况
        :param trade_date: 交易日期
        :return: 市场概况数据
        """
        try:
            if trade_date is None:
                trade_date = date.today()
            
            # 获取当日所有指数数据
            index_data = IndexDailyBasic.query.filter_by(trade_date=trade_date).all()
            
            if not index_data:
                return {
                    'trade_date': trade_date.isoformat(),
                    'total_indices': 0,
                    'avg_pe': 0,
                    'avg_pb': 0,
                    'avg_turnover_rate': 0,
                    'total_market_value': 0,
                    'indices': []
                }
            
            # 计算统计数据
            total_pe = sum(item.pe for item in index_data if item.pe is not None)
            total_pb = sum(item.pb for item in index_data if item.pb is not None)
            total_turnover = sum(item.turnover_rate for item in index_data if item.turnover_rate is not None)
            total_mv = sum(item.total_mv for item in index_data if item.total_mv is not None)
            
            valid_pe_count = len([item for item in index_data if item.pe is not None])
            valid_pb_count = len([item for item in index_data if item.pb is not None])
            valid_turnover_count = len([item for item in index_data if item.turnover_rate is not None])
            
            return {
                'trade_date': trade_date.isoformat(),
                'total_indices': len(index_data),
                'avg_pe': total_pe / valid_pe_count if valid_pe_count > 0 else 0,
                'avg_pb': total_pb / valid_pb_count if valid_pb_count > 0 else 0,
                'avg_turnover_rate': total_turnover / valid_turnover_count if valid_turnover_count > 0 else 0,
                'total_market_value': total_mv,
                'indices': [item.as_dict() for item in index_data]
            }
        except Exception as e:
            logger.error(f"获取市场概况失败: {str(e)}")
            return {
                'trade_date': trade_date.isoformat() if trade_date else date.today().isoformat(),
                'error': str(e)
            }
    
    @staticmethod
    def create_or_update(data: Dict[str, Any]) -> Optional[IndexDailyBasic]:
        """
        创建或更新指数数据
        :param data: 指数数据
        :return: 创建的指数数据
        """
        try:
            ts_code = data.get('ts_code')
            trade_date_str = data.get('trade_date')
            
            if not ts_code or not trade_date_str:
                logger.error("缺少必要参数: ts_code 或 trade_date")
                return None
            
            # 转换日期
            if isinstance(trade_date_str, str):
                trade_date = datetime.strptime(trade_date_str, '%Y%m%d').date()
            else:
                trade_date = trade_date_str
            
            # 查找现有记录
            existing = IndexDailyBasic.query.filter_by(
                ts_code=ts_code,
                trade_date=trade_date
            ).first()
            
            if existing:
                # 更新现有记录
                for key, value in data.items():
                    if hasattr(existing, key) and key not in ['ts_code', 'trade_date']:
                        setattr(existing, key, value)
                existing.updated_at = datetime.now()
                db.session.commit()
                logger.info(f"更新指数数据: {ts_code} {trade_date}")
                return existing
            else:
                # 创建新记录
                index_data = IndexDailyBasic(
                    ts_code=ts_code,
                    trade_date=trade_date,
                    total_mv=data.get('total_mv'),
                    float_mv=data.get('float_mv'),
                    total_share=data.get('total_share'),
                    float_share=data.get('float_share'),
                    free_share=data.get('free_share'),
                    turnover_rate=data.get('turnover_rate'),
                    turnover_rate_f=data.get('turnover_rate_f'),
                    pe=data.get('pe'),
                    pe_ttm=data.get('pe_ttm'),
                    pb=data.get('pb')
                )
                db.session.add(index_data)
                db.session.commit()
                logger.info(f"创建指数数据: {ts_code} {trade_date}")
                return index_data
                
        except Exception as e:
            logger.error(f"创建或更新指数数据失败: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def batch_create_or_update(data_list: List[Dict[str, Any]]) -> int:
        """
        批量创建或更新指数数据
        :param data_list: 指数数据列表
        :return: 成功处理的数量
        """
        success_count = 0
        try:
            for data in data_list:
                if IndexDailyBasicService.create_or_update(data):
                    success_count += 1
            logger.info(f"批量处理指数数据完成，成功: {success_count}/{len(data_list)}")
            return success_count
        except Exception as e:
            logger.error(f"批量处理指数数据失败: {str(e)}")
            return success_count

# 创建全局服务实例
index_daily_basic_service = IndexDailyBasicService() 