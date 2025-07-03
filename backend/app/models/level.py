"""
关卡模型
"""

from .base import Base, Column, Integer, String, Text, relationship

class Level(Base):
    """
    关卡表模型
    
    存储游戏关卡信息
    """
    __tablename__ = "levels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    order = Column(Integer)
    trick_summary = Column(Text, nullable=True)  # 本关骗术总结
    
    # 关联关系
    emails = relationship("Email", back_populates="level", cascade="all, delete-orphan")
    records = relationship("PlayerRecord", back_populates="level", cascade="all, delete-orphan") 