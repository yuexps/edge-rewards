@echo off
chcp 65001
echo 正在检查是否安装了 pip 和 selenium...

:: 检查是否安装了 pip
pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo 未检测到 pip，请确保 Python 和 pip 已正确安装。
    echo 请访问 https://www.python.org/downloads/ 下载并安装 Python。
    pause
    exit /b
) else (
    echo 已检测到 pip，版本信息如下：
    pip --version
)

:: 检查是否安装了 selenium
for /f "tokens=*" %%i in ('pip list ^| findstr /i "selenium"') do (
    set "found=%%i"
)

:: 检查变量是否包含 selenium
if defined found (
    echo 已检测到 selenium，版本信息如下：
    pip show selenium
    echo 开始执行 Python 脚本...
    python main.py
    if %ERRORLEVEL% == 0 (
        echo Python 脚本运行成功！
    ) else (
        echo Python 脚本运行失败，请检查脚本内容。
    )
) else (
    echo 未检测到 selenium，将尝试自动安装...
    :: 自动安装 selenium
    pip install selenium
    if %ERRORLEVEL% == 0 (
        echo Selenium 安装成功！
        echo 开始执行 Python 脚本...
        python main.py
        if %ERRORLEVEL% == 0 (
            echo Python 脚本运行成功！
        ) else (
            echo Python 脚本运行失败，请检查脚本内容。
        )
    ) else (
        echo Selenium 安装失败，请检查网络或权限。
    )
)

pause
