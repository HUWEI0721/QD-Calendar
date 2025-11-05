# 人员管理与数据分析功能

## 📋 功能概述

新增了完整的**人员管理**和**数据分析**模块，支持活动人员统计和可视化数据分析。

**版本**: v1.2.0  
**日期**: 2025-10-30

---

## 🆕 新增功能

### 1. 人员管理模块
- ✅ 添加/编辑/删除人员
- ✅ 人员信息管理（姓名、电话、邮箱、部门、职位）
- ✅ 人员状态管理（激活/停用）
- ✅ 人员搜索和筛选
- ✅ 人员统计

### 2. 活动人数统计
- ✅ 每个活动可添加参与人员
- ✅ 自动统计参与人数
- ✅ 显示参与人员列表
- ✅ 支持多对多关系（一个人可参与多个活动）

### 3. 数据分析模块
- ✅ 月度活动总览
- ✅ 活动完成率分析
- ✅ 参与人数统计
- ✅ 按状态/优先级分布
- ✅ 每日活动趋势
- ✅ TOP活动排行
- ✅ 人员参与度分析
- ✅ 部门参与统计

---

## 🗄️ 数据库变更

### 新增表

#### 1. members 表（人员表）
```sql
CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,           -- 姓名
    phone VARCHAR(20),                     -- 电话
    email VARCHAR(120),                    -- 邮箱
    department VARCHAR(100),               -- 部门
    position VARCHAR(100),                 -- 职位
    is_active BOOLEAN DEFAULT TRUE,        -- 是否激活
    created_at DATETIME,                   -- 创建时间
    updated_at DATETIME                    -- 更新时间
);
```

#### 2. event_members 表（事件参与者关联表）
```sql
CREATE TABLE event_members (
    event_id INTEGER NOT NULL,             -- 事件ID
    member_id INTEGER NOT NULL,            -- 人员ID
    created_at DATETIME,                   -- 添加时间
    PRIMARY KEY (event_id, member_id),
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
);
```

### 更新表

#### events 表新增字段
```sql
ALTER TABLE events ADD COLUMN participant_count INTEGER DEFAULT 0;
```

---

## 🔌 API 接口

### 人员管理 API

#### 1. 获取人员列表
```
GET /api/members
Authorization: Bearer <token>

Query Parameters:
- page: 页码（默认1）
- per_page: 每页数量（默认50）
- is_active: 筛选状态（true/false）
- search: 搜索关键词（姓名、部门、职位）

Response:
{
  "members": [...],
  "total": 100,
  "pages": 2,
  "current_page": 1
}
```

#### 2. 创建人员
```
POST /api/members
Authorization: Bearer <token> (Admin only)
Content-Type: application/json

{
  "name": "张三",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "department": "技术部",
  "position": "工程师",
  "is_active": true
}

Response:
{
  "message": "人员创建成功",
  "member": {...}
}
```

#### 3. 获取人员详情
```
GET /api/members/<member_id>
Authorization: Bearer <token>

Response:
{
  "id": 1,
  "name": "张三",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "department": "技术部",
  "position": "工程师",
  "is_active": true,
  "event_count": 5,
  "created_at": "2025-10-30T12:00:00",
  "updated_at": "2025-10-30T12:00:00"
}
```

#### 4. 更新人员信息
```
PUT /api/members/<member_id>
Authorization: Bearer <token> (Admin only)
Content-Type: application/json

{
  "name": "张三",
  "department": "产品部",
  "is_active": false
}
```

#### 5. 删除人员
```
DELETE /api/members/<member_id>
Authorization: Bearer <token> (Admin only)
```

#### 6. 人员统计
```
GET /api/members/stats
Authorization: Bearer <token>

Response:
{
  "total_members": 50,
  "inactive_members": 5,
  "departments": [
    {"name": "技术部", "count": 20},
    {"name": "产品部", "count": 15}
  ]
}
```

### 数据分析 API

#### 1. 数据分析总览
```
GET /api/analytics/overview
Authorization: Bearer <token>

Query Parameters:
- year: 年份（默认当前年）
- month: 月份（默认当前月）

Response:
{
  "period": {
    "year": 2025,
    "month": 10,
    "start_date": "2025-10-01",
    "end_date": "2025-10-31"
  },
  "overview": {
    "total_events": 15,
    "completed_events": 10,
    "completion_rate": 66.7,
    "total_participants": 120,
    "unique_participants": 45,
    "avg_participants_per_event": 8.0
  },
  "status_distribution": [
    {"status": "pending", "count": 3, "label": "待处理"},
    {"status": "completed", "count": 10, "label": "已完成"}
  ],
  "priority_distribution": [
    {"priority": "high", "count": 5, "label": "高"},
    {"priority": "medium", "count": 8, "label": "中"}
  ],
  "daily_trend": [
    {"date": "2025-10-01", "count": 2},
    {"date": "2025-10-02", "count": 1}
  ]
}
```

