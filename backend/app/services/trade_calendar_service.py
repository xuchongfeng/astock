from app import db
from app.models.trade_calendar import TradeCalendar
from datetime import datetime, date
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class TradeCalendarService:
    """交易日历服务类"""
    
    @staticmethod
    def get_by_exchange(exchange: str, start_date: date = None, end_date: date = None) -> List[TradeCalendar]:
        """
        根据交易所获取交易日历
        :param exchange: 交易所代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: 交易日历列表
        """
        try:
            query = TradeCalendar.query.filter_by(exchange=exchange)
            
            if start_date:
                query = query.filter(TradeCalendar.cal_date >= start_date)
            if end_date:
                query = query.filter(TradeCalendar.cal_date <= end_date)
            
            return query.order_by(TradeCalendar.cal_date).all()
        except Exception as e:
            logger.error(f"获取交易日历失败: {str(e)}")
            return []
    
    @staticmethod
    def get_trading_days(exchange: str, start_date: date = None, end_date: date = None) -> List[TradeCalendar]:
        """
        获取交易日列表
        :param exchange: 交易所代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: 交易日列表
        """
        try:
            query = TradeCalendar.query.filter_by(exchange=exchange, is_open=True)
            
            if start_date:
                query = query.filter(TradeCalendar.cal_date >= start_date)
            if end_date:
                query = query.filter(TradeCalendar.cal_date <= end_date)
            
            return query.order_by(TradeCalendar.cal_date).all()
        except Exception as e:
            logger.error(f"获取交易日失败: {str(e)}")
            return []
    
    @staticmethod
    def is_trading_day(exchange: str, check_date: date) -> bool:
        """
        判断是否为交易日
        :param exchange: 交易所代码
        :param check_date: 检查日期
        :return: 是否为交易日
        """
        try:
            calendar = TradeCalendar.query.filter_by(
                exchange=exchange,
                cal_date=check_date
            ).first()
            
            return calendar.is_open if calendar else False
        except Exception as e:
            logger.error(f"判断交易日失败: {str(e)}")
            return False
    
    @staticmethod
    def get_next_trading_day(exchange: str, from_date: date) -> Optional[TradeCalendar]:
        """
        获取下一个交易日
        :param exchange: 交易所代码
        :param from_date: 起始日期
        :return: 下一个交易日
        """
        try:
            return TradeCalendar.query.filter(
                TradeCalendar.exchange == exchange,
                TradeCalendar.cal_date > from_date,
                TradeCalendar.is_open == True
            ).order_by(TradeCalendar.cal_date).first()
        except Exception as e:
            logger.error(f"获取下一个交易日失败: {str(e)}")
            return None
    
    @staticmethod
    def get_prev_trading_day(exchange: str, from_date: date) -> Optional[TradeCalendar]:
        """
        获取上一个交易日
        :param exchange: 交易所代码
        :param from_date: 起始日期
        :return: 上一个交易日
        """
        try:
            return TradeCalendar.query.filter(
                TradeCalendar.exchange == exchange,
                TradeCalendar.cal_date < from_date,
                TradeCalendar.is_open == True
            ).order_by(TradeCalendar.cal_date.desc()).first()
        except Exception as e:
            logger.error(f"获取上一个交易日失败: {str(e)}")
            return None
    
    @staticmethod
    def create_or_update(data: Dict[str, Any]) -> Optional[TradeCalendar]:
        """
        创建或更新交易日历
        :param data: 交易日历数据
        :return: 交易日历对象
        """
        try:
            exchange = data.get('exchange')
            cal_date_str = data.get('cal_date')
            
            if not exchange or not cal_date_str:
                logger.error("缺少必要参数: exchange 或 cal_date")
                return None
            
            # 转换日期
            if isinstance(cal_date_str, str):
                cal_date = datetime.strptime(cal_date_str, '%Y%m%d').date()
            else:
                cal_date = cal_date_str
            
            # 查找现有记录
            existing = TradeCalendar.query.filter_by(
                exchange=exchange,
                cal_date=cal_date
            ).first()
            
            if existing:
                # 更新现有记录
                existing.is_open = data.get('is_open', existing.is_open)
                existing.pretrade_date = data.get('pretrade_date')
                existing.updated_at = datetime.now()
                db.session.commit()
                logger.info(f"更新交易日历: {exchange} {cal_date}")
                return existing
            else:
                # 创建新记录
                pretrade_date = data.get('pretrade_date')
                if pretrade_date and isinstance(pretrade_date, str):
                    pretrade_date = datetime.strptime(pretrade_date, '%Y%m%d').date()
                
                calendar = TradeCalendar(
                    exchange=exchange,
                    cal_date=cal_date,
                    is_open=data.get('is_open', False),
                    pretrade_date=pretrade_date
                )
                db.session.add(calendar)
                db.session.commit()
                logger.info(f"创建交易日历: {exchange} {cal_date}")
                return calendar
                
        except Exception as e:
            logger.error(f"创建或更新交易日历失败: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def batch_create_or_update(data_list: List[Dict[str, Any]]) -> int:
        """
        批量创建或更新交易日历
        :param data_list: 交易日历数据列表
        :return: 成功处理的数量
        """
        success_count = 0
        try:
            for data in data_list:
                if TradeCalendarService.create_or_update(data):
                    success_count += 1
            logger.info(f"批量处理交易日历完成，成功: {success_count}/{len(data_list)}")
            return success_count
        except Exception as e:
            logger.error(f"批量处理交易日历失败: {str(e)}")
            return success_count

# 创建全局服务实例
trade_calendar_service = TradeCalendarService() 