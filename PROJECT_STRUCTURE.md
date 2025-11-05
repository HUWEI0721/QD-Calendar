# QD日历项目结构说明

## 项目概览

```
QD-Calendar/
├── backend/                    # Flask 后端
│   ├── resources/             # API 资源模块
│   │   ├── __init__.py
│   │   ├── auth.py           # 认证接口（注册、登录、游客登录）
│   │   └── events.py         # 日程接口（CRUD、日历数据、图片上传）
│   ├── utils/                # 工具函数
│   │   ├── __init__.py
│   │   └── oss_helper.py     # 阿里云 OSS 操作助手
│   ├── app.py                # 应用入口，初始化 Flask 和注册路由
│   ├── config.py             # 配置管理（开发/生产环境）
│   ├── models.py             # 数据库模型（User、Event）
│   ├── requirements.txt      # Python 依赖包
│   ├── .env.example          # 环境变量示例
│   ├── .gitignore           # Git 忽略文件
│   ├── run.sh               # 启动脚本
│   └── README.md            # 后端文档
│
├── frontend/                  # Vue3 前端
│   ├── public/               # 静态资源
│   ├── src/
│   │   ├── api/             # API 接口层
│   │   │   ├── axios.js     # Axios 配置和拦截器
│   │   │   ├── auth.js      # 认证 API
│   │   │   └── events.js    # 日程 API
│   │   ├── components/      # 公共组件（预留）
│   │   ├── router/          # 路由配置
│   │   │   └── index.js     # Vue Router 配置和路由守卫
│   │   ├── stores/          # Pinia 状态管理
│   │   │   ├── auth.js      # 认证状态（用户信息、token）
│   │   │   └── events.js    # 日程状态（日程列表、日历数据）
│   │   ├── views/           # 页面组件
│   │   │   ├── Home.vue     # 首页（营销页面）
│   │   │   ├── Login.vue    # 登录页面
│   │   │   ├── Register.vue # 注册页面
│   │   │   ├── Calendar.vue # 日历视图（核心功能）
│   │   │   └── Admin.vue    # 管理面板（仅管理员）
│   │   ├── App.vue          # 根组件
│   │   ├── main.js          # 应用入口
│   │   └── style.css        # 全局样式
│   ├── index.html           # HTML 模板
│   ├── vite.config.js       # Vite 配置
│   ├── package.json         # Node 依赖
│   ├── .gitignore          # Git 忽略文件
│   └── README.md           # 前端文档
│
├── README.md                 # 项目主文档
├── QUICKSTART.md            # 快速启动指南
├── PROJECT_STRUCTURE.md     # 本文件
└── .gitignore              # 根目录 Git 忽略文件
```

## 核心模块说明

### 后端模块

#### 1. models.py - 数据模型层
定义了两个核心模型：
- **User**: 用户模型，包含认证信息和角色权限
- **Event**: 日程模型，包含日程的所有信息

关键功能：
- 密码哈希存储
- 角色权限枚举（admin/user/guest）
- 优先级和状态管理
- 时间戳自动更新

#### 2. resources/auth.py - 认证接口
实现用户认证相关的 RESTful API：
- `RegisterResource`: 用户注册
- `LoginResource`: 用户登录
- `GuestLoginResource`: 游客登录
- `RefreshTokenResource`: 刷新令牌
- `UserProfileResource`: 获取用户资料

安全特性：
- JWT 令牌认证
- 密码哈希加密
- 游客自动创建

#### 3. resources/events.py - 日程接口
实现日程管理的 RESTful API：
- `EventListResource`: 日程列表（GET/POST）
- `EventDetailResource`: 日程详情（GET/PUT/DELETE）
- `EventCalendarResource`: 日历数据（按月获取）
- `ImageUploadResource`: 图片上传

权限控制：
- `@admin_required` 装饰器确保只有管理员可以修改
- `@jwt_required(optional=True)` 允许未登录用户查看

#### 4. utils/oss_helper.py - OSS 工具
阿里云对象存储操作封装：
- 文件上传到 OSS
- 文件删除
- 文件存在性检查
- 自动生成唯一文件名

#### 5. config.py - 配置管理
环境配置管理：
- 开发环境配置
- 生产环境配置
- 数据库连接配置
- OSS 配置
- JWT 配置

#### 6. app.py - 应用入口
Flask 应用初始化：
- 扩展初始化（SQLAlchemy、JWT、CORS）
- 路由注册
- 错误处理
- 数据库表创建
- 默认管理员创建

### 前端模块

#### 1. stores/auth.js - 认证状态
Pinia store 管理用户认证状态：
- 用户登录/注册/登出
- JWT token 管理
- 用户角色判断
- 认证状态持久化

