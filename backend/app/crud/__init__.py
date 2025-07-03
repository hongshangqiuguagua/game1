"""
数据库CRUD操作
"""

from .user import (
    verify_password, get_password_hash, get_user, get_user_by_username,
    get_user_by_email, create_user, authenticate_user
)

from .level import (
    get_levels, get_level, get_next_level, create_level, update_level, delete_level
)

from .email import (
    get_emails_by_level, get_email, create_email, update_email, delete_email
)

from .player_record import (
    create_player_record, get_player_records, get_player_record_by_level,
    get_player_summary, get_email_statistics, get_overall_statistics
)

__all__ = [
    # 用户相关
    'verify_password', 'get_password_hash', 'get_user', 'get_user_by_username',
    'get_user_by_email', 'create_user', 'authenticate_user',
    
    # 关卡相关
    'get_levels', 'get_level', 'get_next_level', 'create_level', 'update_level', 'delete_level',
    
    # 邮件相关
    'get_emails_by_level', 'get_email', 'create_email', 'update_email', 'delete_email',
    
    # 玩家记录相关
    'create_player_record', 'get_player_records', 'get_player_record_by_level',
    'get_player_summary', 'get_email_statistics', 'get_overall_statistics'
] 