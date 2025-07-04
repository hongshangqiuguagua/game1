@echo off
chcp 65001 > nul
echo 正在初始化钓鱼邮件识别教学游戏数据库...
echo.

REM 设置日志目录
if not exist "logs" mkdir logs
set LOG_FILE=logs\init_database.log
echo [%date% %time%] 开始初始化数据库 > %LOG_FILE%

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
python -c "import sqlalchemy" > nul 2>&1
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

REM 初始化数据库
echo [INFO] 正在初始化数据库...
python init_db.py
if %errorlevel% neq 0 (
    echo [ERROR] 数据库初始化失败，错误代码: %errorlevel%
    echo [%date% %time%] 错误: 数据库初始化失败，错误代码: %errorlevel% >> %LOG_FILE%
    echo 按任意键退出...
    pause > nul
    exit /b 1
)
echo [SUCCESS] 数据库初始化完成
echo [%date% %time%] 数据库初始化完成 >> %LOG_FILE%
echo.
echo [INFO] 数据库已成功初始化，现在可以启动应用了
echo.

pause 