#### 2. stores/events.js - 日程状态
Pinia store 管理日程数据：
- 日程列表获取和缓存
- 日程 CRUD 操作
- 日历数据管理
- 加载状态管理

#### 3. api/axios.js - HTTP 客户端
Axios 配置和拦截器：
- 请求拦截器（添加 token）
- 响应拦截器（错误处理）
- 统一错误提示
- 自动 token 刷新

#### 4. router/index.js - 路由配置
Vue Router 配置：
- 页面路由定义
- 路由元信息（requiresAuth、requiresAdmin）
- 路由守卫（权限检查）
- 重定向逻辑

#### 5. views/Calendar.vue - 日历视图（核心）
应用的核心功能页面：
- 月历网格展示
- 日程卡片显示
- 日程详情弹窗
- 日程列表弹窗
- 筛选功能
- 背景图片展示
- 优先级颜色标识
- 动态效果

组件结构：
```
Calendar.vue
├── header (顶部导航)
├── calendar-controls (月份切换、筛选器)
├── calendar-grid (日历网格)
│   └── calendar-day (日历单元格)
│       ├── day-header (日期和事件数量)
│       ├── day-background (背景图)
│       └── day-events (事件列表)
├── day-events-dialog (日程列表弹窗)
└── event-detail-dialog (日程详情弹窗)
```

#### 6. views/Admin.vue - 管理面板
管理员专用页面：
- 日程表格展示
- 搜索和筛选
- 创建日程对话框
- 编辑日程对话框
- 删除确认
- 图片上传

表单验证：
- 标题必填
- 日期必填
- 优先级和状态选择
- 图片格式和大小限制

#### 7. views/Login.vue & Register.vue - 认证页面
用户认证界面：
- 表单验证
- 动态背景动画
- 游客登录快捷入口
- 页面间跳转

#### 8. views/Home.vue - 首页
营销和导航页面：
- Hero 区域（标题、描述、CTA）
- 功能展示
- 动态卡片动画
- 导航菜单

## 数据流

### 认证流程
```
用户输入 → LoginResource → JWT生成 → 前端存储token → 后续请求携带token
```

### 日程创建流程（管理员）
```
管理员表单 → uploadImage(OSS) → createEvent(API) → 数据库保存 → 返回结果 → 更新前端状态
```

### 日历查看流程
```
选择月份 → getCalendar(API) → 按日期分组 → 渲染日历网格 → 点击查看详情
```

## 权限层级

### 三级权限系统
1. **游客（guest）**
   - 只能查看日程
   - 无需注册
   - 访问受限

2. **普通用户（user）**
   - 只能查看日程
   - 需要注册登录
   - 可查看完整信息

3. **管理员（admin）**
   - 所有查看权限
   - 创建、编辑、删除日程
   - 上传图片
   - 访问管理面板

### 权限实现
- 后端：装饰器 `@admin_required`
- 前端：路由守卫 + 组件条件渲染

## 技术亮点

### 后端
✅ RESTful API 设计
✅ JWT 令牌认证
✅ 角色权限控制
✅ ORM 数据库操作
✅ 阿里云 OSS 集成
✅ 错误处理和日志
✅ CORS 跨域支持

### 前端
✅ Composition API
✅ Pinia 状态管理
✅ 响应式设计
✅ 动态过渡动画
✅ 表单验证
✅ 错误处理
✅ Loading 状态
✅ 悬浮窗口
✅ 筛选和搜索

## 扩展方向

### 可能的功能扩展
- [ ] 日程提醒推送
- [ ] 日程导出（iCal）
- [ ] 多日历视图（周视图、列表视图）
- [ ] 日程评论和协作
- [ ] 日程标签和分类
- [ ] 数据统计和图表
- [ ] 移动端 App
- [ ] WebSocket 实时更新
- [ ] 邮件通知
- [ ] 日程模板

### 性能优化
- [ ] Redis 缓存
- [ ] 数据库索引优化
- [ ] 图片懒加载
- [ ] 虚拟滚动
- [ ] CDN 加速
- [ ] 代码分割

### 安全增强
- [ ] 双因素认证
- [ ] API 限流
- [ ] SQL 注入防护
- [ ] XSS 防护
- [ ] CSRF 防护
- [ ] 安全审计日志

## 开发规范

### 代码风格
- Python: PEP 8
- JavaScript: ESLint
- Vue: Vue 官方风格指南

### Git 提交规范
```
feat: 新功能
fix: 修复
docs: 文档
style: 格式
refactor: 重构
test: 测试
chore: 构建
```

### 分支管理
- main: 生产分支
- develop: 开发分支
- feature/*: 功能分支
- hotfix/*: 修复分支

