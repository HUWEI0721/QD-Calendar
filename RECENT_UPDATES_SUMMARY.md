# QD-Calendar 最近更新总结

## 📅 更新日期
2025-11-05

## 🎯 本次更新内容

### 1. ✨ 主页活动轮播功能

**功能描述**：在主页新增活动轮播组件，自动展示当天及未来一周内的活动。

**核心特性**：
- ✅ 自动循环播放（每5秒切换）
- ✅ 支持左右箭头手动切换
- ✅ 显示活动海报、标题、时间、地点、主办部门、预计参与人数
- ✅ 仅展示已上传海报图片的活动
- ✅ 优雅的卡片式设计，支持点击查看详情

**相关文件**：
- `frontend/src/components/EventCarousel.vue` - 轮播组件
- `frontend/src/views/Home.vue` - 主页集成
- `frontend/src/api/events.js` - API接口
- `backend/resources/events.py` - 后端API实现

**API端点**：
- `GET /api/events/upcoming` - 获取近期活动

---

### 2. 🗂️ 活动数据库字段扩展

**新增字段**：

| 字段名 | 类型 | 说明 | 是否必填 |
|-------|------|------|---------|
| `organizer_department` | String(100) | 举办部门 | 是* |
| `expected_participants` | Integer | 预计参与人数 | 否 |
| `location` | String(200) | 活动地点 | 是* |

\* 在轮播展示的活动中为必填项

**数据库迁移**：
- 文件：`backend/migrations/add_event_fields.py`
- 状态：✅ 已执行

**相关文件**：
- `backend/models.py` - Event模型更新
- `backend/resources/events.py` - API验证逻辑

---

### 3. 🖼️ 在线图片URL支持

**功能描述**：支持用户通过粘贴在线图片URL的方式上传活动海报。

**使用方式**：
1. 在管理面板创建/编辑活动
2. 在"活动海报"区域，可以选择：
   - **本地上传**：点击上传按钮选择本地图片
   - **在线URL**：在输入框中粘贴图片URL

**支持的URL格式**：
- `http://example.com/image.jpg`
- `https://example.com/image.jpg`

**相关文件**：
- `frontend/src/views/Admin.vue` - 管理面板UI更新

---

### 4. 🔧 图片URL解析修复

**问题**：前端无法正确解析在线图片URL。

**解决方案**：统一了所有组件的图片URL处理逻辑，支持三种格式：

1. **在线URL**：`http(s)://...` → 直接使用
2. **绝对路径**：`/uploads/...` → 拼接后端地址
3. **相对路径**：`uploads/...` → 拼接后端地址

**修复的组件**：
- ✅ `EventCarousel.vue` - 活动轮播
- ✅ `Calendar.vue` - 日历视图
- ✅ `Admin.vue` - 管理面板（已正确实现）

**详细说明**：参见 [IMAGE_URL_FIX.md](./IMAGE_URL_FIX.md)

---

### 5. 🧪 测试数据创建

**测试活动**：

#### 活动1：校园音乐节
- **日期**：2025-11-07
- **时间**：19:00 - 21:30
- **地点**：学校体育场
- **主办**：学生会文艺部
- **人数**：500人
- **图片**：https://haowallpaper.com/link/common/file/getCroppingImg/17873560258071936

#### 活动2：科技创新大赛
- **日期**：2025-11-10
- **时间**：14:00 - 17:00
- **地点**：图书馆报告厅
- **主办**：科技协会
- **人数**：200人
- **图片**：https://haowallpaper.com/link/common/file/getCroppingImg/15789130517090624

---

## 📂 所有修改的文件清单

### 后端文件
```
backend/
├── models.py                          # Event模型新增字段
├── resources/events.py                # 新增upcoming API，添加验证
├── app.py                             # 注册新API端点
└── migrations/add_event_fields.py     # 数据库迁移脚本
```

