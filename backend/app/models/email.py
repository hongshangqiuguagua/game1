"""
邮件模型
"""

from .base import Base, Column, Boolean, Integer, String, Text, ForeignKey, relationship

class Email(Base):
    """
    邮件表模型
    
    存储每个关卡中的邮件信息，包括是否为钓鱼邮件的标记
    """
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id"))
    sender = Column(String(100))  # 发件人
    subject = Column(String(255))  # 邮件主题
    content = Column(Text)  # 邮件内容
    is_phishing = Column(Boolean)  # 是否为钓鱼邮件
    phishing_clue = Column(Text)  # 如果是钓鱼邮件，提供骗术揭秘
    
    # 关联关系
    level = relationship("Level", back_populates="emails") 