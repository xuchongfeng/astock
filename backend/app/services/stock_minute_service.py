from app import db
from app.models.stock_minute import StockMinute
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class StockMinuteService:
    """分钟行情数据服务类"""
    
    @staticmethod
    def get_by_ts_code(ts_code: str, start_time: datetime = None, end_time: datetime = None, limit: int = 1000) -> List[StockMinute]:
        """
        根据TS代码获取分钟行情数据
        :param ts_code: TS代码
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param limit: 限制数量
        :return: 分钟行情数据列表
        """
        try:
            query = StockMinute.query.filter_by(ts_code=ts_code)
            
            if start_time:
                query = query.filter(StockMinute.trade_time >= start_time)
            if end_time:
                query = query.filter(StockMinute.trade_time <= end_time)
            
            return query.order_by(StockMinute.trade_time.desc()).limit(limit).all()
        except Exception as e:
            logger.error(f"获取分钟行情数据失败: {str(e)}")
            return []
    
    @staticmethod
    def get_by_date(ts_code: str, trade_date: date) -> List[StockMinute]:
        """
        根据日期获取分钟行情数据
        :param ts_code: TS代码
        :param trade_date: 交易日期
        :return: 分钟行情数据列表
        """
        try:
            start_time = datetime.combine(trade_date, datetime.min.time())
            end_time = datetime.combine(trade_date, datetime.max.time())
            
            return StockMinute.query.filter(
                StockMinute.ts_code == ts_code,
                StockMinute.trade_time >= start_time,
                StockMinute.trade_time <= end_time
            ).order_by(StockMinute.trade_time).all()
        except Exception as e:
            logger.error(f"获取分钟行情数据失败: {str(e)}")
            return []
    
    @staticmethod
    def get_latest_by_ts_code(ts_code: str) -> Optional[StockMinute]:
        """
        获取指定股票的最新分钟数据
        :param ts_code: TS代码
        :return: 最新分钟数据
        """
        try:
            return StockMinute.query.filter_by(ts_code=ts_code)\
                .order_by(StockMinute.trade_time.desc())\
                .first()
        except Exception as e:
            logger.error(f"获取最新分钟数据失败: {str(e)}")
            return None
    
    @staticmethod
    def get_by_time_range(ts_code: str, start_time: datetime, end_time: datetime) -> List[StockMinute]:
        """
        根据时间范围获取分钟行情数据
        :param ts_code: TS代码
        :param start_time: 开始时间
        :param end_time: 结束时间
        :return: 分钟行情数据列表
        """
        try:
            return StockMinute.query.filter(
                StockMinute.ts_code == ts_code,
                StockMinute.trade_time >= start_time,
                StockMinute.trade_time <= end_time
            ).order_by(StockMinute.trade_time).all()
        except Exception as e:
            logger.error(f"获取分钟行情数据失败: {str(e)}")
            return []
    
    @staticmethod
    def get_recent_minutes(ts_code: str, minutes: int = 60) -> List[StockMinute]:
        """
        获取最近N分钟的行情数据
        :param ts_code: TS代码
        :param minutes: 分钟数
        :return: 分钟行情数据列表
        """
        try:
            end_time = datetime.now()
            start_time = end_time - timedelta(minutes=minutes)
            
            return StockMinute.query.filter(
                StockMinute.ts_code == ts_code,
                StockMinute.trade_time >= start_time,
                StockMinute.trade_time <= end_time
            ).order_by(StockMinute.trade_time).all()
        except Exception as e:
            logger.error(f"获取最近分钟数据失败: {str(e)}")
            return []
    
    @staticmethod
    def get_by_pct_chg_range(min_pct: float, max_pct: float, trade_date: date = None) -> List[StockMinute]:
        """
        根据涨跌幅范围获取分钟行情数据
        :param min_pct: 最小涨跌幅
        :param max_pct: 最大涨跌幅
        :param trade_date: 交易日期
        :return: 分钟行情数据列表
        """
        try:
            query = StockMinute.query.filter(
                StockMinute.pct_chg >= min_pct,
                StockMinute.pct_chg <= max_pct
            )
            
            if trade_date:
                start_time = datetime.combine(trade_date, datetime.min.time())
                end_time = datetime.combine(trade_date, datetime.max.time())
                query = query.filter(
                    StockMinute.trade_time >= start_time,
                    StockMinute.trade_time <= end_time
                )
            
            return query.order_by(StockMinute.pct_chg.desc()).all()
        except Exception as e:
            logger.error(f"获取分钟行情数据失败: {str(e)}")
            return []
    
    @staticmethod
    def get_by_vol_range(min_vol: int, max_vol: int, trade_date: date = None) -> List[StockMinute]:
        """
        根据成交量范围获取分钟行情数据
        :param min_vol: 最小成交量
        :param max_vol: 最大成交量
        :param trade_date: 交易日期
        :return: 分钟行情数据列表
        """
        try:
            query = StockMinute.query.filter(
                StockMinute.vol >= min_vol,
                StockMinute.vol <= max_vol
            )
            
            if trade_date:
                start_time = datetime.combine(trade_date, datetime.min.time())
                end_time = datetime.combine(trade_date, datetime.max.time())
                query = query.filter(
                    StockMinute.trade_time >= start_time,
                    StockMinute.trade_time <= end_time
                )
            
            return query.order_by(StockMinute.vol.desc()).all()
        except Exception as e:
            logger.error(f"获取分钟行情数据失败: {str(e)}")
            return []
    
    @staticmethod
    def create_or_update(data: Dict[str, Any]) -> Optional[StockMinute]:
        """
        创建或更新分钟行情数据
        :param data: 分钟行情数据
        :return: 分钟行情数据对象
        """
        try:
            ts_code = data.get('ts_code')
            trade_time_str = data.get('trade_time')
            
            if not ts_code or not trade_time_str:
                logger.error("缺少必要参数: ts_code 或 trade_time")
                return None
            
            # 转换时间
            if isinstance(trade_time_str, str):
                trade_time = datetime.strptime(trade_time_str, '%Y%m%d%H%M%S')
            else:
                trade_time = trade_time_str
            
            # 查找现有记录
            existing = StockMinute.query.filter_by(
                ts_code=ts_code,
                trade_time=trade_time
            ).first()
            
            if existing:
                # 更新现有记录
                for key, value in data.items():
                    if hasattr(existing, key) and key not in ['ts_code', 'trade_time']:
                        setattr(existing, key, value)
                existing.updated_at = datetime.now()
                db.session.commit()
                logger.info(f"更新分钟行情数据: {ts_code} {trade_time}")
                return existing
            else:
                # 创建新记录
                minute_data = StockMinute(
                    ts_code=ts_code,
                    trade_time=trade_time,
                    open=data.get('open'),
                    high=data.get('high'),
                    low=data.get('low'),
                    close=data.get('close'),
                    pre_close=data.get('pre_close'),
                    change=data.get('change'),
                    pct_chg=data.get('pct_chg'),
                    vol=data.get('vol'),
                    amount=data.get('amount')
                )
                db.session.add(minute_data)
                db.session.commit()
                logger.info(f"创建分钟行情数据: {ts_code} {trade_time}")
                return minute_data
                
        except Exception as e:
            logger.error(f"创建或更新分钟行情数据失败: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def batch_create_or_update(data_list: List[Dict[str, Any]]) -> int:
        """
        批量创建或更新分钟行情数据
        :param data_list: 分钟行情数据列表
        :return: 成功处理的数量
        """
        success_count = 0
        try:
            for data in data_list:
                if StockMinuteService.create_or_update(data):
                    success_count += 1
            logger.info(f"批量处理分钟行情数据完成，成功: {success_count}/{len(data_list)}")
            return success_count
        except Exception as e:
            logger.error(f"批量处理分钟行情数据失败: {str(e)}")
            return success_count

# 创建全局服务实例
stock_minute_service = StockMinuteService() 