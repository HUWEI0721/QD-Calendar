<template>
  <div class="event-carousel">
    <div class="carousel-header">
      <h2>
        <el-icon><Promotion /></el-icon>
        近期活动预告
      </h2>
      <div class="date-range">{{ dateRange }}</div>
    </div>

    <div v-if="loading" class="loading-container">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>加载中...</span>
    </div>

    <div v-else-if="events.length === 0" class="empty-container">
      <el-icon><Calendar /></el-icon>
      <p>近期暂无活动安排</p>
    </div>

    <el-carousel
      v-else
      :interval="3000"
      type="card"
      height="400px"
      :autoplay="true"
      arrow="always"
      class="event-carousel-slider"
    >
      <el-carousel-item v-for="event in events" :key="event.id">
        <div class="event-card" @click="viewEventDetail(event)">
          <!-- 背景图片 -->
          <div class="event-poster">
            <img 
              v-if="event.background_image" 
              :src="getImageUrl(event.background_image)" 
              :alt="event.title"
              class="poster-image"
              @error="handleImageError"
            />
            <div v-else class="no-image">
              <el-icon><Picture /></el-icon>
              <span>暂无海报</span>
            </div>
            <!-- 优先级标签 -->
            <div class="priority-badge" :class="`priority-${event.priority}`">
              {{ getPriorityLabel(event.priority) }}
            </div>
            <!-- 状态标签 -->
            <div class="status-badge" :class="`status-${event.status}`">
              {{ getStatusLabel(event.status) }}
            </div>
          </div>

          <!-- 活动信息 -->
          <div class="event-info">
            <h3 class="event-title">{{ event.title }}</h3>
            
            <div class="event-details">
              <!-- 时间 -->
              <div class="detail-item">
                <el-icon><Clock /></el-icon>
                <span>{{ formatEventTime(event) }}</span>
              </div>

              <!-- 地点 -->
              <div v-if="event.location" class="detail-item">
                <el-icon><Location /></el-icon>
                <span>{{ event.location }}</span>
              </div>

              <!-- 举办部门 -->
              <div v-if="event.organizer_department" class="detail-item">
                <el-icon><OfficeBuilding /></el-icon>
                <span>{{ event.organizer_department }}</span>
              </div>

              <!-- 参与人数 -->
              <div v-if="event.expected_participants" class="detail-item">
                <el-icon><User /></el-icon>
                <span>预计 {{ event.expected_participants }} 人参与</span>
              </div>
            </div>

            <!-- 描述 -->
            <div v-if="event.description" class="event-description">
              {{ event.description }}
            </div>
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getUpcomingEvents } from '@/api/events'
import { ElMessage } from 'element-plus'
import { 
  Calendar, 
  Clock, 
  Location, 
  OfficeBuilding, 
  User, 
  Picture, 
  Loading, 
  Promotion 
} from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const events = ref([])
const loading = ref(false)

// 日期范围显示
const dateRange = computed(() => {
  if (events.value.length === 0) return ''
  const today = dayjs()
  const nextWeek = today.add(7, 'day')
  return `${today.format('YYYY-MM-DD')} 至 ${nextWeek.format('YYYY-MM-DD')}`
})

// 获取图片完整URL
const getImageUrl = (url) => {
  if (!url) return ''
  // 如果是在线URL（http或https开头），直接返回
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  // 如果是相对路径，加上后端地址
  if (url.startsWith('/')) {
    return `http://localhost:5002${url}`
  }
  // 其他情况（如 uploads/xxx.jpg），也加上后端地址
  return `http://localhost:5002/${url}`
}

// 格式化活动时间
const formatEventTime = (event) => {
  let timeStr = dayjs(event.event_date).format('YYYY年MM月DD日')
  
  if (event.start_time) {
    const startTime = event.start_time.substring(0, 5) // HH:MM
    timeStr += ` ${startTime}`
    
    if (event.end_time) {
      const endTime = event.end_time.substring(0, 5)
      timeStr += `-${endTime}`
    }
  }
  
  return timeStr
}

