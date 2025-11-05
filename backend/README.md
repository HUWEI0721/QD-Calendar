# QD日历后端

基于 Flask 的 RESTful API 后端服务。

## 快速开始

```bash
# 创建虚拟环境
python -m venv env
source env/bin/activate  # Linux/Mac
# 或 env\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 创建数据库
# 在 MySQL 中执行：
CREATE DATABASE qd_calendar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 启动应用
python app.py
```

## 项目结构

```
backend/
├── resources/          # API 资源
│   ├── auth.py        # 认证相关接口
│   └── events.py      # 日程相关接口
├── utils/             # 工具函数
│   └── file_storage.py  # 本地文件存储助手
├── uploads/           # 上传文件目录
├── app.py             # 应用入口
├── config.py          # 配置文件
├── models.py          # 数据库模型
├── requirements.txt   # 依赖列表
├── .env.example       # 环境变量示例
└── run.sh            # 启动脚本
```

## API 文档

### 认证接口

#### 用户注册
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "user1",
  "password": "password123",
  "email": "user1@example.com"
}
```

#### 用户登录
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "user1",
  "password": "password123"
}

Response:
{
  "access_token": "xxx",
  "refresh_token": "xxx",
  "user": {...}
}
```

#### 游客登录
```
POST /api/auth/guest-login

Response:
{
  "access_token": "xxx",
  "user": {...}
}
```

#### 获取用户资料
```
GET /api/auth/profile
Authorization: Bearer <token>

Response:
{
  "id": 1,
  "username": "user1",
  "role": "user",
  "email": "user1@example.com"
}
```

### 日程接口

#### 获取日程列表
```
GET /api/events?start_date=2025-01-01&end_date=2025-01-31&status=pending&priority=high

Response:
{
  "events": [...],
  "count": 10
}
```

#### 获取日程详情
```
GET /api/events/1

Response:
{
  "id": 1,
  "title": "会议",
  "description": "...",
  "event_date": "2025-01-15",
  ...
}
```

#### 创建日程（管理员）
```
POST /api/events
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "title": "新日程",
  "description": "...",
  "event_date": "2025-01-15",
  "start_time": "09:00:00",
  "end_time": "10:00:00",
  "priority": "high",
  "status": "pending",
  "background_image": "https://..."
}
```

#### 更新日程（管理员）
```
PUT /api/events/1
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "title": "更新的日程",
  ...
}
```

#### 删除日程（管理员）
```
DELETE /api/events/1
Authorization: Bearer <admin_token>
```

#### 获取日历数据
```
GET /api/calendar?year=2025&month=1

Response:
{
  "year": 2025,
  "month": 1,
  "calendar": {
    "2025-01-15": [
      {
        "id": 1,
        "title": "会议",
        "event_date": "2025-01-15",
        ...
      }
    ]
  }
}
```

#### 上传图片（管理员）
```
POST /api/upload/image
Authorization: Bearer <admin_token>
Content-Type: multipart/form-data

file: <image_file>

Response:
{
  "message": "图片上传成功",
  "url": "https://..."
}
```

## 数据库模型

### User（用户）
- id: 主键
- username: 用户名（唯一）
- password_hash: 密码哈希
- role: 角色（admin/user/guest）
- email: 邮箱
- created_at: 创建时间
- updated_at: 更新时间

### Event（日程）
- id: 主键
- title: 标题
- description: 描述
- event_date: 日期
- start_time: 开始时间
- end_time: 结束时间
- background_image: 背景图片 URL
- priority: 优先级（low/medium/high）
- status: 状态（pending/in_progress/completed/cancelled）
- created_by: 创建者 ID（外键）
- created_at: 创建时间
- updated_at: 更新时间

## 权限控制

- **游客（guest）**：只能查看日程
- **普通用户（user）**：只能查看日程
- **管理员（admin）**：可以创建、编辑、删除日程，上传图片

## 文件存储配置

图片文件存储在本地 `uploads/` 目录：
- 自动按日期分类（年/月/日）
- 文件命名：`日期_UUID.扩展名`
- 通过 `/uploads/` URL 访问
- 支持的格式：jpg, jpeg, png, gif, webp

## 部署

### 使用 Gunicorn

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用 uWSGI

```bash
pip install uwsgi

uwsgi --http :5000 --wsgi-file app.py --callable app --processes 4 --threads 2
```

### Nginx 反向代理

```nginx
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 安全建议

1. 修改默认的 SECRET_KEY 和 JWT_SECRET_KEY
2. 使用强密码策略
3. 启用 HTTPS
4. 定期更新依赖包
5. 配置数据库访问限制
6. 使用防火墙限制访问

## 日志

应用日志默认输出到控制台，生产环境建议配置文件日志：

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 测试

```bash
# 运行测试
pytest

# 测试覆盖率
pytest --cov=. --cov-report=html
```

## 性能优化

1. 使用数据库连接池
2. 启用查询缓存
3. 添加数据库索引
4. 使用 Redis 缓存热点数据
5. 启用 Gzip 压缩

## 故障排查

### 数据库连接失败
- 检查 MySQL 服务是否启动
- 验证数据库配置信息
- 检查防火墙设置

### 文件上传失败
- 检查 uploads 目录权限
- 确认磁盘空间充足
- 验证文件格式是否支持
- 检查文件大小限制（默认16MB）

### JWT 认证失败
- 检查 token 是否过期
- 验证 JWT_SECRET_KEY 配置
- 确认请求头格式正确

