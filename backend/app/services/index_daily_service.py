from app.models.index_daily import IndexDaily
from app import db
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class IndexDailyService:
    
    @staticmethod
    def get_all_index_daily():
        """获取所有指数日线行情"""
        try:
            daily_data = IndexDaily.query.all()
            return [data.as_dict() for data in daily_data]
        except Exception as e:
            logger.error(f"获取指数日线行情失败: {e}")
            return []
    
    @staticmethod
    def get_index_daily_by_ts_code(ts_code, limit=None):
        """根据TS代码获取指数日线行情"""
        try:
            query = IndexDaily.query.filter_by(ts_code=ts_code).order_by(IndexDaily.trade_date.desc())
            if limit:
                query = query.limit(limit)
            daily_data = query.all()
            return [data.as_dict() for data in daily_data]
        except Exception as e:
            logger.error(f"根据TS代码获取指数日线行情失败: {e}")
            return []
    
    @staticmethod
    def get_index_daily_by_date_range(ts_code, start_date, end_date):
        """根据日期范围获取指数日线行情"""
        try:
            daily_data = IndexDaily.query.filter(
                IndexDaily.ts_code == ts_code,
                IndexDaily.trade_date >= start_date,
                IndexDaily.trade_date <= end_date
            ).order_by(IndexDaily.trade_date.asc()).all()
            return [data.as_dict() for data in daily_data]
        except Exception as e:
            logger.error(f"根据日期范围获取指数日线行情失败: {e}")
            return []
    
    @staticmethod
    def get_index_daily_by_trade_date(trade_date):
        """根据交易日期获取所有指数日线行情"""
        try:
            daily_data = IndexDaily.query.filter_by(trade_date=trade_date).all()
            return [data.as_dict() for data in daily_data]
        except Exception as e:
            logger.error(f"根据交易日期获取指数日线行情失败: {e}")
            return []
    
    @staticmethod
    def get_latest_index_daily(ts_code):
        """获取指定指数的最新日线行情"""
        try:
            latest_data = IndexDaily.query.filter_by(ts_code=ts_code).order_by(IndexDaily.trade_date.desc()).first()
            return latest_data.as_dict() if latest_data else None
        except Exception as e:
            logger.error(f"获取指定指数的最新日线行情失败: {e}")
            return None
    
    @staticmethod
    def get_index_daily_statistics(ts_code, days=30):
        """获取指定指数的统计信息"""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            daily_data = IndexDaily.query.filter(
                IndexDaily.ts_code == ts_code,
                IndexDaily.trade_date >= start_date,
                IndexDaily.trade_date <= end_date
            ).order_by(IndexDaily.trade_date.asc()).all()
            
            if not daily_data:
                return None
            
            # 计算统计信息
            prices = [float(data.close) if data.close else 0 for data in daily_data]
            volumes = [float(data.vol) if data.vol else 0 for data in daily_data]
            amounts = [float(data.amount) if data.amount else 0 for data in daily_data]
            
            stats = {
                'ts_code': ts_code,
                'period_days': days,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'max_price': max(prices) if prices else 0,
                'min_price': min(prices) if prices else 0,
                'avg_price': sum(prices) / len(prices) if prices else 0,
                'total_volume': sum(volumes),
                'total_amount': sum(amounts),
                'price_change': float(daily_data[-1].close) - float(daily_data[0].close) if daily_data else 0,
                'price_change_pct': ((float(daily_data[-1].close) - float(daily_data[0].close)) / float(daily_data[0].close) * 100) if daily_data and daily_data[0].close else 0
            }
            
            return stats
        except Exception as e:
            logger.error(f"获取指定指数的统计信息失败: {e}")
            return None
    
    @staticmethod
    def create_index_daily(data):
        """创建指数日线行情"""
        try:
            daily_data = IndexDaily(**data)
            db.session.add(daily_data)
            db.session.commit()
            return daily_data.as_dict()
        except Exception as e:
            db.session.rollback()
            logger.error(f"创建指数日线行情失败: {e}")
            return None
    
    @staticmethod
    def batch_create_index_daily(data_list):
        """批量创建指数日线行情"""
        try:
            for data in data_list:
                daily_data = IndexDaily(**data)
                db.session.add(daily_data)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"批量创建指数日线行情失败: {e}")
            return False
    
    @staticmethod
    def update_index_daily(ts_code, trade_date, data):
        """更新指数日线行情"""
        try:
            daily_data = IndexDaily.query.filter_by(
                ts_code=ts_code,
                trade_date=trade_date
            ).first()
            
            if not daily_data:
                return None
            
            for key, value in data.items():
                if hasattr(daily_data, key):
                    setattr(daily_data, key, value)
            
            daily_data.updated_at = datetime.now()
            db.session.commit()
            return daily_data.as_dict()
        except Exception as e:
            db.session.rollback()
            logger.error(f"更新指数日线行情失败: {e}")
            return None
    
    @staticmethod
    def delete_index_daily(ts_code, trade_date):
        """删除指数日线行情"""
        try:
            daily_data = IndexDaily.query.filter_by(
                ts_code=ts_code,
                trade_date=trade_date
            ).first()
            
            if not daily_data:
                return False
            
            db.session.delete(daily_data)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"删除指数日线行情失败: {e}")
            return False
