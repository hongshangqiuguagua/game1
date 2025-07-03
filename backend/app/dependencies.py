"""
依赖项

包含API路由所需的各种依赖函数
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, cast, Dict, Any
import logging

from . import config
from . import models
from .database import get_db
from .schemas import TokenData

# 配置日志
logger = logging.getLogger(__name__)

# OAuth2密码流，指定令牌URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    创建JWT访问令牌
    
    Args:
        data: 要编码到令牌中的数据
        expires_delta: 令牌过期时间
        
    Returns:
        生成的JWT令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
        logger.debug(f"创建访问令牌: 用户={data.get('sub', 'unknown')}, 过期时间={expire}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"创建访问令牌失败: {e}")
        raise


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    获取当前用户的依赖函数
    
    从JWT令牌中解析用户信息，并从数据库中获取用户
    
    Args:
        token: JWT令牌
        db: 数据库会话
        
    Returns:
        当前用户对象
        
    Raises:
        HTTPException: 如果令牌无效或用户不存在
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            logger.warning(f"JWT令牌缺少subject字段")
            raise credentials_exception
        # 显式类型转换，确保username是字符串类型
        token_data = TokenData(username=cast(str, username))
    except JWTError as e:
        logger.warning(f"JWT令牌验证失败: {e}")
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        logger.warning(f"未找到令牌中指定的用户: {token_data.username}")
        raise credentials_exception
    
    logger.debug(f"认证成功: 用户={user.username}, ID={user.id}")
    return user


def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    """
    获取当前活跃用户的依赖函数
    
    验证用户是否处于活跃状态，目前我们没有实现禁用用户功能，但保留此依赖以备将来扩展
    
    Args:
        current_user: 当前用户对象
        
    Returns:
        当前活跃用户对象
    """
    # 保留函数以备将来添加用户禁用功能
    return current_user


def get_current_admin(current_user: models.User = Depends(get_current_user)):
    """
    获取当前管理员用户的依赖函数
    
    检查当前用户是否为管理员
    
    Args:
        current_user: 当前用户对象
        
    Returns:
        当前管理员用户对象
        
    Raises:
        HTTPException: 如果当前用户不是管理员
    """
    # 使用布尔值进行检查，避免直接使用数据库字段
    is_admin = bool(current_user.is_admin)
    logger.debug(f"检查管理员权限: 用户={current_user.username}, 是管理员={is_admin}")
    
    if not is_admin:
        logger.warning(f"非管理员用户尝试访问管理员资源: {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理员权限"
        )
    
    logger.info(f"管理员访问: {current_user.username}")
    return current_user 