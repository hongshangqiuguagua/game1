from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime


# 用户相关模型
class UserBase(BaseModel):
    """用户基础模型"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """用户创建模型"""
    password: str


class UserLogin(BaseModel):
    """用户登录模型"""
    username: str
    password: str


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    is_admin: bool = False

    class Config:
        orm_mode = True


# 令牌相关模型
class Token(BaseModel):
    """JWT令牌模型"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """令牌数据模型"""
    username: Optional[str] = None


# 关卡相关模型
class LevelBase(BaseModel):
    """关卡基础模型"""
    name: str
    description: str
    order: int
    trick_summary: Optional[str] = None


class LevelCreate(LevelBase):
    """关卡创建模型"""
    pass


class LevelResponse(LevelBase):
    """关卡响应模型"""
    id: int

    class Config:
        orm_mode = True


# 邮件相关模型
class EmailBase(BaseModel):
    """邮件基础模型"""
    sender: str
    subject: str
    content: str


class EmailCreate(EmailBase):
    """邮件创建模型"""
    level_id: int
    is_phishing: bool
    phishing_clue: Optional[str] = None


class EmailUpdate(BaseModel):
    """邮件更新模型，与EmailCreate相同"""
    level_id: Optional[int] = None
    sender: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    is_phishing: Optional[bool] = None
    phishing_clue: Optional[str] = None


class EmailResponse(EmailBase):
    """邮件响应模型（不包含是否为钓鱼邮件的信息）"""
    id: int

    class Config:
        orm_mode = True


class EmailAdminResponse(EmailResponse):
    """管理员邮件响应模型（包含是否为钓鱼邮件的信息）"""
    is_phishing: bool
    phishing_clue: Optional[str] = None
    level_id: int

    class Config:
        orm_mode = True


# 玩家判断相关模型
class EmailJudgment(BaseModel):
    """邮件判断模型"""
    email_id: int
    is_phishing_guess: bool


class LevelSubmit(BaseModel):
    """关卡提交模型"""
    judgments: List[EmailJudgment]


class ResultDetail(BaseModel):
    """判断结果模型"""
    email_id: int
    is_phishing: bool
    correct: bool
    phishing_clue: Optional[str] = None
    subject: Optional[str] = None


class LevelResultResponse(BaseModel):
    """关卡结果模型"""
    correct_count: int
    total_count: int
    results: List[ResultDetail]
    next_level_id: Optional[int]
    level_name: str
    trick_summary: Optional[str] = None


# 游戏总结相关模型
class LevelRecordSummary(BaseModel):
    """关卡记录模型"""
    level_id: int
    level_name: str
    correct_count: int
    total_count: int


class GameSummaryResponse(BaseModel):
    """游戏总结模型"""
    total_correct: int
    total_played: int
    level_records: List[LevelRecordSummary]


# 统计相关模型
class EmailStatisticsResponse(BaseModel):
    """邮件统计响应模型"""
    email_id: int
    subject: str
    sender: str
    is_phishing: bool
    judgement_count: int
    error_count: int
    error_rate: float

    class Config:
        orm_mode = True


# 总体统计相关模型
class LevelStat(BaseModel):
    """关卡统计模型"""
    level_id: int
    level_name: str
    play_count: int
    total_judgments: int
    correct_judgments: int
    accuracy_rate: float


class RecentPlay(BaseModel):
    """最近游玩记录模型"""
    user_id: int
    username: str
    level_id: int
    level_name: str
    correct_count: int
    total_count: int
    completed_at: datetime


class OverallStatistics(BaseModel):
    """总体统计模型"""
    total_users: int
    total_plays: int
    total_judgments: int
    correct_judgments: int
    accuracy_rate: float
    level_stats: List[LevelStat]
    recent_plays: List[RecentPlay]


class PlayerRecordBase(BaseModel):
    user_id: int
    level_id: int
    correct_count: int
    total_count: int
    judgments: List[Dict[str, Any]]


class PlayerRecordCreate(PlayerRecordBase):
    pass


class PlayerRecordResponse(BaseModel):
    id: int
    user_id: int
    level_id: int
    correct_count: int
    total_count: int
    judgments: List[Dict[str, Any]]
    completed_at: datetime

    class Config:
        orm_mode = True


class EmailResult(BaseModel):
    """邮件处理结果"""
    email_id: int
    is_phishing: bool
    correct: bool
    phishing_clue: Optional[str] = None


class GameSubmitResult(BaseModel):
    correct_count: int
    total_count: int
    results: List[EmailResult]
    next_level_id: Optional[int]
    trick_summary: Optional[str] = None