### 前端文件
```
frontend/
├── src/
│   ├── components/
│   │   └── EventCarousel.vue          # 新建：活动轮播组件
│   ├── views/
│   │   ├── Home.vue                   # 集成轮播组件
│   │   ├── Admin.vue                  # 新增在线URL输入
│   │   └── Calendar.vue               # 修复图片URL解析
│   └── api/
│       └── events.js                  # 新增getUpcomingEvents接口
└── vite.config.js                     # 修复IPv4/IPv6配置
```

### 配置文件
```
frontend/vite.config.js                # 代理配置优化
```

### 文档文件
```
├── CAROUSEL_USAGE_GUIDE.md            # 轮播功能使用指南
├── ONLINE_IMAGE_URL_GUIDE.md          # 在线图片URL使用指南
├── IMAGE_URL_FIX.md                   # 图片URL解析修复说明
└── RECENT_UPDATES_SUMMARY.md          # 本文档
```

---

## 🚀 如何使用新功能

### 查看活动轮播
1. 访问主页：http://localhost:3000
2. 轮播会自动显示近期有海报的活动
3. 可以点击左右箭头手动切换

### 创建带在线图片的活动
1. 登录管理员账户
2. 进入管理面板
3. 点击"创建日程"
4. 填写必填信息：
   - 标题、日期、时间
   - **举办部门**（必填）
   - **活动地点**（必填）
   - 预计参与人数（可选）
5. 上传活动海报（二选一）：
   - 点击上传按钮选择本地文件
   - 在输入框粘贴在线图片URL
6. 保存

### 查看日历中的活动
1. 访问日历页面
2. 有活动的日期会显示背景图
3. 点击日期查看活动列表
4. 点击活动查看详情

---

## 🐛 已修复的问题

### 1. Pillow依赖问题
- **问题**：Windows环境下Pillow 10.1.0编译失败
- **解决**：从requirements.txt移除（项目未实际使用）

### 2. 前端代理连接失败
- **问题**：`ECONNREFUSED ::1:5002`
- **解决**：配置明确使用IPv4 (`127.0.0.1`)

### 3. API 500错误
- **问题**：前端通过代理访问API返回500
- **解决**：修复vite.config.js代理配置，统一IPv4地址

### 4. Axios响应解析错误
- **问题**：`Cannot read properties of undefined (reading 'events')`
- **解决**：Axios拦截器已解包，直接使用`response.events`

### 5. 在线图片URL无法显示
- **问题**：在线图片URL被错误处理
- **解决**：统一图片URL处理逻辑，正确区分在线URL和本地路径

---

## 📊 数据库变更

### events表新增字段
```sql
ALTER TABLE events ADD COLUMN organizer_department VARCHAR(100) DEFAULT NULL;
ALTER TABLE events ADD COLUMN expected_participants INT DEFAULT NULL;
ALTER TABLE events ADD COLUMN location VARCHAR(200) DEFAULT NULL;
```

**迁移状态**：✅ 已成功执行

---

## 🔍 测试检查清单

- [x] 后端API `/api/events/upcoming` 正常返回
- [x] 前端轮播组件正常加载和显示
- [x] 在线图片URL在轮播中正常显示
- [x] 在线图片URL在日历中正常显示
- [x] 在线图片URL在详情弹窗中正常显示
- [x] 管理面板可以创建带在线图片的活动
- [x] 管理面板可以预览在线图片
- [x] 表单验证正确（必填字段检查）
- [x] 数据库迁移成功
- [x] 无linter错误
- [x] 前后端代理正常工作

---

## 📖 相关文档

- [活动轮播使用指南](./CAROUSEL_USAGE_GUIDE.md)
- [在线图片URL使用指南](./ONLINE_IMAGE_URL_GUIDE.md)
- [图片URL解析修复说明](./IMAGE_URL_FIX.md)

---

## 🎉 总结

本次更新成功实现了：
1. ✅ 主页活动轮播展示
2. ✅ 活动信息字段扩展
3. ✅ 在线图片URL支持
4. ✅ 图片URL解析统一
5. ✅ 测试数据创建

所有功能已经过测试，可以正常使用。前端和后端都已启动，可以访问 http://localhost:3000 查看效果！


