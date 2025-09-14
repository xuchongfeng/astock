from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Article(db.Model):
    """文章模型"""
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, comment='用户ID')
    title = Column(String(200), nullable=False, comment='文章标题')
    content = Column(Text, nullable=False, comment='文章内容')
    summary = Column(Text, comment='文章摘要')
    tags = Column(String(500), comment='标签，用逗号分隔')
    category = Column(String(50), default='投资思路', comment='文章分类')
    status = Column(String(20), default='draft', comment='状态：draft-草稿，published-已发布，archived-已归档')
    is_public = Column(Boolean, default=False, comment='是否公开')
    view_count = Column(Integer, default=0, comment='浏览次数')
    like_count = Column(Integer, default=0, comment='点赞次数')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    published_at = Column(DateTime, comment='发布时间')
    
    # 关联关系
    # user = relationship('User', backref='articles')
    
    def as_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'tags': self.tags.split(',') if self.tags else [],
            'category': self.category,
            'status': self.status,
            'is_public': self.is_public,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'user_name': self.user.name if self.user else None
        }
    
    def __repr__(self):
        return f'<Article {self.title}>'
