# QD日历 - 共享日程管理系统

一个基于 Vue3 和 Flask 的现代化日历应用，具有严格的权限控制和动态效果。

## 📋 功能特性

### 核心功能
- ✅ **日历视图**：美观的月历展示，支持日程概览
- ✅ **日程管理**：创建、编辑、删除日程（管理员专属）
- ✅ **权限控制**：管理员、普通用户、游客三级权限
- ✅ **图片上传**：支持本地文件存储背景图片
- ✅ **动态效果**：流畅的过渡动画和悬浮窗口
- ✅ **响应式设计**：适配桌面端和移动端

### 权限说明
- **管理员**：可以创建、编辑、删除所有日程
- **普通用户**：只能查看日程
- **游客**：只能查看日程（无需注册）

## 🛠 技术栈

### 前端
- Vue 3.4 - 渐进式 JavaScript 框架
- Vite 5 - 下一代前端构建工具
- Pinia - Vue 状态管理
- Element Plus - UI 组件库
- V-Calendar - 日历组件
- Axios - HTTP 客户端
- Day.js - 日期处理库

### 后端
- Flask 3.0 - Python Web 框架
- Flask-SQLAlchemy - ORM 数据库
- Flask-RESTful - RESTful API
- Flask-JWT-Extended - JWT 认证
- Flask-CORS - 跨域支持
- MySQL - 关系型数据库

## 📦 安装部署

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 5.7+

### 后端部署

1. **进入后端目录**
```bash
cd backend
```

2. **创建虚拟环境**
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
# 或
env\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

5. **创建数据库**
```bash
# 在 MySQL 中执行
CREATE DATABASE qd_calendar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. **启动应用**
```bash
python app.py
```

后端服务将在 http://localhost:5002 启动

### 前端部署

1. **进入前端目录**
```bash
cd frontend
```

2. **安装依赖**
```bash
npm install
# 或
yarn install
```

3. **开发模式启动**
```bash
npm run dev
# 或
yarn dev
```

前端服务将在 http://localhost:3000 启动

4. **生产构建**
```bash
npm run build
# 或
yarn build
```

## 🔧 配置说明

### 后端配置 (.env)

```env
# Flask 配置
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=qd_calendar
DB_USER=root
DB_PASSWORD=your-password

# 本地文件存储配置（可选）
UPLOAD_FOLDER=uploads
FILE_SERVER_URL=/uploads

# 管理员配置
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### 文件存储说明

图片文件默认保存在 `backend/uploads/` 目录下：
- 自动按日期分类（年/月/日）
- 文件名格式：`日期_UUID.扩展名`
- 通过 `/uploads/` URL 路径访问

## 📱 使用指南

### 首次使用

1. **访问首页**：http://localhost:3000
2. **游客浏览**：点击"游客浏览"直接查看日历
3. **注册账号**：点击"注册账号"创建普通用户账号
4. **管理员登录**：使用配置的管理员账号登录（默认 admin/admin123）

### 管理员操作

1. 登录管理员账号
2. 进入管理面板
3. 点击"创建日程"添加新日程
4. 填写日程信息、上传背景图片
5. 保存日程

### 查看日程

1. 进入日历视图
2. 点击日期查看当天所有日程
3. 点击日程条目查看详细信息
4. 使用筛选器按状态/优先级过滤

## 🎨 界面预览

### 日历视图
- 月历网格展示
- 每日日程概览
- 背景图片展示
- 优先级颜色标识

### 管理面板
- 日程列表表格
- 搜索和筛选功能
- 创建/编辑对话框
- 图片上传功能

## 🔐 API 端点

### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/guest-login` - 游客登录
- `GET /api/auth/profile` - 获取用户资料

### 日程相关
- `GET /api/events` - 获取日程列表
- `GET /api/events/:id` - 获取日程详情
- `POST /api/events` - 创建日程（管理员）
- `PUT /api/events/:id` - 更新日程（管理员）
- `DELETE /api/events/:id` - 删除日程（管理员）
- `GET /api/calendar` - 获取日历数据

### 文件上传
- `POST /api/upload/image` - 上传图片（管理员）

## 🚀 开发计划

- [ ] 添加日程提醒功能
- [ ] 支持日程导出（iCal格式）
- [ ] 添加日程统计图表
- [ ] 支持日程评论功能
- [ ] 移动端 App 开发

## 📄 许可证

MIT License

## 👥 贡献者

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

如有问题或建议，请通过以下方式联系：
- GitHub Issues
- Email: support@qd-calendar.com

---

© 2025 QD日历. All rights reserved.

