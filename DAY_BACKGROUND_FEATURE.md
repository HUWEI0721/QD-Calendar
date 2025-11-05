# 日历日期背景图功能

## 📋 功能说明

当日历中某一天有带背景图片的日程时，该日期单元格会自动显示该图片作为背景。

## 🎯 功能特性

### 1. 智能选择
- ✅ 如果某天有多个带图片的日程，自动选择**优先级最高**的日程图片
- ✅ 优先级排序：**高 > 中 > 低**
- ✅ 如果某天所有日程都没有图片，则不显示背景

### 2. 视觉效果
- ✅ 背景图片全覆盖日期单元格
- ✅ 添加半透明遮罩层，确保文字清晰可读
- ✅ 文字带阴影效果，增强对比度
- ✅ 事件计数徽章变为白色背景，更醒目
- ✅ 悬停时有缩放和阴影效果

### 3. 自适应
- ✅ 背景图片自动适配单元格大小（cover）
- ✅ 居中显示，保持图片最佳展示效果
- ✅ 不会影响其他功能（点击、筛选等）

## 🔧 实现逻辑

### 核心函数

#### 1. getDayBackgroundImage(day)
获取某天应该显示的背景图片 URL

```javascript
function getDayBackgroundImage(day) {
  // 1. 检查是否有事件
  if (!day.events || day.events.length === 0) {
    return null
  }
  
  // 2. 筛选出所有带图片的事件
  const eventsWithImage = day.events.filter(event => event.background_image)
  
  if (eventsWithImage.length === 0) {
    return null
  }
  
  // 3. 按优先级排序（高 > 中 > 低）
  const priorityOrder = { high: 3, medium: 2, low: 1 }
  const sortedEvents = eventsWithImage.sort((a, b) => {
    return (priorityOrder[b.priority] || 0) - (priorityOrder[a.priority] || 0)
  })
  
  // 4. 返回优先级最高的事件的背景图片
  return sortedEvents[0].background_image
}
```

#### 2. getDayBackgroundStyle(day)
生成背景样式对象

```javascript
function getDayBackgroundStyle(day) {
  const bgImage = getDayBackgroundImage(day)
  if (!bgImage) {
    return {}
  }
  
  return {
    backgroundImage: `url(${bgImage})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat'
  }
}
```

### 模板使用

```vue
<div
  class="calendar-day"
  :class="{
    'has-background': getDayBackgroundImage(day)
  }"
  :style="getDayBackgroundStyle(day)"
>
  <!-- 背景遮罩层 -->
  <div class="day-overlay" v-if="getDayBackgroundImage(day)"></div>
  
  <!-- 内容容器 -->
  <div class="day-content">
    <!-- 日期、事件列表等 -->
  </div>
</div>
```

## 🎨 样式设计

### 背景图片样式
```css
.calendar-day {
  position: relative;
  background: white;
  overflow: hidden;
}

/* 应用背景图片（通过内联样式） */
/* background-image, background-size, background-position */
```

### 遮罩层样式
```css
.day-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.3) 0%,
    rgba(0, 0, 0, 0.5) 100%
  );
  z-index: 0;
  pointer-events: none;
}
```

### 文字样式增强
```css
.calendar-day.has-background .day-number,
.calendar-day.has-background .event-title,
.calendar-day.has-background .event-time {
  color: white;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8);
}

.calendar-day.has-background .event-count {
  background: rgba(255, 255, 255, 0.9);
  color: var(--primary-color);
}
```

### 层级结构
```
calendar-day (z-index: auto)
  ├── 背景图片 (通过 background-image)
  ├── day-overlay (z-index: 0) - 遮罩层
  └── day-content (z-index: 1) - 内容层
      ├── day-header - 日期和计数
      └── day-events - 事件列表
