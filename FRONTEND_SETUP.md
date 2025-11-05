# 前端新功能启动指南

## 📋 新增功能

已添加以下前端页面：
1. **人员管理** (`/members`) - 管理员专属
2. **数据分析** (`/analytics`) - 所有登录用户可访问

## 🚀 快速启动

### 1. 安装 ECharts 依赖

```bash
cd frontend
npm install echarts
```

或使用 yarn:

```bash
cd frontend
yarn add echarts
```

### 2. 启动前端开发服务器

```bash
npm run dev
```

或

```bash
yarn dev
```

### 3. 访问新功能

启动后，访问 http://localhost:3000

#### 导航路径：
- **日历页面** → 点击顶部 "数据分析" 按钮
- **日历页面** → 点击顶部 "人员管理" 按钮（仅管理员）

## 📊 功能说明

### 人员管理页面 (`/members`)

**权限**: 仅管理员可访问

**功能**:
- ✅ 查看人员列表（支持分页）
- ✅ 搜索人员（姓名、部门、职位）
- ✅ 添加新人员
- ✅ 编辑人员信息
- ✅ 删除人员
- ✅ 人员状态管理（激活/停用）

**字段**:
- 姓名 *(必填)*
- 部门
- 职位
- 电话
- 邮箱
- 状态（激活/停用）

### 数据分析页面 (`/analytics`)

**权限**: 所有登录用户可访问

**功能**:
- ✅ 数据总览卡片
  - 总活动数
  - 已完成活动数
  - 完成率
  - 参与人数

- ✅ 活动状态分布饼图
  - 待处理 / 进行中 / 已完成 / 已取消

- ✅ 活动优先级分布饼图
  - 高 / 中 / 低

- ✅ 每日活动数量趋势折线图
  - 显示本月每天的活动数量变化

- ✅ 参与人数 TOP 5 活动排行榜
  - 活动名称、日期、参与人数、状态、优先级

- ✅ 人员参与度 TOP 10
  - 姓名、部门、参与活动次数、活跃度进度条

**日期选择**:
- 可以选择不同月份查看数据
- 默认显示当前月份

## 🎨 页面预览

### 人员管理页面
```
┌─────────────────────────────────────────┐
│  人员管理                  [+ 添加人员]  │
├─────────────────────────────────────────┤
│  [搜索框] [状态筛选▼] [搜索]            │
├─────────────────────────────────────────┤
│  ID  姓名  部门  职位  电话  邮箱  状态  │
│   1  张三  技术部 工程师 138... ✓激活   │
│   2  李四  产品部 经理  139... ✓激活    │
│  ...                                    │
└─────────────────────────────────────────┘
```

### 数据分析页面
```
┌─────────────────────────────────────────┐
│  数据分析              [2025年10月 ▼]   │
├──────┬──────┬──────┬──────────────────┤
│  📅  │  ✓   │  📈  │   👤             │
│  15  │  10  │ 66%  │   45             │
│ 总活动│ 已完成│完成率│  参与人数        │
├──────┴──────┴──────┴──────────────────┤
│  [状态分布饼图]  [优先级分布饼图]       │
│  [每日趋势折线图]                      │
│  [TOP活动排行表]                       │
│  [人员参与度排行表]                     │
└─────────────────────────────────────────┘
```

## 📝 新增文件清单

### API 服务层
- `frontend/src/api/members.js` - 人员管理 API
- `frontend/src/api/analytics.js` - 数据分析 API

### 页面组件
- `frontend/src/views/Members.vue` - 人员管理页面
- `frontend/src/views/Analytics.vue` - 数据分析页面

### 路由配置
- 更新 `frontend/src/router/index.js`
  - 添加 `/members` 路由
  - 添加 `/analytics` 路由

### 导航更新
- 更新 `frontend/src/views/Calendar.vue`
  - 添加 "数据分析" 按钮
  - 添加 "人员管理" 按钮

## 🔧 技术栈

- **Vue 3** - 组合式 API
- **Element Plus** - UI 组件库
- **ECharts** - 数据可视化图表库
- **Axios** - HTTP 请求
- **Vue Router** - 路由管理
- **Pinia** - 状态管理

## 💡 使用示例

### 1. 添加人员

```javascript
// 管理员登录后访问 /members
// 点击 "添加人员" 按钮
// 填写表单：
{
  name: "张三",
  department: "技术部",
  position: "工程师",
  phone: "13800138001",
  email: "zhangsan@example.com",
  is_active: true
}
```

### 2. 查看数据分析

```javascript
// 任何登录用户访问 /analytics
// 选择月份：2025年10月
// 自动加载并展示：
// - 总览数据
// - 图表数据
// - 排行榜
```

### 3. 为活动添加参与者

```javascript
// 在管理面板创建/编辑活动时
// 添加 member_ids 字段：
{
  title: "团建活动",
  event_date: "2025-11-15",
  member_ids: [1, 2, 3, 4, 5]  // 人员ID数组
}
```

## 🐛 故障排查

### 问题1: ECharts 图表不显示

**原因**: 未安装 echarts 依赖

**解决**:
```bash
cd frontend
npm install echarts
```

### 问题2: 404 错误

**原因**: 后端服务未启动或端口不对

**解决**:
```bash
cd backend
source env/bin/activate
python app.py
```

确保后端运行在 `http://localhost:5002`

### 问题3: 数据为空

**原因**: 数据库中没有人员或活动数据

**解决**:
1. 先在人员管理页面添加几个人员
2. 在管理面板创建活动并添加参与人员
3. 刷新数据分析页面

### 问题4: 图表大小不对

**原因**: 窗口大小变化时图表未重新渲染

**解决**: 页面已添加自动 resize 监听，刷新页面即可

## 📱 响应式设计

- ✅ 桌面端完美显示
- ✅ 平板适配
- ✅ 移动端基础支持（建议在桌面端使用数据分析功能）

## 🎨 自定义配置

### 修改图表颜色

编辑 `frontend/src/views/Analytics.vue`:

```javascript
// 状态分布饼图颜色
color: ['#409EFF', '#E6A23C', '#67C23A', '#F56C6C']

// 优先级分布饼图颜色
color: ['#F56C6C', '#E6A23C', '#909399']
```

### 修改分页大小

编辑 `frontend/src/views/Members.vue`:

```javascript
const pageSize = ref(20)  // 改为你想要的每页数量
```

## 🚀 部署建议

### 生产环境构建

```bash
cd frontend
npm run build
```

生成的文件在 `frontend/dist` 目录

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 前端
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # API
    location /api {
        proxy_pass http://localhost:5002;
    }
    
    # 上传文件
    location /uploads {
        proxy_pass http://localhost:5002;
    }
}
```

## 📖 相关文档

- [ECharts 官方文档](https://echarts.apache.org/zh/index.html)
- [Element Plus 文档](https://element-plus.org/zh-CN/)
- [Vue 3 文档](https://cn.vuejs.org/)
- [后端 API 文档](./MEMBERS_AND_ANALYTICS_FEATURE.md)

## ✅ 完成检查清单

- [ ] 安装 ECharts 依赖
- [ ] 启动后端服务（5002端口）
- [ ] 启动前端服务（3000端口）
- [ ] 管理员登录
- [ ] 访问人员管理页面
- [ ] 添加几个测试人员
- [ ] 创建活动并添加参与人员
- [ ] 访问数据分析页面
- [ ] 查看图表和统计数据

---

**准备就绪后，开始使用新功能！** 🎉