#### 2. 活动详细分析
```
GET /api/analytics/events
Authorization: Bearer <token>

Query Parameters:
- year: 年份
- month: 月份

Response:
{
  "events": [
    {
      "id": 1,
      "title": "团队建设",
      "event_date": "2025-10-15",
      "start_time": "10:00",
      "status": "completed",
      "priority": "high",
      "participant_count": 25,
      "creator_name": "admin"
    }
  ],
  "top_events": [
    {/* TOP 5 参与人数最多的活动 */}
  ],
  "total": 15
}
```

#### 3. 人员参与分析
```
GET /api/analytics/members
Authorization: Bearer <token>

Query Parameters:
- year: 年份
- month: 月份

Response:
{
  "member_participation": [
    {
      "member_id": 1,
      "name": "张三",
      "department": "技术部",
      "event_count": 8
    }
  ],
  "department_participation": [
    {
      "department": "技术部",
      "member_count": 20,
      "event_count": 45,
      "avg_events_per_member": 2.3
    }
  ],
  "top_participants": [
    {/* TOP 10 参与最多的人员 */}
  ]
}
```

### 活动管理 API 更新

#### 创建活动（新增人员字段）
```
POST /api/events
Authorization: Bearer <token> (Admin only)
Content-Type: application/json

{
  "title": "团队建设",
  "description": "季度团建活动",
  "event_date": "2025-11-15",
  "start_time": "10:00:00",
  "end_time": "17:00:00",
  "priority": "high",
  "status": "pending",
  "background_image": "/uploads/...",
  "member_ids": [1, 2, 3, 4, 5]  // ✅ 新增：参与人员ID列表
}
```

#### 更新活动（支持更新人员）
```
PUT /api/events/<event_id>
Authorization: Bearer <token> (Admin only)
Content-Type: application/json

{
  "title": "团队建设（更新）",
  "member_ids": [1, 2, 3, 6, 7]  // ✅ 新增：更新参与人员
}
```

#### 获取活动详情（返回人员信息）
```
GET /api/events/<event_id>
Authorization: Bearer <token>

Response:
{
  "id": 1,
  "title": "团队建设",
  "participant_count": 5,  // ✅ 新增：参与人数
  "members": [             // ✅ 新增：参与人员列表
    {"id": 1, "name": "张三"},
    {"id": 2, "name": "李四"}
  ],
  ...
}
```

---

## 💻 使用示例

### 1. 添加人员
```javascript
// 前端代码示例
async function addMember() {
  const response = await axios.post('/api/members', {
    name: '张三',
    phone: '13800138000',
    email: 'zhangsan@example.com',
    department: '技术部',
    position: '工程师'
  })
  console.log(response.data)
}
```

### 2. 创建活动并添加参与人员
```javascript
async function createEventWithMembers() {
  const response = await axios.post('/api/events', {
    title: '团队建设',
    event_date: '2025-11-15',
    start_time: '10:00:00',
    member_ids: [1, 2, 3, 4, 5]  // 人员ID数组
  })
  console.log('创建成功，参与人数:', response.data.event.participant_count)
}
```

### 3. 获取数据分析
```javascript
async function getAnalytics() {
  const response = await axios.get('/api/analytics/overview', {
    params: {
      year: 2025,
      month: 10
    }
  })
  
  console.log('本月活动数:', response.data.overview.total_events)
  console.log('参与总人数:', response.data.overview.total_participants)
  console.log('完成率:', response.data.overview.completion_rate + '%')
}
```

### 4. 查询人员列表
```javascript
async function searchMembers() {
  const response = await axios.get('/api/members', {
    params: {
      search: '技术部',
      is_active: true,
      page: 1,
      per_page: 20
    }
  })
  
  console.log('找到人员:', response.data.total)
  console.log('人员列表:', response.data.members)
}
```

---

## 📊 数据可视化建议

### 1. 活动总览图表
- **卡片统计**: 总活动数、完成率、参与人数
- **饼图**: 状态分布、优先级分布
- **折线图**: 每日活动数量趋势
- **柱状图**: 部门参与度对比

### 2. 活动排行榜
- **表格**: TOP 5 参与人数最多的活动
- **进度条**: 各活动完成进度

### 3. 人员参与分析
- **排行榜**: TOP 10 活跃人员
- **柱状图**: 各部门参与人数
- **热力图**: 人员活动参与热度

### 4. 趋势分析
- **面积图**: 月度活动趋势
- **对比图**: 本月vs上月数据对比

---

## 🎨 前端实现建议

### 推荐使用的图表库
1. **ECharts** - 功能强大，中文文档完善
2. **Chart.js** - 轻量简洁
3. **Ant Design Charts** - 开箱即用
4. **VChart** - 现代化可视化库

