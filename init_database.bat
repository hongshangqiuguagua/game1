@echo off
chcp 65001 > nul
echo 正在初始化钓鱼邮件识别教学游戏数据库...
echo.

REM 设置项目根目录
cd /d "%~dp0backend"
echo [INFO] 当前目录: %CD%

REM 初始化数据库
echo [INFO] 正在初始化数据库...
python init_db.py
if %errorlevel% neq 0 (
    echo [ERROR] 数据库初始化失败，错误代码: %errorlevel%
    echo 按任意键退出...
    pause > nul
    exit /b 1
)
echo [SUCCESS] 数据库初始化完成
echo.
echo [INFO] 数据库已成功初始化，现在可以启动应用了
echo.

pause 