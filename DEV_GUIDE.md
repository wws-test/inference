# Xinference 本地开发指南

## 🎯 概述

本指南介绍如何在本地启动Xinference的开发环境，用于二次开发和调试。

## 🚀 快速启动

### 方法1：使用批处理脚本（推荐）
```bash
# 双击运行
dev_start.bat
```

### 方法2：手动启动

#### 1. 启动后端服务
```bash
# 在项目根目录下
python -m xinference.deploy.worker --host 0.0.0.0 --port 9997
```

#### 2. 启动前端开发服务器
```bash
# 进入前端目录
cd xinference/ui/web/ui

# 启动开发服务器
npm start
```

## 📱 访问地址

- **前端开发服务器**: http://localhost:3000
- **后端API服务**: http://localhost:9997

## 🔧 开发环境配置

### 前端开发
- **框架**: React 18
- **UI库**: Material-UI (MUI)
- **状态管理**: React Hooks
- **路由**: React Router
- **国际化**: i18next
- **热重载**: 自动启用

### 后端开发
- **框架**: Python
- **端口**: 9997
- **API**: RESTful API
- **WebSocket**: 实时通信

## 💡 开发提示

### 前端开发
1. **热重载**: 修改前端代码会自动刷新浏览器
2. **开发工具**: 使用浏览器开发者工具调试
3. **API调试**: 前端会代理API请求到后端
4. **样式修改**: 支持CSS/SCSS热重载

### 后端开发
1. **代码修改**: 需要重启后端服务
2. **日志查看**: 在终端查看后端日志
3. **API测试**: 使用Postman或curl测试API
4. **调试**: 使用Python调试器

## 🛠️ 二次开发重点

根据你的二开想法，重点关注以下文件：

### 前端文件
```
xinference/ui/web/ui/src/
├── scenes/
│   └── register_model/
│       ├── index.js          # 模型注册页面
│       └── data/
│           └── languages.js   # 语言配置
├── components/
│   └── translateButton.js    # 语言切换按钮
└── i18n.js                   # 国际化配置
```

### 后端文件
```
xinference/
├── deploy/
│   └── worker.py             # 后端服务主文件
└── model/
    └── ...                   # 模型相关代码
```

## 🎨 修改示例

### 1. 修改默认语言（已完成）
- 文件: `xinference/ui/web/ui/src/i18n.js`
- 修改: 设置默认语言为中文

### 2. 添加局域网模型下载选项
- 前端: 在模型注册页面添加"lan_repository"选项
- 后端: 在worker.py中添加对应的下载逻辑

### 3. 修改UI界面
- 文件: `xinference/ui/web/ui/src/scenes/`
- 功能: 修改各个页面的UI组件

## 🔍 调试技巧

### 前端调试
```javascript
// 在代码中添加调试信息
console.log('调试信息:', data);

// 使用React DevTools
// 在浏览器中安装React Developer Tools扩展
```

### 后端调试
```python
# 在代码中添加调试信息
import logging
logging.info('调试信息: %s', data)

# 使用Python调试器
import pdb; pdb.set_trace()
```

## 📝 开发流程

1. **启动开发环境**
   ```bash
   dev_start.bat
   ```

2. **修改代码**
   - 前端: 直接修改，自动热重载
   - 后端: 修改后重启服务

3. **测试功能**
   - 访问 http://localhost:3000
   - 测试修改的功能

4. **构建测试**
   ```bash
   # 测试构建
   python quick_build.py --skip-upload
   ```

## 🐛 常见问题

### 端口被占用
```bash
# 查看端口占用
netstat -tlnp | grep 9997
netstat -tlnp | grep 3000

# 使用其他端口
python -m xinference.deploy.worker --port 9998
```

### 前端依赖问题
```bash
# 重新安装依赖
cd xinference/ui/web/ui
rm -rf node_modules package-lock.json
npm install
```

### 后端依赖问题
```bash
# 重新安装
pip install -e .
```

## 📚 相关文档

- [Xinference官方文档](https://github.com/xorbitsai/inference)
- [React开发文档](https://react.dev/)
- [Material-UI文档](https://mui.com/)
- [i18next文档](https://www.i18next.com/)

---

**🎉 开始你的二次开发之旅！**
