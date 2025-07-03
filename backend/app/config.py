"""
应用配置

包含应用运行所需的各种配置参数
"""

import os
from datetime import timedelta

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../sql_app.db")

# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-keep-it-secret")  # 生产环境中应使用强随机密钥
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))  # 默认24小时

# 跨域配置
CORS_ORIGINS = [
    "http://localhost:8080",  # Vue CLI默认端口
    "http://localhost:3000",  # React默认端口
    "http://localhost:5173",  # Vite默认端口
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5173",
]

# 应用配置
APP_NAME = "钓鱼邮件识别教学游戏"

# 安全配置
HASHING_ALGORITHM = "bcrypt"

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
