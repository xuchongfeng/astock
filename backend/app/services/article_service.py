from typing import List, Dict, Optional
from datetime import datetime
from app import db
from app.models.article import Article
from app.models.user import User
from sqlalchemy import desc, asc, and_, or_
import logging

logger = logging.getLogger(__name__)

class ArticleService:
    """文章服务类"""
    
    def get_all_articles(self, filters: Dict = None, query_only: bool = False):
        """
        获取所有文章
        :param filters: 过滤条件
        :param query_only: 是否只返回查询对象
        :return: 文章列表或查询对象
        """
        try:
            query = Article.query
            
            if filters:
                # 按用户ID过滤
                if 'user_id' in filters:
                    query = query.filter(Article.user_id == filters['user_id'])
                
                # 按状态过滤
                if 'status' in filters:
                    query = query.filter(Article.status == filters['status'])
                
                # 按分类过滤
                if 'category' in filters:
                    query = query.filter(Article.category == filters['category'])
                
                # 按是否公开过滤
                if 'is_public' in filters:
                    query = query.filter(Article.is_public == filters['is_public'])
                
                # 按标签过滤
                if 'tags' in filters:
                    query = query.filter(Article.tags.like(f"%{filters['tags']}%"))
                
                # 按标题搜索
                if 'title' in filters:
                    query = query.filter(Article.title.like(f"%{filters['title']}%"))
                
                # 按内容搜索
                if 'content' in filters:
                    query = query.filter(Article.content.like(f"%{filters['content']}%"))
            
            # 默认按创建时间倒序排列
            query = query.order_by(desc(Article.created_at))
            
            if query_only:
                return query
            
            return query.all()
            
        except Exception as e:
            logger.error(f"获取文章列表失败: {str(e)}")
            return []
    
    def get_article_by_id(self, article_id: int) -> Optional[Article]:
        """
        根据ID获取文章
        :param article_id: 文章ID
        :return: 文章对象
        """
        try:
            return Article.query.get(article_id)
        except Exception as e:
            logger.error(f"获取文章失败: {str(e)}")
            return None
    
    def create_article(self, data: Dict) -> Optional[Article]:
        """
        创建文章
        :param data: 文章数据
        :return: 创建的文章对象
        """
        try:
            article = Article(
                user_id=data.get('user_id'),
                title=data.get('title'),
                content=data.get('content'),
                summary=data.get('summary', ''),
                tags=','.join(data.get('tags', [])) if isinstance(data.get('tags'), list) else data.get('tags', ''),
                category=data.get('category', '投资思路'),
                status=data.get('status', 'draft'),
                is_public=data.get('is_public', False)
            )
            
            db.session.add(article)
            db.session.commit()
            
            logger.info(f"创建文章成功: {article.id}")
            return article
            
        except Exception as e:
            logger.error(f"创建文章失败: {str(e)}")
            db.session.rollback()
            return None
    
    def update_article(self, article_id: int, data: Dict) -> Optional[Article]:
        """
        更新文章
        :param article_id: 文章ID
        :param data: 更新数据
        :return: 更新后的文章对象
        """
        try:
            article = Article.query.get(article_id)
            if not article:
                return None
            
            # 更新字段
            if 'title' in data:
                article.title = data['title']
            if 'content' in data:
                article.content = data['content']
            if 'summary' in data:
                article.summary = data['summary']
            if 'tags' in data:
                article.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
            if 'category' in data:
                article.category = data['category']
            if 'status' in data:
                article.status = data['status']
                # 如果状态改为已发布，设置发布时间
                if data['status'] == 'published' and not article.published_at:
                    article.published_at = datetime.utcnow()
            if 'is_public' in data:
                article.is_public = data['is_public']
            
            article.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            logger.info(f"更新文章成功: {article_id}")
            return article
            
        except Exception as e:
            logger.error(f"更新文章失败: {str(e)}")
            db.session.rollback()
            return None
    
    def delete_article(self, article_id: int) -> bool:
        """
        删除文章
        :param article_id: 文章ID
        :return: 是否删除成功
        """
        try:
            article = Article.query.get(article_id)
            if not article:
                return False
            
            db.session.delete(article)
            db.session.commit()
            
            logger.info(f"删除文章成功: {article_id}")
            return True
            
        except Exception as e:
            logger.error(f"删除文章失败: {str(e)}")
            db.session.rollback()
            return False
    
    def increment_view_count(self, article_id: int) -> bool:
        """
        增加文章浏览次数
        :param article_id: 文章ID
        :return: 是否成功
        """
        try:
            article = Article.query.get(article_id)
            if not article:
                return False
            
            article.view_count += 1
            db.session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"增加浏览次数失败: {str(e)}")
            db.session.rollback()
            return False
    
    def increment_like_count(self, article_id: int) -> bool:
        """
        增加文章点赞次数
        :param article_id: 文章ID
        :return: 是否成功
        """
        try:
            article = Article.query.get(article_id)
            if not article:
                return False
            
            article.like_count += 1
            db.session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"增加点赞次数失败: {str(e)}")
            db.session.rollback()
            return False
    
    def get_user_articles(self, user_id: int, status: str = None) -> List[Article]:
        """
        获取用户文章
        :param user_id: 用户ID
        :param status: 状态过滤
        :return: 文章列表
        """
        try:
            query = Article.query.filter(Article.user_id == user_id)
            
            if status:
                query = query.filter(Article.status == status)
            
            return query.order_by(desc(Article.created_at)).all()
            
        except Exception as e:
            logger.error(f"获取用户文章失败: {str(e)}")
            return []
    
    def get_public_articles(self, limit: int = 20, offset: int = 0) -> List[Article]:
        """
        获取公开文章
        :param limit: 限制数量
        :param offset: 偏移量
        :return: 文章列表
        """
        try:
            return Article.query.filter(
                and_(
                    Article.is_public == True,
                    Article.status == 'published'
                )
            ).order_by(desc(Article.published_at)).offset(offset).limit(limit).all()
            
        except Exception as e:
            logger.error(f"获取公开文章失败: {str(e)}")
            return []
    
    def get_article_statistics(self, user_id: int) -> Dict:
        """
        获取用户文章统计
        :param user_id: 用户ID
        :return: 统计信息
        """
        try:
            total = Article.query.filter(Article.user_id == user_id).count()
            published = Article.query.filter(
                and_(Article.user_id == user_id, Article.status == 'published')
            ).count()
            draft = Article.query.filter(
                and_(Article.user_id == user_id, Article.status == 'draft')
            ).count()
            archived = Article.query.filter(
                and_(Article.user_id == user_id, Article.status == 'archived')
            ).count()
            
            return {
                'total': total,
                'published': published,
                'draft': draft,
                'archived': archived
            }
            
        except Exception as e:
            logger.error(f"获取文章统计失败: {str(e)}")
            return {
                'total': 0,
                'published': 0,
                'draft': 0,
                'archived': 0
            }

# 创建全局服务实例
article_service = ArticleService()
