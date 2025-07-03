"""
钓鱼邮件识别教学游戏API服务

主入口文件，创建FastAPI应用并配置路由
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from . import config
from .routers import auth_router, game_router, admin_router
from . import __version__

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title=config.APP_NAME,
    description="一款模仿邮箱的网页小游戏，旨在帮助玩家学会如何识别钓鱼邮件，提升网络安全意识。",
    version=__version__,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router)
app.include_router(game_router)
app.include_router(admin_router)


@app.get("/")
def read_root():
    """
    根路径，返回欢迎信息
    """
    logger.info("访问根路径")
    return {
        "name": config.APP_NAME,
        "version": __version__,
        "message": "欢迎使用钓鱼邮件识别教学游戏API"
    }


@app.get("/health")
def health_check():
    """
    健康检查接口
    
    用于前端检查API服务是否正常运行
    """
    logger.debug("健康检查API被调用")
    return {"status": "ok", "version": __version__}


if __name__ == "__main__":
    # 直接运行此文件时启动服务器
    logger.info(f"启动应用服务器 - {config.APP_NAME} v{__version__}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 