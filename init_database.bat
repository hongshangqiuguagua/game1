@echo off
chcp 65001 > nul
echo [DATABASE] 钓鱼邮件识别教学游戏 - 数据库初始化
echo.

cd /d "%~dp0backend"

echo [INFO] 正在初始化数据库...
python init_db.py
if %errorlevel% neq 0 (
    echo [ERROR] 数据库初始化失败
    pause
    exit /b 1
)
echo [SUCCESS] 数据库初始化完成
echo.
echo [INFO] 数据库已重置并填充初始数据
echo.
pause