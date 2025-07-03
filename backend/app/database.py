from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_URL

# 创建SQLAlchemy引擎，对于SQLite增加连接参数
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # 仅SQLite需要
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类，用于创建模型类
Base = declarative_base()

# 依赖函数，用于获取数据库会话
def get_db():
    """
    获取数据库会话的依赖函数
    
    每个API请求会创建一个新的会话，请求结束后关闭会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 