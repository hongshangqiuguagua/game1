"""
管理后台路由

包含管理员专用API接口，需要管理员权限才能访问
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
import logging

from .. import crud, models, schemas, dependencies
from ..database import get_db

# 配置日志
logger = logging.getLogger(__name__)

# 创建管理员路由，所有路由都需要管理员权限
router = APIRouter(
    prefix="/api/admin",
    tags=["管理后台"],
    dependencies=[Depends(dependencies.get_current_admin)],  # 所有路由都需要管理员权限
    responses={
        404: {"description": "未找到资源"},
        403: {"description": "权限不足，需要管理员权限"}
    }
)


# 关卡管理
@router.get("/levels", response_model=List[schemas.LevelResponse])
def get_levels(db: Session = Depends(get_db)):
    """
    获取所有关卡
    
    返回系统中所有关卡的列表，包括关卡ID、名称、描述等信息
    """
    logger.info("管理员请求获取所有关卡")
    return crud.get_levels(db)


@router.post("/levels", response_model=schemas.LevelResponse, status_code=status.HTTP_201_CREATED)
def create_level(
    level: schemas.LevelCreate, 
    db: Session = Depends(get_db), 
    admin: models.User = Depends(dependencies.get_current_admin)
):
    """
    创建新关卡
    
    管理员可以创建新关卡，需要提供关卡名称、描述、顺序等信息
    """
    logger.info(f"管理员 {admin.username} 创建新关卡: {level.name}")
    return crud.create_level(db=db, level=level)


@router.put("/levels/{level_id}", response_model=schemas.LevelResponse)
def update_level(
    level_id: int, 
    level: schemas.LevelCreate, 
    db: Session = Depends(get_db),
    admin: models.User = Depends(dependencies.get_current_admin)
):
    """
    更新关卡信息
    
    管理员可以更新已有关卡的信息，需要提供关卡ID和新的数据
    """
    logger.info(f"管理员 {admin.username} 更新关卡 ID={level_id}: {level.name}")
    db_level = crud.update_level(db=db, level_id=level_id, level=level)
    if db_level is None:
        logger.warning(f"尝试更新不存在的关卡: ID={level_id}")
        raise HTTPException(status_code=404, detail="关卡不存在")
    return db_level


@router.delete("/levels/{level_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_level(
    level_id: int, 
    db: Session = Depends(get_db),
    admin: models.User = Depends(dependencies.get_current_admin)
):
    """
    删除关卡
    
    管理员可以删除关卡，会同时删除该关卡下的所有邮件
    """
    logger.info(f"管理员 {admin.username} 删除关卡 ID={level_id}")
    success = crud.delete_level(db=db, level_id=level_id)
    if not success:
        logger.warning(f"尝试删除不存在的关卡: ID={level_id}")
        raise HTTPException(status_code=404, detail="关卡不存在")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# 邮件管理
@router.get("/levels/{level_id}/emails", response_model=List[schemas.EmailAdminResponse])
def get_emails_for_level(
    level_id: int, 
    db: Session = Depends(get_db),
    admin: models.User = Depends(dependencies.get_current_admin)
):
    """
    获取关卡下的所有邮件（管理员视图）
    
    返回指定关卡下的所有邮件，包括是否为钓鱼邮件等敏感信息
    """
    logger.info(f"管理员 {admin.username} 获取关卡 ID={level_id} 的邮件列表")
    emails = crud.get_emails_by_level(db, level_id=level_id)
    if not emails and not crud.get_level(db, level_id):
        logger.warning(f"关卡不存在: ID={level_id}")
        raise HTTPException(status_code=404, detail="关卡不存在")
    return emails


@router.post("/emails", response_model=schemas.EmailAdminResponse, status_code=status.HTTP_201_CREATED)
def create_email(
    email: schemas.EmailCreate, 
    db: Session = Depends(get_db),
    admin: models.User = Depends(dependencies.get_current_admin)
):
    """
    为指定关卡创建新邮件
    
    管理员可以为指定关卡创建新邮件，需要提供邮件主题、内容、是否为钓鱼邮件等信息
    """
    logger.info(f"管理员 {admin.username} 创建新邮件: {email.subject} (关卡ID={email.level_id})")
    
    # 验证关卡是否存在
    level = crud.get_level(db, level_id=email.level_id)
    if not level:
        logger.warning(f"尝试为不存在的关卡创建邮件: 关卡ID={email.level_id}")
        raise HTTPException(status_code=404, detail="关卡不存在")
    
    return crud.create_email(db=db, email=email)


@router.put("/emails/{email_id}", response_model=schemas.EmailAdminResponse)
def update_email(
    email_id: int, 
    email: schemas.EmailUpdate, 
    db: Session = Depends(get_db),
    admin: models.User = Depends(dependencies.get_current_admin)
):
    """
    更新邮件信息
    
    管理员可以更新邮件信息，需要提供邮件ID和新的数据
    """
    logger.info(f"管理员 {admin.username} 更新邮件 ID={email_id}")
    
    # 如果更新了level_id，验证目标关卡是否存在
    if email.level_id is not None:
        level = crud.get_level(db, level_id=email.level_id)
        if not level:
            logger.warning(f"尝试将邮件移动到不存在的关卡: 关卡ID={email.level_id}")
            raise HTTPException(status_code=404, detail="目标关卡不存在")
    
    db_email = crud.update_email(db=db, email_id=email_id, email=email)
    if db_email is None:
        logger.warning(f"尝试更新不存在的邮件: ID={email_id}")
        raise HTTPException(status_code=404, detail="邮件不存在")
    return db_email


@router.delete("/emails/{email_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_email(
    email_id: int, 
    db: Session = Depends(get_db),
    admin: models.User = Depends(dependencies.get_current_admin)
):
    """
    删除邮件
    
    管理员可以删除邮件
    """
    logger.info(f"管理员删除邮件 ID={email_id}")
    success = crud.delete_email(db=db, email_id=email_id)
    if not success:
        logger.warning(f"尝试删除不存在的邮件: ID={email_id}")
        raise HTTPException(status_code=404, detail="邮件不存在")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# 统计相关
@router.get("/statistics/emails", response_model=List[schemas.EmailStatisticsResponse])
def get_email_error_statistics(
    db: Session = Depends(get_db),
    admin: models.User = Depends(dependencies.get_current_admin)
):
    """
    获取邮件错误率统计
    
    返回每封邮件的判断次数、错误次数和错误率，按错误率降序排序
    管理员可以据此了解玩家最常误判的邮件类型
    """
    logger.info(f"管理员 {admin.username} 请求邮件错误率统计")
    stats = crud.get_email_statistics(db)
    if not stats:
        return []
    return stats


@router.get("/statistics/overview", response_model=schemas.OverallStatistics)
def get_overall_statistics(
    db: Session = Depends(get_db), 
    admin: models.User = Depends(dependencies.get_current_admin)
):
    """
    获取总体游戏统计
    
    管理员用于查看整体游戏数据，包括用户数、游玩次数、判断正确率等
    """
    logger.info(f"管理员 {admin.username} 请求总体统计数据")
    statistics = crud.get_overall_statistics(db)
    return statistics 