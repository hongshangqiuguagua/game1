@echo off
chcp 65001 > nul
echo 正在启动钓鱼邮件识别教学游戏后端服务...
echo.

REM 设置日志目录
if not exist "logs" mkdir logs
set LOG_FILE=logs\backend_start.log
echo [%date% %time%] 开始启动后端 > %LOG_FILE%

REM 检查Python是否已安装
echo [INFO] 检查Python环境...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python未安装或未添加到PATH中
    echo [ERROR] 请安装Python 3.8或更高版本
    echo [ERROR] 下载地址: https://www.python.org/downloads/
    echo [%date% %time%] 错误: Python未安装或未添加到PATH中 >> %LOG_FILE%
    pause
    exit /b 1
)

REM 切换到后端目录
cd /d "%~dp0backend"
echo [INFO] 当前目录: %CD%
echo [%date% %time%] 当前目录: %CD% >> %LOG_FILE%

REM 检查requirements.txt是否存在
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt文件不存在
    echo [%date% %time%] 错误: requirements.txt文件不存在 >> %LOG_FILE%
    pause
    exit /b 1
)

REM 检查依赖是否已安装，如果未安装则询问是否安装
echo [INFO] 检查Python依赖...
python -c "import fastapi, uvicorn, sqlalchemy" > nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] 部分Python依赖未安装
    set /p INSTALL_DEPS="是否安装所需依赖? (y/n): "
    if /i "%INSTALL_DEPS%"=="y" (
        echo [INFO] 正在安装Python依赖...
        pip install -r requirements.txt
        if %errorlevel% neq 0 (
            echo [ERROR] 安装依赖失败
            echo [%date% %time%] 错误: 安装依赖失败 >> %LOG_FILE%
            pause
            exit /b 1
        )
        echo [SUCCESS] 依赖安装完成
    ) else (
        echo [ERROR] 依赖未安装，无法继续
        pause
        exit /b 1
    )
)

REM 启动FastAPI服务
echo [INFO] 正在启动后端服务...
echo [INFO] 服务将在 http://localhost:8000 上运行
echo [INFO] 按Ctrl+C可以停止服务

python app.py
if %errorlevel% neq 0 (
    echo [ERROR] 后端服务启动失败
    echo [%date% %time%] 错误: 后端服务启动失败 >> %LOG_FILE%
    pause
    exit /b 1
)

cd .. 