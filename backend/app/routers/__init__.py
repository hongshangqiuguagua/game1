"""
路由模块

包含所有API路由定义
"""

from .auth import router as auth_router
from .game import router as game_router
from .admin import router as admin_router

__all__ = ["auth_router", "game_router", "admin_router"] 