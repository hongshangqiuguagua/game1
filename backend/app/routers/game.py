"""
游戏路由

包含游戏功能相关的API接口，用户需要登录才能访问
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
import logging

from .. import crud, models, schemas, dependencies
from ..database import get_db

# 配置日志
logger = logging.getLogger(__name__)

# 创建游戏路由，所有路由都需要用户登录
router = APIRouter(
    prefix="/api/game",
    tags=["游戏"],
    dependencies=[Depends(dependencies.get_current_user)],  # 所有路由都需要用户登录
    responses={
        401: {"description": "未登录或令牌无效"},
        404: {"description": "资源未找到"}
    },
)

@router.get("/levels", response_model=List[schemas.LevelResponse])
def get_levels_for_game(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    """
    获取所有关卡列表
    
    返回系统中所有关卡的列表，用于在游戏主界面展示
    """
    logger.debug(f"用户 {current_user.username} 获取关卡列表")
    return crud.get_levels(db)

@router.get("/levels/{level_id}/emails", response_model=List[schemas.EmailResponse])
def get_level_emails_for_game(
    level_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    """
    获取指定关卡的所有邮件
    
    返回指定关卡的所有邮件，但不包含是否为钓鱼邮件等敏感信息
    """
    logger.debug(f"用户 {current_user.username} 获取关卡 {level_id} 的邮件")
    
    # 检查关卡是否存在
    level = crud.get_level(db, level_id=level_id)
    if not level:
        logger.warning(f"用户 {current_user.username} 尝试访问不存在的关卡 {level_id}")
        raise HTTPException(status_code=404, detail="关卡不存在")
        
    return crud.get_emails_by_level(db, level_id=level_id)

@router.post("/levels/{level_id}/submit", response_model=schemas.LevelResultResponse)
def submit_level_result(
    level_id: int, 
    submission: schemas.LevelSubmit, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    """
    提交关卡结果
    
    提交玩家在当前关卡的判断结果，系统将计算分数并保存记录
    """
    logger.info(f"用户 {current_user.username} 提交关卡 {level_id} 的结果")
    
    # 检查关卡是否存在
    level = crud.get_level(db, level_id=level_id)
    if not level:
        logger.warning(f"用户 {current_user.username} 尝试提交不存在的关卡 {level_id} 的结果")
        raise HTTPException(status_code=404, detail="关卡不存在")

    # 获取关卡所有邮件
    emails = crud.get_emails_by_level(db, level_id=level_id)
    if not emails:
        logger.warning(f"关卡 {level_id} 没有邮件")
        raise HTTPException(status_code=400, detail="关卡没有任何邮件")
        
    emails_dict = {email.id: email for email in emails}

    # 验证提交的判断数量
    if len(submission.judgments) != len(emails):
        logger.warning(f"用户 {current_user.username} 提交的邮件数量与关卡不符")
        raise HTTPException(
            status_code=400, 
            detail=f"提交的邮件数量与关卡不符，期望 {len(emails)} 封，实际提交 {len(submission.judgments)} 封"
        )

    correct_count = 0
    results_with_details = []
    judgments_with_correct = []
    
    # 计算得分并记录结果
    for judgment in submission.judgments:
        email_id = judgment.email_id
        if email_id not in emails_dict:
            logger.warning(f"用户 {current_user.username} 提交了无效的邮件ID {email_id}")
            raise HTTPException(status_code=400, detail=f"邮件ID {email_id} 无效")

        email = emails_dict[email_id]
        is_correct = (judgment.is_phishing_guess == email.is_phishing)
        if is_correct:
            correct_count += 1
        
        # 添加正确性标记到判断结果中
        judgment_dict = judgment.dict()
        judgment_dict["correct"] = is_correct
        judgments_with_correct.append(judgment_dict)
        
        phishing_clue = email.phishing_clue if email.phishing_clue is not None else None
        subject = email.subject if email.subject is not None else None
        
        results_with_details.append(schemas.ResultDetail(
            email_id=email.id,
            is_phishing=bool(email.is_phishing),
            correct=is_correct,
            phishing_clue=str(phishing_clue) if phishing_clue else None,
            subject=str(subject) if subject else None
        ))

    # 创建玩家记录
    try:
        record_in = schemas.PlayerRecordCreate(
            user_id=int(current_user.id),
            level_id=level_id,
            correct_count=correct_count,
            total_count=len(emails),
            judgments=judgments_with_correct  # 使用带有correct字段的判断结果
        )
        crud.create_player_record(db=db, record=record_in)
        logger.info(f"用户 {current_user.username} 完成关卡 {level_id}，得分: {correct_count}/{len(emails)}")
    except Exception as e:
        logger.error(f"保存玩家记录时出错: {e}")
        # 即使保存记录失败，仍然返回结果给玩家
        # 这是一个可恢复的错误，不应该阻止玩家看到他们的结果
    
    # 获取下一关卡
    next_level = crud.get_next_level(db, current_level_order=int(level.order))
    next_level_id = next_level.id if next_level else None
    
    # 返回关卡结果
    trick_summary = level.trick_summary if level.trick_summary is not None else None
    
    return schemas.LevelResultResponse(
        correct_count=correct_count,
        total_count=len(emails),
        results=results_with_details,
        next_level_id=next_level_id,
        level_name=str(level.name),
        trick_summary=str(trick_summary) if trick_summary else None
    )

@router.get("/summary", response_model=schemas.GameSummaryResponse)
def get_game_summary(
    current_user: models.User = Depends(dependencies.get_current_user), 
    db: Session = Depends(get_db)
):
    """
    获取游戏总结
    
    返回当前玩家的所有游戏记录和成绩总结
    """
    logger.debug(f"用户 {current_user.username} 获取游戏总结")
    
    summary = crud.get_player_summary(db, user_id=int(current_user.id))
    # 不抛出404异常，因为即使用户没有任何游戏记录，也应该返回一个空的总结
    return summary