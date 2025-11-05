# QD日历 - 文档索引

欢迎！这是 QD日历项目的文档导航中心。

## 🚀 新手入门

从这里开始你的 QD日历之旅：

### 1. [START_HERE.md](./START_HERE.md) ⭐ 首次必读
- 项目介绍
- 5分钟快速开始
- 核心功能概览
- 下一步指引

### 2. [QUICKSTART.md](./QUICKSTART.md) - 快速启动指南
- 详细启动步骤
- 环境准备
- 配置说明
- 常见问题解答

### 3. [CHECKLIST.md](./CHECKLIST.md) - 启动检查清单
- 逐项检查清单
- 配置验证
- 功能测试
- 问题排查

## 📚 详细文档

深入了解项目的方方面面：

### 核心文档

#### [README.md](./README.md) - 项目主文档
- 功能特性详解
- 完整技术栈
- 安装部署步骤
- API 接口文档
- 使用指南

#### [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) - 项目结构
- 完整项目结构
- 文件组织说明
- 模块功能解析
- 数据流说明
- 技术架构图

#### [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) - 项目总结
- 项目统计数据
- 技术亮点分析
- 代码质量评估
- 开发时间统计
- 扩展性分析

### 部署文档

#### [DEPLOYMENT.md](./DEPLOYMENT.md) - 生产部署指南
- 服务器要求
- 详细部署步骤
- Nginx 配置
- SSL 证书配置
- 性能优化建议
- 监控和日志
- 备份策略

### 参考文档

#### [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - 快速参考
- 常用命令速查
- API 端点列表
- 环境变量说明
- 请求示例
- 调试技巧

#### [CHANGELOG.md](./CHANGELOG.md) - 更新日志
- 版本历史
- 功能变更
- 未来计划

#### [LICENSE](./LICENSE) - 开源许可
- MIT 许可证全文

## 🎯 按需求查找

### 我想快速体验
→ [START_HERE.md](./START_HERE.md) → [QUICKSTART.md](./QUICKSTART.md)

### 我想完整了解
→ [README.md](./README.md) → [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)

### 我想检查配置
→ [CHECKLIST.md](./CHECKLIST.md)

### 我想部署上线
→ [DEPLOYMENT.md](./DEPLOYMENT.md)

### 我想快速查找
→ [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)

### 我想了解细节
→ [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)

## 📁 代码目录

### 后端代码
```
backend/
├── app.py                    # Flask 应用入口
├── config.py                 # 配置管理
├── models.py                 # 数据库模型
├── init_db.py               # 数据库初始化
├── requirements.txt          # Python 依赖
├── resources/
│   ├── auth.py              # 认证接口
│   └── events.py            # 日程接口
└── utils/
    └── oss_helper.py        # OSS 操作助手
```

详细说明：[backend/README.md](./backend/README.md)

### 前端代码
```
frontend/
├── index.html               # HTML 模板
├── package.json             # Node 依赖
├── vite.config.js          # Vite 配置
└── src/
    ├── main.js             # 应用入口
    ├── App.vue             # 根组件
    ├── style.css           # 全局样式
    ├── views/              # 页面组件
    │   ├── Home.vue        # 首页
    │   ├── Login.vue       # 登录页
    │   ├── Register.vue    # 注册页
    │   ├── Calendar.vue    # 日历视图 ⭐
    │   └── Admin.vue       # 管理面板
    ├── stores/             # 状态管理
    │   ├── auth.js         # 认证状态
    │   └── events.js       # 日程状态
    ├── api/                # API 封装
    │   ├── axios.js        # HTTP 客户端
    │   ├── auth.js         # 认证 API
    │   └── events.js       # 日程 API
    └── router/
        └── index.js        # 路由配置
```

详细说明：[frontend/README.md](./frontend/README.md)

## 🎓 学习路径

### 初学者路径
1. 阅读 [START_HERE.md](./START_HERE.md) 了解项目
2. 按照 [QUICKSTART.md](./QUICKSTART.md) 启动项目
3. 使用 [CHECKLIST.md](./CHECKLIST.md) 验证配置
4. 浏览 [README.md](./README.md) 了解功能

