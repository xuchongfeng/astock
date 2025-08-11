from app import db
from app.models.ipo_stock import IpoStock
from datetime import datetime, date
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class IpoStockService:
    """IPO新股服务类"""
    
    @staticmethod
    def get_by_ts_code(ts_code: str) -> Optional[IpoStock]:
        """
        根据TS代码获取IPO信息
        :param ts_code: TS代码
        :return: IPO信息
        """
        try:
            return IpoStock.query.filter_by(ts_code=ts_code).first()
        except Exception as e:
            logger.error(f"获取IPO信息失败: {str(e)}")
            return None
    
    @staticmethod
    def get_by_date_range(start_date: date = None, end_date: date = None) -> List[IpoStock]:
        """
        根据日期范围获取IPO信息
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: IPO信息列表
        """
        try:
            query = IpoStock.query
            
            if start_date:
                query = query.filter(IpoStock.ipo_date >= start_date)
            if end_date:
                query = query.filter(IpoStock.ipo_date <= end_date)
            
            return query.order_by(IpoStock.ipo_date.desc()).all()
        except Exception as e:
            logger.error(f"获取IPO信息失败: {str(e)}")
            return []
    
    @staticmethod
    def get_by_issue_date_range(start_date: date = None, end_date: date = None) -> List[IpoStock]:
        """
        根据发行日期范围获取IPO信息
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: IPO信息列表
        """
        try:
            query = IpoStock.query
            
            if start_date:
                query = query.filter(IpoStock.issue_date >= start_date)
            if end_date:
                query = query.filter(IpoStock.issue_date <= end_date)
            
            return query.order_by(IpoStock.issue_date.desc()).all()
        except Exception as e:
            logger.error(f"获取IPO信息失败: {str(e)}")
            return []
    
    @staticmethod
    def get_by_pe_range(min_pe: float, max_pe: float) -> List[IpoStock]:
        """
        根据市盈率范围获取IPO信息
        :param min_pe: 最小市盈率
        :param max_pe: 最大市盈率
        :return: IPO信息列表
        """
        try:
            return IpoStock.query.filter(
                IpoStock.pe >= min_pe,
                IpoStock.pe <= max_pe
            ).order_by(IpoStock.pe).all()
        except Exception as e:
            logger.error(f"获取IPO信息失败: {str(e)}")
            return []
    
    @staticmethod
    def get_by_price_range(min_price: float, max_price: float) -> List[IpoStock]:
        """
        根据发行价格范围获取IPO信息
        :param min_price: 最小价格
        :param max_price: 最大价格
        :return: IPO信息列表
        """
        try:
            return IpoStock.query.filter(
                IpoStock.price >= min_price,
                IpoStock.price <= max_price
            ).order_by(IpoStock.price).all()
        except Exception as e:
            logger.error(f"获取IPO信息失败: {str(e)}")
            return []
    
    @staticmethod
    def get_recent_ipo(days: int = 30) -> List[IpoStock]:
        """
        获取最近上市的IPO信息
        :param days: 天数
        :return: IPO信息列表
        """
        try:
            from datetime import timedelta
            start_date = date.today() - timedelta(days=days)
            
            return IpoStock.query.filter(
                IpoStock.ipo_date >= start_date
            ).order_by(IpoStock.ipo_date.desc()).all()
        except Exception as e:
            logger.error(f"获取最近IPO信息失败: {str(e)}")
            return []
    
    @staticmethod
    def create_or_update(data: Dict[str, Any]) -> Optional[IpoStock]:
        """
        创建或更新IPO信息
        :param data: IPO数据
        :return: IPO对象
        """
        try:
            ts_code = data.get('ts_code')
            
            if not ts_code:
                logger.error("缺少必要参数: ts_code")
                return None
            
            # 转换日期
            ipo_date = data.get('ipo_date')
            if ipo_date and isinstance(ipo_date, str):
                ipo_date = datetime.strptime(ipo_date, '%Y%m%d').date()
            
            issue_date = data.get('issue_date')
            if issue_date and isinstance(issue_date, str):
                issue_date = datetime.strptime(issue_date, '%Y%m%d').date()
            
            # 查找现有记录
            existing = IpoStock.query.filter_by(ts_code=ts_code).first()
            
            if existing:
                # 更新现有记录
                for key, value in data.items():
                    if hasattr(existing, key) and key not in ['ts_code']:
                        if key in ['ipo_date', 'issue_date'] and isinstance(value, str):
                            value = datetime.strptime(value, '%Y%m%d').date()
                        setattr(existing, key, value)
                existing.updated_at = datetime.now()
                db.session.commit()
                logger.info(f"更新IPO信息: {ts_code}")
                return existing
            else:
                # 创建新记录
                ipo_stock = IpoStock(
                    ts_code=ts_code,
                    name=data.get('name'),
                    ipo_date=ipo_date,
                    issue_date=issue_date,
                    amount=data.get('amount'),
                    market_amount=data.get('market_amount'),
                    price=data.get('price'),
                    pe=data.get('pe'),
                    limit_amount=data.get('limit_amount'),
                    funds=data.get('funds'),
                    ballot=data.get('ballot')
                )
                db.session.add(ipo_stock)
                db.session.commit()
                logger.info(f"创建IPO信息: {ts_code}")
                return ipo_stock
                
        except Exception as e:
            logger.error(f"创建或更新IPO信息失败: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def batch_create_or_update(data_list: List[Dict[str, Any]]) -> int:
        """
        批量创建或更新IPO信息
        :param data_list: IPO数据列表
        :return: 成功处理的数量
        """
        success_count = 0
        try:
            for data in data_list:
                if IpoStockService.create_or_update(data):
                    success_count += 1
            logger.info(f"批量处理IPO信息完成，成功: {success_count}/{len(data_list)}")
            return success_count
        except Exception as e:
            logger.error(f"批量处理IPO信息失败: {str(e)}")
            return success_count

# 创建全局服务实例
ipo_stock_service = IpoStockService() 