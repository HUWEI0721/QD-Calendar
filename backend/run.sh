#!/bin/bash

# QD日历后端启动脚本

echo "启动 QD日历后端服务..."

# 检查虚拟环境
if [ ! -d "env" ]; then
    echo "创建虚拟环境..."
    python3 -m venv env
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source env/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "警告: .env 文件不存在，请复制 .env.example 并配置"
    cp .env.example .env
    echo "已创建 .env 文件，请编辑配置后重新运行"
    exit 1
fi

# 启动应用
echo "启动 Flask 应用..."
python app.py

