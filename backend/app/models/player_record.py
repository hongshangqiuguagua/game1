"""
玩家记录模型
"""

from .base import Base, Column, Integer, TIMESTAMP, JSON, ForeignKey, relationship, datetime

class PlayerRecord(Base):
    """
    玩家记录表模型
    
    存储玩家完成关卡的记录和判断结果
    """
    __tablename__ = "player_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    level_id = Column(Integer, ForeignKey("levels.id"))
    correct_count = Column(Integer)  # 正确判断的邮件数量
    total_count = Column(Integer)  # 总邮件数量
    completed_at = Column(TIMESTAMP, default=datetime.utcnow)  # 完成时间
    judgments = Column(JSON)  # 玩家判断结果，JSON格式
    
    # 关联关系
    user = relationship("User", back_populates="records")
    level = relationship("Level", back_populates="records") 