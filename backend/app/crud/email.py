"""
邮件相关CRUD操作
"""

from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from .. import models, schemas

logger = logging.getLogger(__name__)

def get_emails_by_level(db: Session, level_id: int) -> List[models.Email]:
    """
    获取某个关卡下的所有邮件
    
    参数:
        db: 数据库会话
        level_id: 关卡ID
    
    返回:
        邮件列表
    """
    return db.query(models.Email).filter(models.Email.level_id == level_id).all()


def get_email(db: Session, email_id: int) -> Optional[models.Email]:
    """
    获取单个邮件
    
    参数:
        db: 数据库会话
        email_id: 邮件ID
    
    返回:
        邮件对象，不存在则返回None
    """
    return db.query(models.Email).filter(models.Email.id == email_id).first()


def create_email(db: Session, email: schemas.EmailCreate) -> models.Email:
    """
    创建新邮件
    
    参数:
        db: 数据库会话
        email: 邮件创建模型
    
    返回:
        创建的邮件对象
    """
    db_email = models.Email(**email.dict())
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    logger.info(f"创建了新邮件: {email.subject} (level_id: {email.level_id})")
    return db_email


def update_email(db: Session, email_id: int, email: schemas.EmailUpdate) -> Optional[models.Email]:
    """
    更新邮件
    
    参数:
        db: 数据库会话
        email_id: 要更新的邮件ID
        email: 包含新数据的邮件更新模型
    
    返回:
        更新后的邮件对象，不存在则返回None
    """
    db_email = get_email(db, email_id)
    if db_email:
        update_data = email.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_email, key, value)
        db.commit()
        db.refresh(db_email)
        logger.info(f"更新了邮件: ID={email_id}")
    else:
        logger.warning(f"尝试更新不存在的邮件: ID={email_id}")
    return db_email


def delete_email(db: Session, email_id: int) -> bool:
    """
    删除邮件
    
    参数:
        db: 数据库会话
        email_id: 要删除的邮件ID
    
    返回:
        操作是否成功
    """
    db_email = get_email(db, email_id)
    if db_email:
        db.delete(db_email)
        db.commit()
        logger.info(f"删除了邮件: ID={email_id}, 标题={db_email.subject}")
        return True
    logger.warning(f"尝试删除不存在的邮件: ID={email_id}")
    return False 