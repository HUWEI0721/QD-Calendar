# QD日历快速参考

## 🚀 一键启动命令

### 后端启动
```bash
cd backend
source env/bin/activate  # 激活虚拟环境
python app.py
```

### 前端启动
```bash
cd frontend
npm run dev
```

## 🔑 默认账号

| 角色 | 用户名 | 密码 | 权限 |
|------|--------|------|------|
| 管理员 | admin | admin123 | 所有权限 |
| 测试用户 | testuser | password123 | 只读 |
| 游客 | - | - | 只读（免登录） |

## 🌐 访问地址

- **前端**: http://localhost:3000
- **后端 API**: http://localhost:5000
- **健康检查**: http://localhost:5000/api/health

## 📡 API 端点速查

### 认证接口
```
POST /api/auth/register        # 注册
POST /api/auth/login          # 登录
POST /api/auth/guest-login    # 游客登录
GET  /api/auth/profile        # 获取用户信息
```

### 日程接口
```
GET    /api/events            # 获取日程列表
POST   /api/events            # 创建日程（管理员）
GET    /api/events/:id        # 获取日程详情
PUT    /api/events/:id        # 更新日程（管理员）
DELETE /api/events/:id        # 删除日程（管理员）
GET    /api/calendar          # 获取日历数据
POST   /api/upload/image      # 上传图片（管理员）
```

## 🗂️ 项目结构速览

```
QD-Calendar/
├── backend/          # Flask 后端
│   ├── app.py       # 应用入口
│   ├── models.py    # 数据模型
│   ├── resources/   # API 资源
│   └── utils/       # 工具函数
├── frontend/         # Vue3 前端
│   └── src/
│       ├── views/   # 页面组件
│       ├── stores/  # 状态管理
│       ├── api/     # API 封装
│       └── router/  # 路由配置
└── docs/            # 文档文件
```

## 💻 常用命令

### 后端命令
```bash
# 创建虚拟环境
python3 -m venv env

# 激活虚拟环境（Mac/Linux）
source env/bin/activate

# 激活虚拟环境（Windows）
env\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动应用（开发模式）
python app.py

# 启动应用（生产模式）
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 前端命令
```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build

# 预览构建
npm run preview
```

### 数据库命令
```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE qd_calendar CHARACTER SET utf8mb4;

# 删除数据库（谨慎！）
DROP DATABASE qd_calendar;

# 备份数据库
mysqldump -u root -p qd_calendar > backup.sql

# 恢复数据库
mysql -u root -p qd_calendar < backup.sql
```

## 🎨 状态和优先级

### 日程状态
- `pending` - 待处理（蓝色）
- `in_progress` - 进行中（橙色）
- `completed` - 已完成（绿色）
- `cancelled` - 已取消（红色）

### 优先级
- `high` - 高优先级（红色边框）
- `medium` - 中优先级（橙色边框）
- `low` - 低优先级（灰色边框）

## 🔧 环境变量速查

### 必需配置
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DB_HOST=localhost
DB_PORT=3306
DB_NAME=qd_calendar
DB_USER=root
DB_PASSWORD=your-password
```

### 可选配置
```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
OSS_ACCESS_KEY_ID=your-key
OSS_ACCESS_KEY_SECRET=your-secret
OSS_BUCKET_NAME=your-bucket
```

## 📝 请求示例

### 登录请求
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### 创建日程
```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title":"新日程",
    "event_date":"2025-11-01",
    "priority":"high",
    "status":"pending"
  }'
```

### 获取日程列表
```bash
curl -X GET "http://localhost:5000/api/events?start_date=2025-11-01&end_date=2025-11-30"
```

## 🐛 调试技巧

### 查看后端日志
```bash
# 实时日志
tail -f /var/log/qd-calendar/access.log
tail -f /var/log/qd-calendar/error.log
```

### 前端调试
- 打开浏览器开发者工具（F12）
- 查看 Console 标签页错误信息
- 查看 Network 标签页网络请求
- 查看 Application 标签页本地存储

### 数据库调试
```sql
-- 查看用户表
SELECT * FROM users;

-- 查看日程表
SELECT * FROM events;

-- 查看特定日期的日程
SELECT * FROM events WHERE event_date = '2025-11-01';

-- 查看管理员创建的日程
SELECT * FROM events WHERE created_by IN (
  SELECT id FROM users WHERE role = 'admin'
);
```

## 🔐 安全提示

- ⚠️ 修改默认管理员密码
- ⚠️ 不要提交 .env 文件到 Git
- ⚠️ 生产环境使用强密钥
- ⚠️ 启用 HTTPS
- ⚠️ 定期更新依赖包

## 📊 性能优化提示

### 后端优化
- 使用数据库索引
- 启用查询缓存
- 使用 Redis 缓存
- 限制单次查询数量

### 前端优化
- 启用路由懒加载
- 压缩静态资源
- 使用 CDN
- 图片懒加载

## 🎯 快速跳转

- [完整文档](./README.md)
- [快速启动](./QUICKSTART.md)
- [项目结构](./PROJECT_STRUCTURE.md)
- [部署指南](./DEPLOYMENT.md)
- [启动检查清单](./CHECKLIST.md)
- [项目总结](./PROJECT_SUMMARY.md)

## 📞 获取帮助

遇到问题？
1. 查看文档
2. 检查日志
3. 搜索错误信息
4. 提交 Issue

## 🎉 快捷键（开发时）

### VS Code
- `Ctrl/Cmd + B` - 切换侧边栏
- `Ctrl/Cmd + P` - 快速打开文件
- `Ctrl/Cmd + Shift + F` - 全局搜索
- `Ctrl/Cmd + \`` - 打开终端

### 浏览器
- `F12` - 开发者工具
- `Ctrl/Cmd + Shift + R` - 强制刷新
- `Ctrl/Cmd + Shift + I` - 审查元素

---

**提示**: 将此文件加入收藏，随时查阅！⭐