### 开发者路径
1. 研究 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) 理解架构
2. 查看源代码，理解实现
3. 参考 [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) 开发
4. 阅读 [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) 学习亮点

### 运维路径
1. 跟随 [QUICKSTART.md](./QUICKSTART.md) 本地测试
2. 使用 [CHECKLIST.md](./CHECKLIST.md) 检查环境
3. 按照 [DEPLOYMENT.md](./DEPLOYMENT.md) 部署
4. 参考 [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) 维护

## 📊 文档统计

| 文档 | 行数 | 用途 |
|------|------|------|
| START_HERE.md | 300+ | 新手入门 |
| README.md | 300+ | 项目主文档 |
| QUICKSTART.md | 250+ | 快速启动 |
| PROJECT_STRUCTURE.md | 500+ | 架构详解 |
| PROJECT_SUMMARY.md | 400+ | 项目总结 |
| DEPLOYMENT.md | 600+ | 部署指南 |
| CHECKLIST.md | 300+ | 检查清单 |
| QUICK_REFERENCE.md | 200+ | 快速参考 |
| **总计** | **2,850+** | **完整文档** |

## 🔍 快速搜索

### 关键词索引

**启动相关**: [QUICKSTART.md](./QUICKSTART.md), [CHECKLIST.md](./CHECKLIST.md)  
**配置相关**: [QUICKSTART.md](./QUICKSTART.md), [DEPLOYMENT.md](./DEPLOYMENT.md)  
**API相关**: [README.md](./README.md), [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)  
**架构相关**: [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)  
**部署相关**: [DEPLOYMENT.md](./DEPLOYMENT.md)  
**功能相关**: [README.md](./README.md), [START_HERE.md](./START_HERE.md)  
**问题排查**: [QUICKSTART.md](./QUICKSTART.md), [CHECKLIST.md](./CHECKLIST.md)

## 💡 使用建议

### 第一次使用？
1. 从 [START_HERE.md](./START_HERE.md) 开始 ⭐
2. 跟随 5分钟快速启动步骤
3. 体验核心功能
4. 查看其他文档深入了解

### 要深入学习？
1. 完整阅读 [README.md](./README.md)
2. 研究 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)
3. 查看源代码
4. 尝试修改和扩展

### 要部署上线？
1. 先在本地测试成功
2. 准备生产环境
3. 按照 [DEPLOYMENT.md](./DEPLOYMENT.md) 部署
4. 配置监控和备份

### 日常使用？
1. 收藏 [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
2. 遇到问题先查文档
3. 查看日志调试
4. 必要时提交 Issue

## 🎯 核心文件推荐

### ⭐⭐⭐ 必读
- [START_HERE.md](./START_HERE.md) - 首次必读
- [QUICKSTART.md](./QUICKSTART.md) - 快速启动
- [README.md](./README.md) - 完整功能

### ⭐⭐ 推荐
- [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) - 理解架构
- [CHECKLIST.md](./CHECKLIST.md) - 配置检查
- [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - 日常参考

### ⭐ 按需
- [DEPLOYMENT.md](./DEPLOYMENT.md) - 部署时阅读
- [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) - 深入了解
- [CHANGELOG.md](./CHANGELOG.md) - 了解版本

## 📞 获取帮助

### 文档中找不到答案？
1. 搜索相关关键词
2. 查看源代码注释
3. 检查日志输出
4. 提交 GitHub Issue

### 发现文档错误？
欢迎提交 PR 改进文档！

### 想要新功能？
在 GitHub Issues 提交功能建议。

## 🎉 开始使用

**现在就开始吧！** 

点击 [START_HERE.md](./START_HERE.md) 开启你的 QD日历之旅！

---

**QD日历 v1.0.0** | [GitHub](https://github.com/your-repo) | [Issues](https://github.com/your-repo/issues)

最后更新：2025-10-30

