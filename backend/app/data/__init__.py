"""
数据初始化模块

包含用于初始化和填充数据库的函数和数据
"""

from .sample_data import get_sample_levels, get_admin_user
from .init import init_database

__all__ = ['init_database', 'get_sample_levels', 'get_admin_user'] 