"""
数据库初始化

包含用于初始化数据库并填充示例数据的函数
"""

import logging
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from .sample_data import get_sample_levels, get_admin_user

logger = logging.getLogger(__name__)

def create_level_with_emails(db: Session, level_info: dict):
    """根据提供的信息创建关卡及其下属邮件"""
    level = crud.create_level(db, schemas.LevelCreate(
        name=level_info["name"],
        description=level_info["description"],
        order=level_info["order"],
        trick_summary=level_info.get("trick_summary", "本关暂无总结。")
    ))
    logger.info(f"关卡 '{level.name}' 创建成功")
    
    for email_info in level_info.get("emails", []):
        crud.create_email(db, schemas.EmailCreate(
            level_id=level.id,
            sender=email_info["sender"],
            subject=email_info["subject"],
            content=email_info["content"],
            is_phishing=email_info["is_phishing"],
            phishing_clue=email_info.get("phishing_clue")
        ))
        logger.info(f"邮件 '{email_info['subject']}' 创建成功")


def init_database(db: Session):
    """初始化数据库，创建管理员用户和示例关卡"""
    # 检查并创建管理员用户
    admin_user = db.query(models.User).filter(models.User.is_admin == True).first()
    if not admin_user:
        logger.info("未找到管理员账户，正在创建...")
        admin_data = get_admin_user()
        crud.create_user(db, schemas.UserCreate(
            username=admin_data["username"],
            email=admin_data["email"],
            password=admin_data["password"]
        ), is_admin=True)
        logger.info("管理员用户创建成功")

    # 检查是否已有数据，如果没有才初始化
    if db.query(models.Level).first():
        logger.info("数据库已有关卡数据，跳过初始化。")
        return

    # 创建示例关卡和邮件
    levels_data = get_sample_levels()
    for level_data in levels_data:
        create_level_with_emails(db, level_data)

    logger.info("示例数据初始化完成") 