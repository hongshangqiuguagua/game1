@echo off
chcp 65001 > nul
echo 正在启动钓鱼邮件识别教学游戏后端服务...
echo.

cd /d "%~dp0backend"
echo [INFO] 当前目录: %CD%

REM 启动FastAPI服务
echo [INFO] 正在启动后端服务...
echo [INFO] 服务将在 http://localhost:8000 上运行
echo [INFO] 按Ctrl+C可以停止服务

python app.py
if %errorlevel% neq 0 (
    echo [ERROR] 后端服务启动失败
    pause
    exit /b 1
)

cd .. 