"""
关卡相关CRUD操作
"""

from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from .. import models, schemas

logger = logging.getLogger(__name__)

def get_levels(db: Session, skip: int = 0, limit: int = 100) -> List[models.Level]:
    """
    获取所有关卡
    
    参数:
        db: 数据库会话
        skip: 跳过的记录数
        limit: 限制返回的记录数
    
    返回:
        关卡列表，按order字段排序
    """
    return db.query(models.Level).order_by(models.Level.order).offset(skip).limit(limit).all()


def get_level(db: Session, level_id: int) -> Optional[models.Level]:
    """
    通过ID获取单个关卡
    
    参数:
        db: 数据库会话
        level_id: 关卡ID
    
    返回:
        找到的关卡对象，如果不存在则返回None
    """
    return db.query(models.Level).filter(models.Level.id == level_id).first()


def get_next_level(db: Session, current_level_order: int) -> Optional[models.Level]:
    """
    获取下一个关卡
    
    参数:
        db: 数据库会话
        current_level_order: 当前关卡的order值
    
    返回:
        下一个关卡对象，如果不存在下一关则返回None
    """
    return db.query(models.Level).filter(models.Level.order > current_level_order).order_by(models.Level.order).first()


def create_level(db: Session, level: schemas.LevelCreate) -> models.Level:
    """
    创建新关卡
    
    参数:
        db: 数据库会话
        level: 关卡创建模型
    
    返回:
        创建的关卡对象
    """
    db_level = models.Level(**level.dict())
    db.add(db_level)
    db.commit()
    db.refresh(db_level)
    logger.info(f"创建了新关卡: {level.name} (order: {level.order})")
    return db_level


def update_level(db: Session, level_id: int, level: schemas.LevelCreate) -> Optional[models.Level]:
    """
    更新关卡
    
    参数:
        db: 数据库会话
        level_id: 要更新的关卡ID
        level: 包含新数据的关卡创建模型
    
    返回:
        更新后的关卡对象，如果关卡不存在则返回None
    """
    db_level = get_level(db, level_id)
    if db_level:
        for key, value in level.dict().items():
            setattr(db_level, key, value)
        db.commit()
        db.refresh(db_level)
        logger.info(f"更新了关卡: ID={level_id}, 名称={level.name}")
    else:
        logger.warning(f"尝试更新不存在的关卡: ID={level_id}")
    return db_level


def delete_level(db: Session, level_id: int) -> bool:
    """
    删除关卡
    
    参数:
        db: 数据库会话
        level_id: 要删除的关卡ID
    
    返回:
        操作是否成功
    """
    db_level = get_level(db, level_id)
    if db_level:
        db.delete(db_level)
        db.commit()
        logger.info(f"删除了关卡: ID={level_id}, 名称={db_level.name}")
        return True
    logger.warning(f"尝试删除不存在的关卡: ID={level_id}")
    return False 