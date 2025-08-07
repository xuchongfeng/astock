from app import db
from datetime import datetime, date

class DeepSeek(db.Model):
    """DeepSeek对话记录表"""
    __tablename__ = 'deepseek'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 会话ID - 用于标识同一会话的多次对话
    session_id = db.Column(db.String(100), nullable=False, index=True)
    
    # 类型 - 个股/大盘/行业
    type = db.Column(db.String(20), nullable=False, index=True)
    
    # 返回内容 - 大文本
    content = db.Column(db.Text, nullable=False)
    
    # 日期
    date = db.Column(db.Date, nullable=False, index=True)
    
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def as_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'type': self.type,
            'content': self.content,
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<DeepSeek {self.session_id}:{self.type}>' 