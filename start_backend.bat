@echo off
chcp 65001 > nul
echo 正在启动钓鱼邮件识别教学游戏后端服务...
echo.

cd /d "%~dp0backend"

REM 初始化数据库（如果需要）
echo [INFO] 正在初始化数据库...
python init_db.py
if %errorlevel% neq 0 (
    echo [ERROR] 数据库初始化失败
    pause
    exit /b 1
)
echo [SUCCESS] 数据库初始化完成

REM 启动FastAPI服务
echo [INFO] 正在启动后端服务...
python app.py
if %errorlevel% neq 0 (
    echo [ERROR] 后端服务启动失败
    pause
    exit /b 1
)

cd ..