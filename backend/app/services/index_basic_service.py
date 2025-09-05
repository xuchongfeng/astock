from app.models.index_basic import IndexBasic
from app import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class IndexBasicService:
    
    @staticmethod
    def get_all_index_basic():
        """获取所有指数基本信息"""
        try:
            indices = IndexBasic.query.all()
            return [index.as_dict() for index in indices]
        except Exception as e:
            logger.error(f"获取指数基本信息失败: {e}")
            return []
    
    @staticmethod
    def get_index_basic_by_ts_code(ts_code):
        """根据TS代码获取指数基本信息"""
        try:
            index = IndexBasic.query.filter_by(ts_code=ts_code).first()
            return index.as_dict() if index else None
        except Exception as e:
            logger.error(f"根据TS代码获取指数基本信息失败: {e}")
            return None
    
    @staticmethod
    def get_index_basic_by_market(market):
        """根据市场获取指数基本信息"""
        try:
            indices = IndexBasic.query.filter_by(market=market).all()
            return [index.as_dict() for index in indices]
        except Exception as e:
            logger.error(f"根据市场获取指数基本信息失败: {e}")
            return []
    
    @staticmethod
    def get_index_basic_by_publisher(publisher):
        """根据发布方获取指数基本信息"""
        try:
            indices = IndexBasic.query.filter_by(publisher=publisher).all()
            return [index.as_dict() for index in indices]
        except Exception as e:
            logger.error(f"根据发布方获取指数基本信息失败: {e}")
            return []
    
    @staticmethod
    def get_index_basic_by_category(category):
        """根据指数类别获取指数基本信息"""
        try:
            indices = IndexBasic.query.filter_by(category=category).all()
            return [index.as_dict() for index in indices]
        except Exception as e:
            logger.error(f"根据指数类别获取指数基本信息失败: {e}")
            return []
    
    @staticmethod
    def search_index_basic(keyword):
        """搜索指数基本信息"""
        try:
            indices = IndexBasic.query.filter(
                db.or_(
                    IndexBasic.name.like(f'%{keyword}%'),
                    IndexBasic.fullname.like(f'%{keyword}%'),
                    IndexBasic.ts_code.like(f'%{keyword}%')
                )
            ).all()
            return [index.as_dict() for index in indices]
        except Exception as e:
            logger.error(f"搜索指数基本信息失败: {e}")
            return []
    
    @staticmethod
    def create_index_basic(data):
        """创建指数基本信息"""
        try:
            index = IndexBasic(**data)
            db.session.add(index)
            db.session.commit()
            return index.as_dict()
        except Exception as e:
            db.session.rollback()
            logger.error(f"创建指数基本信息失败: {e}")
            return None
    
    @staticmethod
    def update_index_basic(ts_code, data):
        """更新指数基本信息"""
        try:
            index = IndexBasic.query.filter_by(ts_code=ts_code).first()
            if not index:
                return None
            
            for key, value in data.items():
                if hasattr(index, key):
                    setattr(index, key, value)
            
            index.updated_at = datetime.now()
            db.session.commit()
            return index.as_dict()
        except Exception as e:
            db.session.rollback()
            logger.error(f"更新指数基本信息失败: {e}")
            return None
    
    @staticmethod
    def delete_index_basic(ts_code):
        """删除指数基本信息"""
        try:
            index = IndexBasic.query.filter_by(ts_code=ts_code).first()
            if not index:
                return False
            
            db.session.delete(index)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"删除指数基本信息失败: {e}")
            return False
