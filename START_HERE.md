# 🎉 欢迎使用 QD日历！

## 👋 你好！

感谢选择 QD日历 - 一个功能完整、设计精美的共享日程管理系统。

## ⚡ 5分钟快速开始

### 第1步：检查环境
确保已安装：
- ✅ Python 3.8+
- ✅ Node.js 16+
- ✅ MySQL 5.7+

### 第2步：创建数据库
```sql
CREATE DATABASE qd_calendar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 第3步：启动后端
```bash
cd backend
python3 -m venv env
source env/bin/activate      # Mac/Linux
pip install -r requirements.txt
cp .env.example .env         # 编辑配置数据库
python init_db.py            # 初始化数据库
python app.py                # 启动后端
```

### 第4步：启动前端
打开新终端：
```bash
cd frontend
npm install
npm run dev
```

### 第5步：开始使用
打开浏览器访问：http://localhost:3000

🎊 **恭喜！现在可以开始使用了！**

## 🔑 默认账号

- **管理员**: admin / admin123
- **测试用户**: testuser / password123
- **游客**: 无需登录，直接点击"游客浏览"

## 📚 文档导航

根据你的需求选择：

### 🚀 我想快速开始
→ 阅读 [QUICKSTART.md](./QUICKSTART.md)  
详细的分步启动指南，5分钟启动应用

### 📖 我想了解完整功能
→ 阅读 [README.md](./README.md)  
完整的项目文档，包含所有功能说明

### 🏗️ 我想了解架构
→ 阅读 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)  
详细的项目结构和技术架构说明

### 🚢 我想部署到生产环境
→ 阅读 [DEPLOYMENT.md](./DEPLOYMENT.md)  
完整的生产环境部署指南

### ✅ 我想检查配置
→ 阅读 [CHECKLIST.md](./CHECKLIST.md)  
逐步检查清单，确保配置正确

### 📊 我想了解项目详情
→ 阅读 [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)  
项目统计、技术亮点、代码质量分析

### ⚡ 我想快速查找命令
→ 阅读 [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)  
常用命令、API端点、快速参考

## 🎯 核心功能

### ✨ 日程管理
- 创建、编辑、删除日程（管理员专属）
- 设置优先级和状态
- 添加背景图片
- 时间段管理

### 📅 日历视图
- 美观的月历展示
- 每日日程概览
- 悬浮窗口详情
- 筛选和搜索

### 🔐 权限控制
- **管理员**: 完全控制权限
- **普通用户**: 只能查看
- **游客**: 免登录浏览

### 🎨 用户体验
- 响应式设计
- 流畅动画
- 直观操作
- 友好提示

## 🛠️ 技术栈

### 前端
- **Vue 3** - Composition API
- **Pinia** - 状态管理
- **Element Plus** - UI组件
- **V-Calendar** - 日历组件

### 后端
- **Flask** - Web框架
- **SQLAlchemy** - ORM
- **JWT** - 认证
- **MySQL** - 数据库

## 📁 项目结构一览

```
QD-Calendar/
├── backend/              # Flask 后端
│   ├── app.py           # 应用入口
│   ├── models.py        # 数据模型
│   ├── resources/       # API 资源
│   └── utils/           # 工具函数
│
├── frontend/            # Vue3 前端
│   └── src/
│       ├── views/       # 页面组件
│       │   ├── Home.vue        # 首页
│       │   ├── Login.vue       # 登录
│       │   ├── Register.vue    # 注册
│       │   ├── Calendar.vue    # 日历视图 ⭐
│       │   └── Admin.vue       # 管理面板
│       ├── stores/      # 状态管理
│       ├── api/         # API 封装
│       └── router/      # 路由配置
│
└── docs/                # 完整文档
    ├── README.md
    ├── QUICKSTART.md
    ├── PROJECT_STRUCTURE.md
    ├── DEPLOYMENT.md
    ├── CHECKLIST.md
    ├── PROJECT_SUMMARY.md
    └── QUICK_REFERENCE.md
```

## 🎬 使用场景

### 个人使用
- 日程规划
- 时间管理
- 学习Vue3/Flask

### 团队协作
- 共享日程
- 团队日历
- 活动管理

### 企业应用
- 会议安排
- 项目里程碑
- 资源调度

## 💡 特色亮点

### 1️⃣ 开箱即用
- 5分钟启动
- 零配置（基础功能）
- 示例数据

### 2️⃣ 代码优雅
- 模块化设计
- 清晰注释
- 最佳实践

### 3️⃣ 文档完整
- 7份完整文档
- API 文档
- 部署指南

### 4️⃣ 可扩展
- 易于添加功能
- 灵活配置
- 良好架构

## 🎓 学习价值

这个项目适合学习：
- ✅ Vue 3 Composition API
- ✅ Flask RESTful API
- ✅ JWT 认证机制
- ✅ 权限控制设计
- ✅ 前后端分离
- ✅ 状态管理
- ✅ 响应式设计
- ✅ 云服务集成

## 📊 项目数据

- **代码量**: 约 3,697 行
- **文档量**: 约 1,650+ 行
- **文件数**: 38 个
- **开发时间**: 约 9 小时
- **版本**: 1.0.0
- **许可**: MIT

## 🚀 下一步

### 现在就开始！

1. **快速体验**
   ```bash
   # 按照上面的5步骤启动
   # 5分钟后即可使用！
   ```

2. **深入了解**
   - 阅读相关文档
   - 查看代码实现
   - 尝试添加功能

3. **部署上线**
   - 参考部署指南
   - 配置生产环境
   - 对外提供服务

## ❓ 常见问题

### Q: 必须配置阿里云 OSS 吗？
**A**: 不必须。OSS 仅用于图片上传功能，不配置不影响其他功能。

### Q: 可以修改和商用吗？
**A**: 可以！项目采用 MIT 许可，可自由使用和修改。

### Q: 遇到问题怎么办？
**A**: 
1. 查看 QUICKSTART.md 中的常见问题
2. 检查配置和日志
3. 参考完整文档
4. 提交 GitHub Issue

### Q: 如何贡献代码？
**A**: 欢迎提交 Pull Request！请遵循项目代码规范。

## 🌟 项目特点

### ⚡ 高效
- 快速启动
- 流畅操作
- 即时响应

### 🎨 美观
- 现代UI
- 流畅动画
- 精致细节

### 🔒 安全
- JWT 认证
- 权限控制
- 密码加密

### 📱 响应式
- 桌面适配
- 移动友好
- 多端支持

## 💬 获取支持

- 📖 查看文档
- 🐛 提交 Issue
- 💡 功能建议
- ⭐ 给项目加星

## 🎉 开始你的日历之旅！

**不要犹豫，现在就开始！**

按照上面的5步骤，5分钟后你就能看到运行中的 QD日历了！

有任何问题，随时查看文档或提问。

**祝使用愉快！** ✨

---

**快速链接**:
- [快速启动 →](./QUICKSTART.md)
- [完整文档 →](./README.md)
- [检查清单 →](./CHECKLIST.md)
- [快速参考 →](./QUICK_REFERENCE.md)

---

**QD日历 v1.0.0** | MIT License | 2025