```

## 📖 使用示例

### 场景1: 单个日程带图片
```javascript
day = {
  date: '2025-10-30',
  events: [
    {
      title: '团队活动',
      priority: 'high',
      background_image: '/uploads/events/2025/10/30/image1.jpg'
    }
  ]
}
// ✅ 显示 image1.jpg 作为背景
```

### 场景2: 多个日程带图片
```javascript
day = {
  date: '2025-10-30',
  events: [
    {
      title: '会议',
      priority: 'medium',
      background_image: '/uploads/events/2025/10/30/image1.jpg'
    },
    {
      title: '重要活动',
      priority: 'high',
      background_image: '/uploads/events/2025/10/30/image2.jpg'
    },
    {
      title: '日常任务',
      priority: 'low',
      background_image: '/uploads/events/2025/10/30/image3.jpg'
    }
  ]
}
// ✅ 显示 image2.jpg（优先级最高的）
```

### 场景3: 部分日程带图片
```javascript
day = {
  date: '2025-10-30',
  events: [
    {
      title: '会议',
      priority: 'high',
      background_image: null  // 没有图片
    },
    {
      title: '活动',
      priority: 'medium',
      background_image: '/uploads/events/2025/10/30/image1.jpg'
    }
  ]
}
// ✅ 显示 image1.jpg（唯一有图片的）
```

### 场景4: 没有日程或都无图片
```javascript
day = {
  date: '2025-10-30',
  events: []
}
// ✅ 不显示背景，使用默认白色
```

## 🎯 优先级规则

### 排序逻辑
```
1. 先筛选出所有带图片的日程
2. 按优先级排序：
   - high (高) = 3
   - medium (中) = 2
   - low (低) = 1
3. 选择分数最高的日程图片
```

### 示例对比
| 日程 | 优先级 | 有图片 | 分数 | 结果 |
|------|--------|--------|------|------|
| 日程A | high | ✅ | 3 | **选中** ✅ |
| 日程B | medium | ✅ | 2 | - |
| 日程C | low | ✅ | 1 | - |
| 日程D | high | ❌ | - | 忽略 |

## 🔍 调试技巧

### 检查背景图片是否加载
打开浏览器开发者工具（F12）：

1. **Elements 标签**
   - 找到 `.calendar-day` 元素
   - 查看 `style` 属性是否有 `background-image: url(...)`

2. **Network 标签**
   - 筛选 Img/Media
   - 查找图片请求状态（应该是 200）

3. **Console 测试**
   ```javascript
   // 测试函数
   const day = calendarDays.value[10] // 某一天
   console.log(getDayBackgroundImage(day))
   console.log(getDayBackgroundStyle(day))
   ```

### 常见问题

#### 问题1: 图片不显示
**排查步骤**:
1. 检查 `event.background_image` 是否有值
2. 检查 URL 格式是否正确（`/uploads/...`）
3. 检查 Vite 代理配置（`/uploads` 路径）
4. 检查浏览器控制台是否有 404 错误

#### 问题2: 文字看不清
**解决方案**:
- 增加遮罩层透明度
- 调整文字阴影强度
- 修改渐变方向

```css
.day-overlay {
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.4) 0%,  /* 增加透明度 */
    rgba(0, 0, 0, 0.7) 100%
  );
}
```

#### 问题3: 背景图片被拉伸
**解决方案**:
- 确保使用 `background-size: cover`
- 检查图片尺寸和比例

## 🎨 自定义配置

### 调整遮罩层透明度
修改 `Calendar.vue` 中的样式：

```css
.day-overlay {
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.2) 0%,  /* 浅色遮罩 */
    rgba(0, 0, 0, 0.4) 100%
  );
}
```

### 修改优先级规则
修改 `getDayBackgroundImage` 函数：

```javascript
// 改为按时间排序（最早的优先）
const sortedEvents = eventsWithImage.sort((a, b) => {
  return a.start_time.localeCompare(b.start_time)
})

// 或随机选择
const randomEvent = eventsWithImage[Math.floor(Math.random() * eventsWithImage.length)]
return randomEvent.background_image
```

### 禁用背景功能
注释掉背景样式绑定：

```vue
<div
  class="calendar-day"
  <!-- :style="getDayBackgroundStyle(day)" -->
>
```

## 📊 性能优化

### 已优化项
- ✅ 使用 `computed` 计算 `calendarDays`，只在数据变化时重新计算
- ✅ `filter` 和 `sort` 只处理单日事件，性能开销小
- ✅ CSS `transform` 用于悬停动画，性能更好
- ✅ 图片使用 `background-image`，浏览器自动优化

### 未来优化
- [ ] 图片懒加载（只加载可见日期的图片）
- [ ] 图片压缩（上传时自动压缩）
- [ ] 缓存背景图片计算结果
- [ ] 虚拟滚动（大范围日期）

## 🎉 完成

功能已完整实现！特性总结：

1. ✅ 自动从当天日程中选择背景图片
2. ✅ 优先级排序（高 > 中 > 低）
3. ✅ 美观的视觉效果（遮罩 + 文字阴影）
4. ✅ 完全响应式和自适应
5. ✅ 不影响原有功能

**使用方法**: 创建日程时上传背景图片，日历视图会自动显示！

---

*更新时间: 2025-10-30*  
*版本: v1.1.0*

