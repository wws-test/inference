# Xinference 构建工具说明

## 🎯 概述

本项目提供了多种构建和上传工具，支持将Xinference项目打包并上传到私有PyPI仓库。

## 🛠️ 构建工具

### 1. build.bat (Windows批处理文件)
**最简单的使用方式，推荐Windows用户使用**

```bash
# 双击运行
build.bat

# 或命令行执行
.\build.bat
```

**功能菜单：**
- 快速构建并上传 (跳过UI，推荐)
- 快速构建不上传 (跳过UI)
- 清理后构建上传 (跳过UI)
- 完整构建并上传 (包含UI，需要Node.js)
- 完整构建不上传 (包含UI，需要Node.js)
- 查看帮助
- 退出

### 2. quick_build.py (快速构建脚本)
**跳过UI构建，适合Windows环境**

```bash
# 快速构建上传
python quick_build.py

# 清理后构建上传
python quick_build.py --clean

# 只构建不上传
python quick_build.py --skip-upload
```

**特点：**
- ✅ 跳过UI构建，避免Node.js依赖
- ✅ 自动检查前置条件
- ✅ 彩色输出，用户体验好
- ✅ 自动安装缺失的依赖
- ✅ 适合日常开发和测试

### 3. build_and_upload.py (完整构建脚本)
**包含UI构建，功能完整**

```bash
# 完整构建上传
python build_and_upload.py

# 清理后构建上传
python build_and_upload.py --clean

# 跳过UI构建
python build_and_upload.py --skip-ui

# 只构建不上传
python build_and_upload.py --skip-upload

# 构建上传后测试安装
python build_and_upload.py --test

# 强制继续（即使某些步骤失败）
python build_and_upload.py --force
```

**特点：**
- ✅ 包含Web UI构建
- ✅ 功能完整，适合正式发布
- ✅ 支持测试安装
- ✅ 需要Node.js环境

## 📋 前置条件

### 基础要求
- Python 3.7+
- twine (会自动安装)

### 完整构建要求
- Python 3.7+
- Node.js
- npm
- twine (会自动安装)

## 🎨 功能特性

### 智能检查
- 自动检查Python版本
- 自动检查Node.js和npm (完整构建)
- 自动安装缺失的依赖

### 彩色输出
- 🎉 成功信息 (绿色)
- ⚠️ 警告信息 (黄色)
- ✗ 错误信息 (红色)
- 📦 步骤信息 (紫色)

### 自动清理
- 清理构建文件
- 清理缓存文件
- 清理临时文件

### 版本管理
- 自动获取Git版本
- 支持versioneer
- 版本兼容性检查

## 🚀 使用流程

### 快速开始 (推荐)
1. 双击运行 `build.bat`
2. 选择 "1. 快速构建并上传"
3. 等待构建完成

### 命令行使用
```bash
# 快速构建
python quick_build.py

# 完整构建
python build_and_upload.py
```

## 📦 构建结果

### 包文件
- 位置: `dist/` 目录
- 格式: `xinference-<version>.tar.gz`
- 大小: 约20-25MB

### 版本信息
- 自动从Git获取版本
- 支持开发版本标记
- 版本兼容性验证

## 🔗 私有仓库

### 仓库信息
- 地址: `http://192.2.123.34:8081`
- 用户名: `admin`
- 密码: `admin123`

### 安装命令
```bash
pip3 install --extra-index-url http://admin:admin123@192.2.123.34:8081/simple/ --trusted-host 192.2.123.34 xinference==<version>
```

## ⚠️ 注意事项

### Windows环境
- 推荐使用 `quick_build.py` 或 `build.bat`
- 避免Node.js依赖问题
- 支持中文路径

### Linux/macOS环境
- 可以使用完整构建脚本
- 需要安装Node.js
- 支持UI构建

### 版本兼容性
- 支持Python 3.7+
- 自动选择兼容的包版本
- 私有仓库支持fallback功能

## 🐛 故障排除

### 常见问题

1. **Node.js未安装**
   - 使用 `quick_build.py` 跳过UI构建
   - 或安装Node.js后使用完整构建

2. **twine未安装**
   - 脚本会自动安装
   - 手动安装: `pip install twine`

3. **权限问题**
   - 确保有写入权限
   - 使用管理员权限运行

4. **网络问题**
   - 检查私有仓库连接
   - 确认防火墙设置

### 日志查看
- 构建过程会显示详细日志
- 错误信息会高亮显示
- 支持中断和重试

## 📚 相关文档

- [私有PyPI仓库使用指南](pypiserver.md)
- [Xinference项目文档](README.md)
- [构建脚本源码](quick_build.py)

## 🤝 贡献

欢迎提交Issue和Pull Request来改进构建工具！

---

**🎉 享受便捷的构建体验！**
