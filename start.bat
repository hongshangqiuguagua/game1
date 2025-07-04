@echo off
chcp 65001 > nul
echo.
echo [钓鱼邮件识别教学游戏] 启动完整应用 (后端 + 前端)...
echo.

REM 设置项目根目录
cd /d "%~dp0"

REM 创建logs目录(如果不存在)
if not exist "logs" mkdir logs

echo [INFO] 提示: 如果这是首次运行，请先运行 init_database.bat 初始化数据库
echo [INFO] 提示: 请确保已安装Python 3.8+和Node.js
echo.

echo [INFO] 在新窗口中启动后端服务器...
start "Backend Server" cmd /c "start_backend.bat"

echo [INFO] 等待后端初始化 (5 秒)...
timeout /t 5 /nobreak

echo [INFO] 在新窗口中启动前端服务器...
start "Frontend Server" cmd /c "start_frontend.bat"

echo.
echo [SUCCESS] 两个服务器正在不同窗口中启动
echo   - 后端将在: http://localhost:8000
echo   - 前端将在: http://localhost:8080
echo   - 前端开发环境启动可能需要几分钟，请耐心等待
echo.
echo [INFO] 您可以关闭此窗口，服务器将继续在其各自窗口中运行
echo. 