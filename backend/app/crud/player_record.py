"""
玩家记录相关CRUD操作
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc, case
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import json

from .. import models, schemas
from .level import get_level

logger = logging.getLogger(__name__)

def create_player_record(db: Session, record: schemas.PlayerRecordCreate) -> models.PlayerRecord:
    """
    创建玩家记录
    
    参数:
        db: 数据库会话
        record: 玩家记录创建模型
    
    返回:
        创建的玩家记录对象
    """
    db_record = models.PlayerRecord(
        **record.dict()
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    logger.info(f"创建了玩家记录: user_id={record.user_id}, level_id={record.level_id}, score={record.correct_count}/{record.total_count}")
    return db_record


def get_player_records(db: Session, user_id: int) -> List[models.PlayerRecord]:
    """
    获取玩家的所有记录
    
    参数:
        db: 数据库会话
        user_id: 用户ID
    
    返回:
        玩家记录列表
    """
    return db.query(models.PlayerRecord).filter(
        models.PlayerRecord.user_id == user_id
    ).all()


def get_player_record_by_level(db: Session, user_id: int, level_id: int) -> Optional[models.PlayerRecord]:
    """
    获取玩家在特定关卡的记录
    
    参数:
        db: 数据库会话
        user_id: 用户ID
        level_id: 关卡ID
    
    返回:
        玩家在指定关卡的记录，不存在则返回None
    """
    return db.query(models.PlayerRecord).filter(
        models.PlayerRecord.user_id == user_id,
        models.PlayerRecord.level_id == level_id
    ).first()


def get_player_summary(db: Session, user_id: int) -> Dict[str, Any]:
    """
    获取玩家的游戏总结
    
    参数:
        db: 数据库会话
        user_id: 用户ID
    
    返回:
        包含总体数据和关卡记录的字典
    """
    records = get_player_records(db, user_id)
    
    total_correct = sum(record.correct_count for record in records)
    total_played = sum(record.total_count for record in records)
    
    level_records = []
    for record in records:
        # 使用整数转换处理level_id
        try:
            level_id = int(str(record.level_id).strip())
            level = get_level(db, level_id)
            level_name = str(level.name) if level else "未知关卡"
        except (ValueError, AttributeError, TypeError):
            level_id = 0
            level_name = "未知关卡"
        
        level_records.append({
            "level_id": record.level_id,
            "level_name": level_name,
            "correct_count": record.correct_count,
            "total_count": record.total_count
        })
    
    return {
        "total_correct": total_correct,
        "total_played": total_played,
        "level_records": level_records
    }


def get_email_statistics(db: Session) -> List[Dict[str, Any]]:
    """
    获取邮件错误率统计
    
    返回每封邮件的判断次数、错误次数和错误率，按错误率降序排序
    """
    # 1. 查询所有玩家记录
    records = db.query(models.PlayerRecord).all()
    if not records:
        return []

    # 2. 在Python中处理判断结果
    email_stats: Dict[int, Dict[str, int]] = {}
    for record in records:
        # judgments字段可能为字符串或字典/列表
        judgments_data = record.judgments
        if isinstance(judgments_data, str):
            try:
                judgments_data = json.loads(judgments_data)
            except json.JSONDecodeError:
                logger.warning(f"无法解析玩家记录 {record.id} 的judgments字段: {record.judgments}")
                continue

        if not isinstance(judgments_data, list):
            continue

        for j in judgments_data:
            email_id = j.get("email_id")
            is_correct = j.get("correct", None)
            
            # 跳过无效数据
            if email_id is None or is_correct is None:
                continue

            # 确保email_id是整数
            try:
                email_id = int(email_id)
            except (ValueError, TypeError):
                logger.warning(f"无效的email_id: {email_id}")
                continue

            if email_id not in email_stats:
                email_stats[email_id] = {"judgement_count": 0, "error_count": 0}
            
            email_stats[email_id]["judgement_count"] += 1
            if not is_correct:
                email_stats[email_id]["error_count"] += 1

    if not email_stats:
        return []

    # 3. 获取所有相关邮件的信息
    email_ids = list(email_stats.keys())
    emails = db.query(models.Email).filter(models.Email.id.in_(email_ids)).all()
    # 创建一个邮件ID到邮件对象的映射字典
    email_map = {int(email.id): email for email in emails}

    # 4. 组合最终结果
    results = []
    for email_id, stats in email_stats.items():
        email = email_map.get(email_id)
        if not email:
            continue

        judgement_count = stats["judgement_count"]
        error_count = stats["error_count"]
        error_rate = (error_count / judgement_count) * 100 if judgement_count > 0 else 0

        results.append({
            "email_id": email_id,
            "subject": email.subject,
            "sender": email.sender,
            "is_phishing": email.is_phishing,
            "judgement_count": judgement_count,
            "error_count": error_count,
            "error_rate": error_rate,
        })

    # 5. 按错误率降序排序
    results.sort(key=lambda x: x["error_rate"], reverse=True)
    
    return results


def get_overall_statistics(db: Session) -> Dict[str, Any]:
    """
    获取总体游戏统计
    """
    total_users = db.query(models.User).count()
    total_records = db.query(models.PlayerRecord).count()
    
    # 计算总判断数和总正确数
    total_judgments = db.query(func.sum(models.PlayerRecord.total_count)).scalar() or 0
    total_correct = db.query(func.sum(models.PlayerRecord.correct_count)).scalar() or 0
    
    # 计算总正确率
    accuracy = (total_correct / total_judgments) * 100 if total_judgments > 0 else 0
    
    return {
        "total_users": total_users,
        "total_play_sessions": total_records,
        "total_judgments": total_judgments,
        "accuracy": accuracy,
    } 