// 获取优先级标签
const getPriorityLabel = (priority) => {
  const labels = {
    high: '高优先级',
    medium: '中优先级',
    low: '低优先级'
  }
  return labels[priority] || priority
}

// 获取状态标签
const getStatusLabel = (status) => {
  const labels = {
    pending: '待开始',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return labels[status] || status
}

// 查看活动详情
const viewEventDetail = (event) => {
  ElMessage.info(`活动详情：${event.title}`)
  // 可以在这里添加跳转到详情页或显示详情弹窗的逻辑
}

// 图片加载错误处理
const handleImageError = (event) => {
  console.error('图片加载失败:', event.target.src)
  event.target.style.display = 'none'
  // 可以设置默认图片
  // event.target.src = '/path/to/default-image.jpg'
}

// 加载近期活动
const loadUpcomingEvents = async () => {
  loading.value = true
  try {
    const response = await getUpcomingEvents()
    // axios拦截器已经返回了response.data，所以这里直接使用response
    // 只显示有背景图片的活动
    const allEvents = response.events || []
    events.value = allEvents.filter(event => event.background_image)
    
    if (allEvents.length > 0 && events.value.length === 0) {
      console.warn('近期有活动但都没有上传海报图片')
    }
  } catch (error) {
    console.error('加载近期活动失败:', error)
    ElMessage.error('加载活动失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUpcomingEvents()
})
</script>

<style scoped>
.event-carousel {
  width: 100%;
  padding: 30px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.carousel-header {
  text-align: center;
  margin-bottom: 30px;
  color: white;
}

.carousel-header h2 {
  font-size: 28px;
  font-weight: bold;
  margin: 0 0 10px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.carousel-header h2 .el-icon {
  font-size: 32px;
}

.date-range {
  font-size: 14px;
  opacity: 0.9;
}

.loading-container,
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: white;
  font-size: 16px;
  gap: 10px;
}

.loading-container .el-icon,
.empty-container .el-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.event-carousel-slider {
  margin: 0 auto;
  max-width: 1200px;
}

.event-card {
  height: 100%;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.event-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.event-poster {
  width: 100%;
  height: 200px;
  background-color: #f5f5f5;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.poster-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.no-image {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #999;
}

.no-image .el-icon {
  font-size: 48px;
}

.priority-badge,
.status-badge {
  position: absolute;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  color: white;
  backdrop-filter: blur(4px);
}

.priority-badge {
  top: 10px;
  left: 10px;
}

.priority-high {
  background: rgba(255, 59, 48, 0.9);
}

.priority-medium {
  background: rgba(255, 149, 0, 0.9);
}

.priority-low {
  background: rgba(142, 142, 147, 0.9);
}

.status-badge {
  top: 10px;
  right: 10px;
}

.status-pending {
  background: rgba(0, 122, 255, 0.9);
}

.status-in_progress {
  background: rgba(52, 199, 89, 0.9);
}

.status-completed {
  background: rgba(88, 86, 214, 0.9);
}

.status-cancelled {
  background: rgba(255, 59, 48, 0.9);
}

.event-info {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.event-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.event-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.detail-item .el-icon {
  font-size: 16px;
  color: #409EFF;
}

.event-description {
  font-size: 13px;
  color: #999;
  line-height: 1.5;
  max-height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* 轮播指示器样式 */
:deep(.el-carousel__indicator) {
  background-color: rgba(255, 255, 255, 0.3);
}

:deep(.el-carousel__indicator.is-active) {
  background-color: white;
}

/* 轮播箭头样式 */
:deep(.el-carousel__arrow) {
  background-color: rgba(255, 255, 255, 0.8);
  color: #667eea;
}

:deep(.el-carousel__arrow:hover) {
  background-color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .event-carousel {
    padding: 20px 10px;
  }

  .carousel-header h2 {
    font-size: 22px;
  }

  .event-carousel-slider {
    height: 350px !important;
  }

  .event-poster {
    height: 150px;
  }

  .event-title {
    font-size: 16px;
  }
}
</style>

