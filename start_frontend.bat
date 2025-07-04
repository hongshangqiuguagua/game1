@echo off
REM 钓鱼邮件识别教学游戏 - 前端启动脚本
chcp 65001 > nul
echo.
echo [钓鱼邮件识别教学游戏] 正在启动前端服务...
echo.

REM 设置日志目录和文件
if not exist "logs" mkdir logs
set LOG_FILE=logs\frontend_start.log
echo [%date% %time%] 开始启动前端 > %LOG_FILE%

REM 检查Node.js是否已安装
echo [INFO] 检查Node.js环境...
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js未安装或未添加到PATH中
    echo [ERROR] 请安装Node.js 14.0或更高版本
    echo [ERROR] 下载地址: https://nodejs.org/
    echo [%date% %time%] 错误: Node.js未安装或未添加到PATH中 >> %LOG_FILE%
    pause
    exit /b 1
)

REM 检查npm是否已安装
echo [INFO] 检查npm环境...
npm --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm未安装或未添加到PATH中
    echo [ERROR] 请重新安装Node.js，确保包含npm
    echo [%date% %time%] 错误: npm未安装或未添加到PATH中 >> %LOG_FILE%
    pause
    exit /b 1
)

REM 检查并进入前端目录
set ROOT_DIR=%~dp0
if not exist "%ROOT_DIR%frontend" (
    echo [ERROR] 前端目录不存在
    echo [%date% %time%] 错误: 前端目录不存在 >> %LOG_FILE%
    pause
    exit /b 1
)
cd /d "%ROOT_DIR%frontend"
echo [INFO] 当前目录: %CD%
echo [%date% %time%] 切换到目录: %CD% >> %LOG_FILE%

REM 检查package.json是否存在
if not exist "package.json" (
    echo [ERROR] package.json文件不存在
    echo [%date% %time%] 错误: package.json文件不存在 >> %LOG_FILE%
    pause
    exit /b 1
)

REM 检查node_modules目录是否存在，如果不存在则询问是否安装依赖
if not exist "node_modules" (
    echo [WARNING] 前端依赖未安装
    set /p INSTALL_DEPS="是否安装所需依赖? (y/n): "
    if /i "%INSTALL_DEPS%"=="y" (
        echo [INFO] 正在安装前端依赖...
        call npm install
        if %errorlevel% neq 0 (
            echo [ERROR] 安装依赖失败
            echo [%date% %time%] 错误: npm install 失败，错误码: %errorlevel% >> %LOG_FILE%
            pause
            exit /b 1
        )
        echo [SUCCESS] 依赖安装完成
    ) else (
        echo [ERROR] 依赖未安装，无法继续
        pause
        exit /b 1
    )
) else (
    echo [INFO] 前端依赖已安装
)

REM 启动前端服务
echo [INFO] 启动Vue服务...
echo [INFO] 服务将在 http://localhost:8080 上运行
echo [INFO] 按Ctrl+C可以停止服务
echo [%date% %time%] 启动Vue服务 >> %LOG_FILE%

call npm run serve
if %errorlevel% neq 0 (
    echo [ERROR] 前端服务启动失败
    echo [%date% %time%] 错误: npm run serve 失败，错误码: %errorlevel% >> %LOG_FILE%
    pause
    exit /b 1
)

echo [INFO] 前端服务已停止
echo [%date% %time%] 前端服务已停止 >> %LOG_FILE% 