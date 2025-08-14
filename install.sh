#!/bin/bash

# 安装依赖
pip install -e ".[all]"

# 创建模型目录
MODEL_PATH="/opt/xinference/models"
sudo mkdir -p "$MODEL_PATH"/{llama2-7b,chatglm-6b,qwen-7b}
sudo chown -R $USER:$USER "$MODEL_PATH"

# 安装nginx（如果未安装）
if ! command -v nginx &> /dev/null; then
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y nginx
    elif [ -f /etc/redhat-release ]; then
        # CentOS/RHEL
        sudo yum install -y epel-release
        sudo yum install -y nginx
    fi
fi


# 重启nginx使配置生效
sudo systemctl restart nginx

echo "安装完成！"
echo "请将模型文件放置在 $MODEL_PATH 对应的子目录中" 