"""
认证路由

包含用户注册、登录和获取用户信息相关的API接口
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from .. import crud, models, schemas, dependencies, config
from ..database import get_db

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/auth",
    tags=["认证"],
    responses={
        400: {"description": "请求参数错误"},
        401: {"description": "认证失败"},
        404: {"description": "资源未找到"}
    },
)


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    注册新用户
    
    检查用户名和邮箱是否已存在，然后创建新用户
    """
    logger.info(f"用户注册请求: {user.username}, {user.email}")
    
    # 检查用户名是否已存在
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        logger.warning(f"注册失败: 用户名已被使用 - {user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被使用"
        )
    
    # 检查邮箱是否已存在
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        logger.warning(f"注册失败: 邮箱已被注册 - {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 创建新用户
    try:
        new_user = crud.create_user(db=db, user=user)
        logger.info(f"用户注册成功: {user.username}")
        return new_user
    except Exception as e:
        logger.error(f"用户注册异常: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册过程中发生错误，请稍后再试"
        )


@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    用户登录
    
    验证用户凭据并返回JWT令牌
    """
    logger.info(f"用户登录请求: {form_data.username}")
    
    # 认证用户
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"登录失败: 用户名或密码错误 - {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = dependencies.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"用户登录成功: {user.username}, 是管理员={user.is_admin}")
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(dependencies.get_current_user)):
    """
    获取当前登录用户信息
    
    需要有效的JWT令牌
    """
    logger.debug(f"用户 {current_user.username} 获取个人信息")
    return current_user


@router.get("/health")
def auth_health():
    """
    认证服务健康检查
    
    用于前端检查认证服务是否正常运行
    """
    logger.debug("认证服务健康检查")
    return {"status": "ok", "service": "auth"} 