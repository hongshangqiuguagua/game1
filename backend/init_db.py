import logging
import os
import sys

# 将 'backend' 目录添加到 Python 路径中，以便可以找到 'app' 模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base, SessionLocal
from app.data.init import init_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """
    重置并初始化数据库：删除所有表，创建新表，然后填充初始数据。
    """
    logger.info("--- 开始设置数据库 ---")
    
    try:
        logger.info("正在删除所有旧表...")
        Base.metadata.drop_all(bind=engine)
        
        logger.info("正在创建所有新表...")
        Base.metadata.create_all(bind=engine)
        logger.info("--- 数据库表已创建 ---")

        db = SessionLocal()
        try:
            logger.info("--- 开始填充数据库 ---")
            init_database(db)
            logger.info("--- 数据库填充完成 ---")
        finally:
            db.close()
            
        logger.info("--- 数据库设置成功 ---")

    except Exception as e:
        logger.error(f"数据库设置过程中发生错误: {e}")
        raise

if __name__ == "__main__":
    setup_database() 