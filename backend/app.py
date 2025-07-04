"""
钓鱼邮件识别教学游戏 - 应用启动脚本

这是应用的入口点，用于启动FastAPI服务器
"""

import uvicorn
import logging
import os
import sys

# 确保app模块可以被正确导入
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app import __version__, config

# 确保logs目录存在
logs_dir = os.path.join(os.path.dirname(current_dir), "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# 配置日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(logs_dir, "app.log"), encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def main():
    """
    主入口函数，启动服务器
    """
    logger.info(f"启动 {config.APP_NAME} v{__version__}")
    logger.info(f"数据库URL: {config.DATABASE_URL}")
    
    # 从环境变量中获取配置，并提供安全的默认值
    host = os.getenv("HOST", "0.0.0.0")
    
    port = 8000
    port_str = os.getenv("PORT")
    if port_str:
        try:
            port = int(port_str)
        except (ValueError, TypeError):
            logger.warning(f"无效的端口号: '{port_str}'，使用默认值: {port}")

    reload = True
    reload_str = os.getenv("RELOAD")
    if reload_str and reload_str.lower() in ["false", "0", "no"]:
        reload = False
        
    # 输出启动信息
    logger.info(f"服务器配置: host={host}, port={port}, reload={reload}")
    logger.info("启动服务器...")
    
    # 启动服务器
    try:
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level=config.LOG_LEVEL.lower()
        )
    except Exception as e:
        logger.error(f"启动服务器时发生错误: {e}")
        input("按Enter键继续...")
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"程序运行失败: {e}")
        input("按Enter键退出...")
        sys.exit(1) 