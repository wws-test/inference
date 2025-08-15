# 私有PyPI仓库使用指南

## 概述
私有PyPI仓库地址：`http://192.2.123.34:8081`
- 用户名：`admin`
- 密码：`admin123`
- 端口：`8081`

## 功能特性
✅ **多版本兼容**：支持Python 3.7+的多个版本包
✅ **智能Fallback**：如果私有仓库没有某个包，会自动从公共PyPI下载
✅ **认证访问**：支持用户名密码认证
✅ **包缓存**：已缓存常用基础包，提高下载速度

## 安装包

### 方法1：使用extra-index-url（推荐）
```bash
pip3 install --extra-index-url http://admin:admin123@192.2.123.34:8081/simple/ --trusted-host 192.2.123.34 <package_name>
```

### 方法2：使用index-url
```bash
pip3 install --index-url http://admin:admin123@192.2.123.34:8081/simple/ --trusted-host 192.2.123.34 <package_name>
```

### 方法3：配置pip.conf（永久配置）
```bash
# 创建或编辑 ~/.pip/pip.conf
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
extra-index-url = http://admin:admin123@192.2.123.34:8081/simple/
trusted-host = 192.2.123.34
EOF
```

## 构建和上传包

### 方法1：使用快速构建脚本（推荐）
```bash
# 快速构建上传（跳过UI，适合Windows）
python quick_build.py

# 清理后构建上传
python quick_build.py --clean

# 只构建不上传
python quick_build.py --skip-upload
```

### 方法2：使用完整构建脚本（包含UI）
```bash
# 完整构建上传（包含UI构建）
python build_and_upload.py

# 清理后构建上传
python build_and_upload.py --clean

# 跳过UI构建
python build_and_upload.py --skip-ui

# 只构建不上传
python build_and_upload.py --skip-upload

# 构建上传后测试安装
python build_and_upload.py --test
```

### 方法3：使用批处理文件 (Windows)
```bash
# 双击运行或命令行执行
build.bat

# 选择相应的构建选项
```

### 方法4：手动构建上传
```bash
# 构建包（跳过UI）
$env:NO_WEB_UI=1; python setup.py sdist

# 上传到私有仓库
twine upload --repository-url http://192.2.123.34:8081 --username admin --password admin123 <package_file>
```

### 示例：上传xinference包
```bash
# 使用快速构建脚本
python quick_build.py

# 或手动构建上传
$env:NO_WEB_UI=1; python setup.py sdist
twine upload --repository-url http://192.2.123.34:8081 --username admin --password admin123 dist/xinference-1.8.2.tar.gz
```

## 管理私有仓库

### 查看服务状态
```bash
systemctl status private-pypi
```

### 启动服务
```bash
systemctl start private-pypi
```

### 停止服务
```bash
systemctl stop private-pypi
```

### 重启服务
```bash
systemctl restart private-pypi
```

### 查看服务日志
```bash
journalctl -u private-pypi -f
```

## 包管理

### 查看私有仓库中的包
```bash
curl -u admin:admin123 http://192.2.123.34:8081/simple/
```

### 查看特定包的版本
```bash
curl -u admin:admin123 http://192.2.123.34:8081/simple/<package_name>/
```

### 下载包到私有仓库
```bash
# 使用脚本下载基础包
python3 /opt/private-pypi/download_py37_packages.py

# 手动下载单个包
python3 -m pip download --no-deps --dest /opt/private-pypi/packages <package_name>
```

## 实际使用示例

### 安装xinference（私有包）
```bash
pip3 install --extra-index-url http://admin:admin123@192.2.123.34:8081/simple/ --trusted-host 192.2.123.34 xinference==1.8.2
```


## 版本兼容性说明

### 当前支持的Python版本
- Python 3.7+ (主要支持)
- Python 3.8+ (完全支持)

### 包版本策略
1. **私有包**：优先使用私有仓库中的版本
2. **基础包**：私有仓库中有多个版本，pip会自动选择兼容的版本
3. **缺失包**：如果私有仓库没有，会自动从公共PyPI下载

### 已缓存的基础包
- setuptools (65.5.1) - 兼容Python 3.7+
- wheel (0.40.0) - 兼容Python 3.7+
- pip (23.3.2) - 兼容Python 3.7+
- requests, numpy, pandas, flask, django等常用包

## 故障排除

### 连接问题
```bash
# 检查服务是否运行
systemctl status private-pypi

# 检查端口是否开放
netstat -tlnp | grep 8081

# 测试连接
curl -u admin:admin123 http://192.2.123.34:8081/simple/
```

### 认证问题
```bash
# 检查认证文件
ls -la /opt/private-pypi/auth/.htpasswd

# 重新创建用户
python3 /opt/private-pypi/create_user.py admin admin123
```

### 包下载问题
```bash
# 检查包目录
ls -la /opt/private-pypi/packages/

# 重新下载基础包
python3 /opt/private-pypi/download_py37_packages.py
```

## 目录结构
```
/opt/private-pypi/
├── packages/           # 包存储目录
├── auth/              # 认证配置
│   └── .htpasswd      # 用户密码文件
├── start_server.sh    # 启动脚本
├── manage.sh          # 管理脚本
├── download_py37_packages.py  # 下载脚本
├── create_user.py     # 用户管理脚本
└── README.md          # 说明文档
```

## 构建脚本说明

### quick_build.py - 快速构建脚本
- **用途**: 快速构建Python包并上传到私有仓库
- **特点**: 跳过UI构建，适合Windows环境
- **依赖**: Python 3.7+, twine
- **推荐**: 日常开发和测试使用

### build_and_upload.py - 完整构建脚本
- **用途**: 完整构建包含UI的Python包并上传
- **特点**: 包含Web UI构建，功能完整
- **依赖**: Python 3.7+, Node.js, npm, twine
- **推荐**: 正式发布使用

## 注意事项
1. 使用`--extra-index-url`而不是`--index-url`可以同时搜索私有仓库和公共PyPI
2. 私有仓库已启用fallback功能，会自动从公共PyPI获取缺失的包
3. 所有包都经过版本兼容性测试，支持Python 3.7+
4. 建议在生产环境中使用HTTPS而不是HTTP
5. Windows环境下推荐使用`quick_build.py`，避免Node.js依赖问题
6. 构建脚本会自动检查前置条件并安装缺失的依赖
