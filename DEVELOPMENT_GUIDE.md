# Xinference 二次开发指南

本文档提供了如何进行 Xinference 二次开发，同时保持与官方版本同步更新的详细指南。

## 目录
- [1. 环境准备](#1-环境准备)
- [2. 仓库配置](#2-仓库配置)
- [3. 开发流程](#3-开发流程)
- [4. 代码同步](#4-代码同步)
- [5. 最佳实践](#5-最佳实践)
- [6. 常见问题](#6-常见问题)

## 1. 环境准备

确保您的开发环境已经安装：
- Git
- Python 3.8+
- pip 或 conda 包管理器

## 2. 仓库配置

### 2.1 配置远程仓库
您的仓库应该配置两个远程源：
```bash
# 检查当前远程仓库配置
git remote -v

# 如果还没有配置 upstream，添加官方仓库作为 upstream
git remote add upstream https://github.com/xorbitsai/inference.git
```

### 2.2 分支管理
创建并切换到开发分支：
```bash
# 创建新的开发分支
git checkout -b feature/custom-development

# 查看当前分支状态
git status
```

## 3. 开发流程

### 3.1 日常开发
1. 确保在开发分支上进行修改
2. 遵循项目代码规范
3. 保持合理的提交粒度

### 3.2 提交规范
使用语义化的提交信息：
```bash
# 示例
git commit -m "feat: 添加新的模型支持"
git commit -m "fix: 修复模型加载问题"
git commit -m "docs: 更新API文档"
```

提交类型说明：
- feat: 新功能
- fix: 修复问题
- docs: 文档更新
- style: 代码格式修改
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

## 4. 代码同步

### 4.1 同步官方更新
```bash
# 1. 切换到 main 分支
git checkout main

# 2. 获取官方最新代码
git fetch upstream

# 3. 合并官方更新
git merge upstream/main

# 4. 推送到自己的远程仓库
git push origin main
```

### 4.2 更新开发分支
```bash
# 1. 切换到开发分支
git checkout feature/custom-development

# 2. 合并主分支更新
git merge main

# 3. 解决冲突（如果有）并提交
git add .
git commit -m "merge: 合并主分支更新"

# 4. 推送到远程
git push origin feature/custom-development
```

## 5. 最佳实践

### 5.1 代码组织
- 在 `xinference/extensions/` 目录下创建新的模块
- 避免直接修改核心代码
- 使用依赖注入和插件模式进行功能扩展

### 5.2 测试规范
- 为新功能编写单元测试
- 确保测试覆盖率
- 运行完整测试套件确保无破坏性更改

### 5.3 文档维护
- 及时更新API文档
- 添加新功能的使用说明
- 维护更新日志（CHANGELOG）

## 6. 常见问题

### 6.1 合并冲突处理
当遇到合并冲突时：
1. 仔细审查冲突内容
2. 优先保持官方的核心功能实现
3. 调整自定义代码以兼容官方更新
4. 在解决冲突后进行完整测试

### 6.2 版本发布
- 在重要节点使用版本标签
```bash
git tag -a v1.0.0 -m "发布1.0.0版本"
git push origin v1.0.0
```

### 6.3 注意事项
- 定期同步官方更新
- 保持良好的代码注释
- 遵循项目的代码风格指南
- 保持模块化和可测试性

## 帮助和支持

如果您在开发过程中遇到问题，可以：
1. 查看官方文档
2. 在官方仓库提交 Issue
3. 参与社区讨论

---

本指南将持续更新，欢迎提供改进建议。 