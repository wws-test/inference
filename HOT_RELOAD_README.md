# Xinference 热更新功能

## 概述

为 `xinference-local` 命令添加了新的 `--hot-reload` 选项，提供更完善的开发体验，包括前端和后端的热更新功能。

## 功能特性

### 新增的 `--hot-reload` 选项

- **自动依赖安装**: 自动检查并安装前端依赖（npm install）
- **React 开发服务器**: 自动启动 React 开发服务器（npm start）
- **增强的日志输出**: 提供更详细的启动信息和状态提示
- **开发环境检查**: 检查 Node.js 和 npm 是否可用

### 与现有 `--dev` 选项的区别

| 功能 | `--dev` | `--hot-reload` |
|------|---------|----------------|
| 启动 React 开发服务器 | ✓ | ✓ |
| 自动安装依赖 | ✗ | ✓ |
| 环境检查 | ✗ | ✓ |
| 详细日志 | 基础 | 增强 |
| 启动等待时间 | 无 | 2秒等待 |

## 使用方法

### 1. 启动热更新模式

```bash
xinference-local --hot-reload
```

这将：
- 自动检查 Node.js 和 npm 环境
- 自动安装前端依赖（如果未安装）
- 启动 React 开发服务器
- 启动后端 API 服务器
- 提供详细的启动信息

### 2. 启动基础开发模式

```bash
xinference-local --dev
```

### 3. 自定义端口和主机

```bash
xinference-local --hot-reload --host 0.0.0.0 --port 9998
```

## 开发流程

### 前端开发

1. 启动热更新模式：
   ```bash
   xinference-local --hot-reload
   ```

2. 访问前端开发服务器：
   - 前端: http://localhost:3000
   - 后端 API: http://localhost:9997

3. 修改前端代码（位于 `xinference/ui/web/ui/src/`）
4. 浏览器会自动刷新显示最新更改

### 后端开发

1. 修改后端代码（位于 `xinference/` 目录）
2. 重启 xinference-local 服务
3. 前端会自动连接到新的后端服务

## 技术实现

### 代码修改位置

1. **命令行接口**: `xinference/deploy/cmdline.py`
   - 添加 `--hot-reload` 选项
   - 修改 `local()` 函数

2. **本地集群**: `xinference/deploy/local.py`
   - 添加 `hot_reload_mode` 参数支持

3. **RESTful API**: `xinference/api/restful_api.py`
   - 增强前端开发服务器启动逻辑
   - 添加环境检查和依赖安装

### 前端技术栈

- **框架**: React 18
- **构建工具**: Create React App
- **UI 库**: Material-UI (MUI)
- **开发服务器**: React Scripts (npm start)

## 环境要求

### 必需软件

- Python 3.8+
- Node.js 16+
- npm 8+

### 检查环境

```bash
# 检查 Node.js
node --version

# 检查 npm
npm --version

# 检查 Python
python --version
```

## 故障排除

### 常见问题

1. **npm 未找到**
   ```
   错误: npm is not available. Please install Node.js and npm.
   ```
   解决: 安装 Node.js 和 npm

2. **前端依赖安装失败**
   ```
   错误: Failed to start dev server
   ```
   解决: 手动运行 `cd xinference/ui/web/ui && npm install`

3. **端口被占用**
   ```
   错误: Failed to create socket with port 9997
   ```
   解决: 使用 `--port` 选项指定其他端口

### 调试模式

```bash
xinference-local --hot-reload --log-level debug
```

## 测试

运行测试脚本验证功能：

```bash
python test_hot_reload.py
```

## 贡献

如需改进热更新功能，请：

1. 修改相关代码文件
2. 更新测试脚本
3. 更新本文档
4. 提交 Pull Request

## 许可证

遵循项目的 Apache License 2.0 许可证。