### 示例：ECharts 饼图
```vue
<template>
  <div ref="chart" style="width: 100%; height: 400px"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

const chart = ref(null)

onMounted(async () => {
  const { data } = await axios.get('/api/analytics/overview')
  
  const myChart = echarts.init(chart.value)
  myChart.setOption({
    title: { text: '活动状态分布' },
    tooltip: {},
    series: [{
      type: 'pie',
      data: data.status_distribution.map(item => ({
        name: item.label,
        value: item.count
      }))
    }]
  })
})
</script>
```

---

## 🔄 数据库初始化

### 1. 手动创建表（如果自动创建失败）
```sql
-- 创建人员表
CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(120),
    department VARCHAR(100),
    position VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建关联表
CREATE TABLE event_members (
    event_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (event_id, member_id),
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
);

-- 更新事件表（可选，实际由关系计算）
ALTER TABLE events ADD COLUMN participant_count INTEGER DEFAULT 0;
```

### 2. 添加示例数据
```sql
-- 添加示例人员
INSERT INTO members (name, department, position, phone, email) VALUES
('张三', '技术部', '工程师', '13800138001', 'zhangsan@example.com'),
('李四', '产品部', '产品经理', '13800138002', 'lisi@example.com'),
('王五', '技术部', '架构师', '13800138003', 'wangwu@example.com'),
('赵六', '市场部', '市场专员', '13800138004', 'zhaoliu@example.com'),
('钱七', '技术部', '前端工程师', '13800138005', 'qianqi@example.com');

-- 为活动添加参与人员
INSERT INTO event_members (event_id, member_id) VALUES
(1, 1), (1, 2), (1, 3),  -- 活动1有3个参与者
(2, 2), (2, 4),          -- 活动2有2个参与者
(3, 1), (3, 3), (3, 5);  -- 活动3有3个参与者
```

---

## 🧪 测试步骤

### 1. 测试人员管理
```bash
# 1. 创建人员
curl -X POST http://localhost:5002/api/members \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"张三","department":"技术部"}'

# 2. 获取人员列表
curl http://localhost:5002/api/members \
  -H "Authorization: Bearer <token>"

# 3. 搜索人员
curl "http://localhost:5002/api/members?search=技术部" \
  -H "Authorization: Bearer <token>"
```

### 2. 测试活动人员关联
```bash
# 1. 创建活动并添加人员
curl -X POST http://localhost:5002/api/events \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"团建活动",
    "event_date":"2025-11-15",
    "member_ids":[1,2,3]
  }'

# 2. 查看活动详情（包含参与人数）
curl http://localhost:5002/api/events/1 \
  -H "Authorization: Bearer <token>"
```

### 3. 测试数据分析
```bash
# 1. 获取数据总览
curl "http://localhost:5002/api/analytics/overview?year=2025&month=10" \
  -H "Authorization: Bearer <token>"

# 2. 获取活动分析
curl "http://localhost:5002/api/analytics/events?year=2025&month=10" \
  -H "Authorization: Bearer <token>"

# 3. 获取人员参与分析
curl "http://localhost:5002/api/analytics/members?year=2025&month=10" \
  -H "Authorization: Bearer <token>"
```

---

## 📁 新增文件

1. `backend/resources/members.py` - 人员管理API
2. `backend/resources/analytics.py` - 数据分析API
3. `MEMBERS_AND_ANALYTICS_FEATURE.md` - 本文档

---

## 🔧 修改文件

1. `backend/models.py`
   - 新增 Member 模型
   - 新增 event_members 关联表
   - Event 模型添加 members 关系和 participant_count 字段

2. `backend/app.py`
   - 注册人员管理API路由
   - 注册数据分析API路由

3. `backend/resources/events.py`
   - 创建活动时支持添加 member_ids
   - 更新活动时支持更新 member_ids
   - 返回数据包含 participant_count 和 members

---

## 🎉 功能特点

### 优势
1. ✅ **完整的人员管理** - 增删改查全覆盖
2. ✅ **灵活的关联关系** - 多对多，支持一人参与多活动
3. ✅ **实时统计** - participant_count 实时计算
4. ✅ **丰富的数据分析** - 多维度统计分析
5. ✅ **易于可视化** - 数据格式适合图表展示
6. ✅ **权限控制** - 管理员才能管理人员
7. ✅ **搜索筛选** - 支持关键词搜索和状态筛选

### 应用场景
- 📊 活动效果评估
- 👥 人员参与度分析
- 📈 月度/季度数据报告
- 🏆 活动排行榜展示
- 📱 移动端数据看板

---

## 🚀 下一步建议

1. **前端开发**
   - 创建人员管理页面
   - 创建数据分析页面（图表展示）
   - 活动表单添加人员选择器

2. **功能增强**
   - 导出Excel报表
   - 数据对比（月度/年度）
   - 邮件通知参与者
   - 签到功能
   - 活动评价

3. **性能优化**
   - 缓存统计数据
   - 异步计算报表
   - 数据分页加载

---

**版本**: v1.2.0  
**更新时间**: 2025-10-30

