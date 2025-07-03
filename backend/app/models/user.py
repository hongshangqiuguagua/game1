"""
用户模型
"""

from .base import Base, Column, Boolean, Integer, String, TIMESTAMP, relationship, datetime

class User(Base):
    """
    用户表模型
    
    存储用户信息，包括用户名、邮箱、密码等
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    
    # 关联关系
    records = relationship("PlayerRecord", back_populates="user") 