# QD日历前端

基于 Vue3 + Vite 的现代化日历应用前端。

## 快速开始

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

## 项目结构

```
frontend/
├── public/              # 静态资源
├── src/
│   ├── api/            # API 接口
│   │   ├── axios.js    # Axios 配置
│   │   ├── auth.js     # 认证接口
│   │   └── events.js   # 日程接口
│   ├── components/     # 公共组件
│   ├── router/         # 路由配置
│   │   └── index.js
│   ├── stores/         # Pinia 状态管理
│   │   ├── auth.js     # 认证状态
│   │   └── events.js   # 日程状态
│   ├── views/          # 页面组件
│   │   ├── Home.vue    # 首页
│   │   ├── Login.vue   # 登录页
│   │   ├── Register.vue # 注册页
│   │   ├── Calendar.vue # 日历页
│   │   └── Admin.vue   # 管理页
│   ├── App.vue         # 根组件
│   ├── main.js         # 入口文件
│   └── style.css       # 全局样式
├── index.html          # HTML 模板
├── vite.config.js      # Vite 配置
└── package.json        # 依赖配置
```

## 技术栈

- **Vue 3.4** - Composition API
- **Vite 5** - 构建工具
- **Pinia** - 状态管理
- **Vue Router 4** - 路由管理
- **Element Plus** - UI 组件库
- **V-Calendar** - 日历组件
- **Axios** - HTTP 客户端
- **Day.js** - 日期处理

## 开发指南

### 添加新页面

1. 在 `src/views/` 创建页面组件
2. 在 `src/router/index.js` 添加路由配置
3. 根据需要配置路由守卫

### 添加新 API

1. 在 `src/api/` 对应文件中添加 API 函数
2. 使用统一的 axios 实例
3. 在组件或 store 中调用

### 状态管理

使用 Pinia 管理全局状态：
- `auth.js` - 用户认证状态
- `events.js` - 日程数据状态

### 样式规范

- 使用 CSS 变量定义主题颜色
- 组件样式使用 scoped
- 动画效果使用 CSS transition

## 环境变量

开发环境自动代理 API 请求到 http://localhost:5000

生产环境需要配置实际的 API 地址。

## 部署

### 构建

```bash
npm run build
```

构建产物在 `dist/` 目录。

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

