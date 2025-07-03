@echo off
REM 钓鱼邮件识别教学游戏 - 前端启动脚本
chcp 65001 > nul
echo.
echo [GAME] Starting Frontend Development Server...
echo.

REM 设置根目录和日志文件
set ROOT_DIR=%~dp0
set LOG_FILE=%ROOT_DIR%frontend_start_log.txt
echo [%date% %time%] 开始启动前端 > %LOG_FILE%

REM 检查并进入前端目录
if not exist "%ROOT_DIR%frontend" (
    echo [ERROR] 前端目录不存在
    echo [%date% %time%] 错误: 前端目录不存在 >> %LOG_FILE%
    goto :error
)
cd /d "%ROOT_DIR%frontend"
echo [INFO] 当前目录: %CD%
echo [%date% %time%] 切换到目录: %CD% >> %LOG_FILE%

REM 安装依赖
echo [FRONTEND] Installing dependencies...
call npm install
if %errorlevel% neq 0 (
    echo [FRONTEND] ERROR: Failed to install dependencies.
    echo [%date% %time%] 错误: npm install 失败，错误码: %errorlevel% >> %LOG_FILE%
    goto :error
)
echo [%date% %time%] npm install 成功 >> %LOG_FILE%

REM 启动前端服务
echo [INFO] 启动Vue服务...
echo [INFO] 按Ctrl+C可以停止服务
echo [%date% %time%] 启动Vue服务 >> %LOG_FILE%

REM 直接在当前窗口运行前端服务
call npm run serve
if %errorlevel% neq 0 (
    echo [FRONTEND] ERROR: Failed to start frontend server.
    echo [%date% %time%] 错误: npm run serve 失败，错误码: %errorlevel% >> %LOG_FILE%
    goto :error
)

REM 如果执行到这里，说明用户手动停止了服务
echo [INFO] 前端服务已停止
echo [%date% %time%] 前端服务已停止 >> %LOG_FILE%
goto :eof

:error
echo [ERROR] 启动过程中发生错误，请查看日志文件 %LOG_FILE%
echo [INFO] 如果问题持续存在，请联系技术支持
echo [%date% %time%] 启动失败 >> %LOG_FILE%
pause
exit /b 1 