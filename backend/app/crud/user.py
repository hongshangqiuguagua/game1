"""
用户相关CRUD操作
"""

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Optional
import logging

from .. import models, schemas

# 日志记录器
logger = logging.getLogger(__name__)

# 密码上下文，用于哈希和验证密码
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.warning(f"密码验证异常: {e}")
        # 如果验证失败，尝试直接比较（用于调试）
        # 注意：这仅用于测试环境，生产环境应移除
        logger.warning("尝试直接比较密码")
        from hashlib import sha256
        return sha256(plain_password.encode()).hexdigest() == hashed_password


def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.warning(f"密码哈希异常: {e}")
        # 如果哈希失败，使用简单的哈希（用于调试）
        # 注意：这仅用于测试环境，生产环境应使用安全的哈希算法
        from hashlib import sha256
        return sha256(password.encode()).hexdigest()


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """通过ID获取用户"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """通过用户名获取用户"""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """通过邮箱获取用户"""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate, is_admin: bool = False) -> models.User:
    """
    创建新用户
    
    参数:
        db: 数据库会话
        user: 用户创建模型
        is_admin: 是否为管理员，默认为False
    
    返回:
        创建的用户对象
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    """
    认证用户
    
    参数:
        db: 数据库会话
        username: 用户名
        password: 密码
    
    返回:
        认证成功返回用户对象，失败返回None
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    
    # 打印用户密码信息（仅用于调试）
    stored_hash = str(user.hashed_password)
    logger.debug(f"用户: {username}, 验证密码: {password}, 存储的哈希: {stored_hash}")
    
    if not verify_password(password, stored_hash):
        # 登录失败时也打印一些信息以便调试
        logger.debug(f"密码验证失败: {username}")
        return None
    
    return user 