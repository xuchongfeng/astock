from app import db
from app.models.stock_name_change import StockNameChange
from datetime import datetime, date
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class StockNameChangeService:
    """股票曾用名服务类"""
    
    @staticmethod
    def get_by_ts_code(ts_code: str) -> List[StockNameChange]:
        """
        根据TS代码获取股票曾用名
        :param ts_code: TS代码
        :return: 股票曾用名列表
        """
        try:
            return StockNameChange.query.filter_by(ts_code=ts_code)\
                .order_by(StockNameChange.start_date.desc()).all()
        except Exception as e:
            logger.error(f"获取股票曾用名失败: {str(e)}")
            return []
    
    @staticmethod
    def get_by_name(name: str) -> List[StockNameChange]:
        """
        根据股票名称获取曾用名记录
        :param name: 股票名称
        :return: 股票曾用名列表
        """
        try:
            return StockNameChange.query.filter_by(name=name)\
                .order_by(StockNameChange.start_date.desc()).all()
        except Exception as e:
            logger.error(f"获取股票曾用名失败: {str(e)}")
            return []
    
    @staticmethod
    def get_by_date_range(start_date: date, end_date: date) -> List[StockNameChange]:
        """
        根据日期范围获取股票曾用名
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: 股票曾用名列表
        """
        try:
            return StockNameChange.query.filter(
                StockNameChange.start_date >= start_date,
                StockNameChange.start_date <= end_date
            ).order_by(StockNameChange.start_date.desc()).all()
        except Exception as e:
            logger.error(f"获取股票曾用名失败: {str(e)}")
            return []
    
    @staticmethod
    def get_current_name(ts_code: str, check_date: date = None) -> Optional[StockNameChange]:
        """
        获取指定日期的股票名称
        :param ts_code: TS代码
        :param check_date: 检查日期
        :return: 股票名称记录
        """
        try:
            if check_date is None:
                check_date = date.today()
            
            return StockNameChange.query.filter(
                StockNameChange.ts_code == ts_code,
                StockNameChange.start_date <= check_date,
                (StockNameChange.end_date.is_(None) | (StockNameChange.end_date >= check_date))
            ).order_by(StockNameChange.start_date.desc()).first()
        except Exception as e:
            logger.error(f"获取当前股票名称失败: {str(e)}")
            return None
    
    @staticmethod
    def create_or_update(data: Dict[str, Any]) -> Optional[StockNameChange]:
        """
        创建或更新股票曾用名
        :param data: 股票曾用名数据
        :return: 股票曾用名对象
        """
        try:
            ts_code = data.get('ts_code')
            name = data.get('name')
            
            if not ts_code or not name:
                logger.error("缺少必要参数: ts_code 或 name")
                return None
            
            # 转换日期
            start_date = data.get('start_date')
            if start_date and isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y%m%d').date()
            
            end_date = data.get('end_date')
            if end_date and isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y%m%d').date()
            
            ann_date = data.get('ann_date')
            if ann_date and isinstance(ann_date, str):
                ann_date = datetime.strptime(ann_date, '%Y%m%d').date()
            
            # 查找现有记录
            existing = StockNameChange.query.filter_by(
                ts_code=ts_code,
                name=name,
                start_date=start_date
            ).first()
            
            if existing:
                # 更新现有记录
                existing.end_date = end_date
                existing.ann_date = ann_date
                existing.updated_at = datetime.now()
                db.session.commit()
                logger.info(f"更新股票曾用名: {ts_code} {name}")
                return existing
            else:
                # 创建新记录
                name_change = StockNameChange(
                    ts_code=ts_code,
                    name=name,
                    start_date=start_date,
                    end_date=end_date,
                    ann_date=ann_date
                )
                db.session.add(name_change)
                db.session.commit()
                logger.info(f"创建股票曾用名: {ts_code} {name}")
                return name_change
                
        except Exception as e:
            logger.error(f"创建或更新股票曾用名失败: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def batch_create_or_update(data_list: List[Dict[str, Any]]) -> int:
        """
        批量创建或更新股票曾用名
        :param data_list: 股票曾用名数据列表
        :return: 成功处理的数量
        """
        success_count = 0
        try:
            for data in data_list:
                if StockNameChangeService.create_or_update(data):
                    success_count += 1
            logger.info(f"批量处理股票曾用名完成，成功: {success_count}/{len(data_list)}")
            return success_count
        except Exception as e:
            logger.error(f"批量处理股票曾用名失败: {str(e)}")
            return success_count

# 创建全局服务实例
stock_name_change_service = StockNameChangeService() 