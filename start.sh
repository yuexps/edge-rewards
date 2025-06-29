#!/bin/bash

echo "正在检查是否安装了 Python 和 pip..."

# 检查是否安装了 Python 3
if ! command -v python3 &> /dev/null; then
    echo "未检测到 Python 3，请先安装 Python 3。"
    echo "您可以使用以下命令安装 Python 3："
    echo "sudo apt-get update && sudo apt-get install python3"  # Debian/Ubuntu
    echo "sudo yum install python3"                            # CentOS/RHEL
    echo "sudo dnf install python3"                            # Fedora
    read -p "按任意键继续..."
    exit 1
else
    echo "已检测到 Python 3，版本信息如下："
    python3 --version
fi

# 检查是否安装了 pip
if ! command -v pip3 &> /dev/null; then
    echo "未检测到 pip，请先安装 pip。"
    echo "您可以使用以下命令安装 pip："
    echo "sudo apt-get update && sudo apt-get install python3-pip"  # Debian/Ubuntu
    echo "sudo yum install python3-pip"                           # CentOS/RHEL
    echo "sudo dnf install python3-pip"                           # Fedora
    read -p "按任意键继续..."
    exit 1
else
    echo "已检测到 pip，版本信息如下："
    pip3 --version
fi

# 检查是否安装了 selenium
if ! pip3 list | grep -i selenium &> /dev/null; then
    echo "未检测到 selenium，将尝试自动安装..."
    # 自动安装 selenium
    if pip3 install selenium; then
        echo "Selenium 安装成功！"
        echo "开始执行 Python 脚本..."
        if python3 main.py; then
            echo "Python 脚本运行成功！"
        else
            echo "Python 脚本运行失败，请检查脚本内容。"
        fi
    else
        echo "Selenium 安装失败，请检查网络或权限。"
    fi
else
    echo "已检测到 selenium，版本信息如下："
    pip3 show selenium
    echo "开始执行 Python 脚本..."
    if python3 main.py; then
        echo "Python 脚本运行成功！"
    else
        echo "Python 脚本运行失败，请检查脚本内容。"
    fi
fi
