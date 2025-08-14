# 私有PyPI仓库使用指南

## 服务器信息
- 服务器地址: http://192.2.123.34:8081
- 默认用户名: admin
- 默认密码: admin123
- 包存储目录: /opt/private-pypi/packages

## 使用方法

### 1. 从私有仓库安装包
pip install --index-url http://admin:admin123@192.2.123.34:8081/simple/ <package_name>

### 2. 上传包到私有仓库
twine upload --repository-url http://192.2.123.34:8081 --username admin --password admin123 <package_file>

### 3. 配置pip.conf使用私有仓库
在 ~/.pip/pip.conf 文件中添加:
[global]
index-url = http://admin:admin123@192.2.123.34:8081/simple/
trusted-host = 192.2.123.34
