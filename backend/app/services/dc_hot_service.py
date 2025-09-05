from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.dc_hot import DcHot
from app import db
import logging

logger = logging.getLogger(__name__)

class DcHotService:
    def __init__(self, db_session=None):
        # 使用全局db实例
        pass
    
    def get_dc_hot_list(
        self,
        page: int = 1,
        page_size: int = 20,
        trade_date: Optional[str] = None,
        ts_code: Optional[str] = None,
        market: Optional[str] = None,
        hot_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取东方财富热榜数据列表
        """
        try:
            query = db.query(DcHot)
            
            # 添加过滤条件
            if trade_date:
                query = query.filter(DcHot.trade_date == trade_date)
            
            if ts_code:
                query = query.filter(DcHot.ts_code == ts_code)
            
            if market:
                query = query.filter(DcHot.market == market)
            
            if hot_type:
                query = query.filter(DcHot.hot_type == hot_type)
            
            if search:
                search_filter = or_(
                    DcHot.ts_code.like(f"%{search}%"),
                    DcHot.ts_name.like(f"%{search}%")
                )
                query = query.filter(search_filter)
            
            # 按排行排序
            query = query.order_by(asc(DcHot.rank))
            
            # 计算总数
            total = query.count()
            
            # 分页
            offset = (page - 1) * page_size
            data = query.offset(offset).limit(page_size).all()
            
            return {
                "data": data,
                "total": total,
                "page": page,
                "page_size": page_size
            }
            
        except Exception as e:
            logger.error(f"获取东方财富热榜数据失败: {str(e)}")
            raise e
    
    def get_latest_dc_hot(self, market: str = "A股市场", hot_type: str = "人气榜") -> List[DcHot]:
        """
        获取最新的东方财富热榜数据
        """
        try:
            # 获取最新的交易日期
            latest_date = db.query(DcHot.trade_date)\
                .filter(and_(DcHot.market == market, DcHot.hot_type == hot_type))\
                .order_by(desc(DcHot.trade_date))\
                .first()
            
            if not latest_date:
                return []
            
            # 获取该日期下的所有数据
            data = db.query(DcHot)\
                .filter(and_(
                    DcHot.trade_date == latest_date[0],
                    DcHot.market == market,
                    DcHot.hot_type == hot_type
                ))\
                .order_by(asc(DcHot.rank))\
                .all()
            
            return data
            
        except Exception as e:
            logger.error(f"获取最新东方财富热榜数据失败: {str(e)}")
            raise e
    
    def get_markets(self) -> List[str]:
        """
        获取可用的市场类型列表
        """
        try:
            markets = db.query(DcHot.market)\
                .distinct()\
                .filter(DcHot.market.isnot(None))\
                .all()
            
            return [market[0] for market in markets if market[0]]
            
        except Exception as e:
            logger.error(f"获取市场类型列表失败: {str(e)}")
            raise e
    
    def get_hot_types(self) -> List[str]:
        """
        获取可用的热点类型列表
        """
        try:
            hot_types = db.query(DcHot.hot_type)\
                .distinct()\
                .filter(DcHot.hot_type.isnot(None))\
                .all()
            
            return [hot_type[0] for hot_type in hot_types if hot_type[0]]
            
        except Exception as e:
            logger.error(f"获取热点类型列表失败: {str(e)}")
            raise e
    
    def create_dc_hot(self, dc_hot_data: Dict[str, Any]) -> DcHot:
        """
        创建东方财富热榜数据
        """
        try:
            dc_hot = DcHot(**dc_hot_data)
            db.session.add(dc_hot)
            db.session.commit()
            db.session.refresh(dc_hot)
            return dc_hot
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"创建东方财富热榜数据失败: {str(e)}")
            raise e
    
    def update_dc_hot(self, dc_hot_id: int, update_data: Dict[str, Any]) -> Optional[DcHot]:
        """
        更新东方财富热榜数据
        """
        try:
            dc_hot = db.query(DcHot).filter(DcHot.id == dc_hot_id).first()
            if not dc_hot:
                return None
            
            for key, value in update_data.items():
                if hasattr(dc_hot, key):
                    setattr(dc_hot, key, value)
            
            dc_hot.updated_at = datetime.now()
            db.session.commit()
            db.session.refresh(dc_hot)
            return dc_hot
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"更新东方财富热榜数据失败: {str(e)}")
            raise e
    
    def delete_dc_hot(self, dc_hot_id: int) -> bool:
        """
        删除东方财富热榜数据
        """
        try:
            dc_hot = db.query(DcHot).filter(DcHot.id == dc_hot_id).first()
            if not dc_hot:
                return False
            
            db.session.delete(dc_hot)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"删除东方财富热榜数据失败: {str(e)}")
            raise e
    
    def get_dc_hot_by_id(self, dc_hot_id: int) -> Optional[DcHot]:
        """
        根据ID获取东方财富热榜数据
        """
        try:
            return db.query(DcHot).filter(DcHot.id == dc_hot_id).first()
        except Exception as e:
            logger.error(f"根据ID获取东方财富热榜数据失败: {str(e)}")
            raise e
