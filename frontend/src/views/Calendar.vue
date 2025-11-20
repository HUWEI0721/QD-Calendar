<template>
  <div class="calendar-container">
    <header class="calendar-header">
      <div class="header-content">
        <h1 class="logo" @click="goToHome">
          <img src="/qd-logo.png" alt="QD Logo" class="logo-image" />
          QD日历
        </h1>
        <div class="header-actions">
          <el-button v-if="authStore.isAuthenticated" @click="goToAnalytics">
            <el-icon><DataAnalysis /></el-icon>
            数据分析
          </el-button>
          <el-button v-if="authStore.isAdmin" @click="goToMembers">
            <el-icon><UserFilled /></el-icon>
            人员管理
          </el-button>
          <el-button v-if="authStore.isAdmin" type="primary" @click="goToAdmin">
            <el-icon><Setting /></el-icon>
            管理
          </el-button>
          <el-button v-if="!authStore.isAuthenticated" @click="goToLogin">
            登录
          </el-button>
          <el-dropdown v-else>
            <el-button>
              {{ authStore.user?.username }}
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>
    
    <main class="calendar-main">
      <div class="calendar-wrapper">
        <div class="calendar-controls">
          <el-button-group>
            <el-button @click="previousMonth">
              <el-icon><ArrowLeft /></el-icon>
            </el-button>
            <el-button @click="goToToday">今天</el-button>
            <el-button @click="nextMonth">
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </el-button-group>
          
          <h2 class="current-month">
            {{ currentYear }}年 {{ currentMonth }}月
          </h2>
          
          <div class="filter-controls">
            <el-select
              v-model="statusFilter"
              placeholder="状态筛选"
              clearable
              @change="loadCalendarData"
            >
              <el-option label="待处理" value="pending" />
              <el-option label="进行中" value="in_progress" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
            
            <el-select
              v-model="priorityFilter"
              placeholder="优先级筛选"
              clearable
              @change="loadCalendarData"
            >
              <el-option label="高" value="high" />
              <el-option label="中" value="medium" />
              <el-option label="低" value="low" />
            </el-select>
          </div>
        </div>
        
        <div class="calendar-view" v-loading="eventsStore.loading">
          <div class="weekdays">
            <div class="weekday" v-for="day in weekdays" :key="day">
              {{ day }}
            </div>
          </div>
          
          <div class="calendar-grid">
            <div
              v-for="day in calendarDays"
              :key="day.date"
              class="calendar-day"
              :class="{
                'other-month': day.isOtherMonth,
                'today': day.isToday,
                'has-events': day.events.length > 0,
                'has-background': getDayBackgroundImage(day),
                'is-hovered': hoveredDay === day.date
              }"
              :style="getDayBackgroundStyle(day)"
              @click="handleDayClick(day)"
              @mouseenter="hoveredDay = day.date"
              @mouseleave="handleMouseLeave"
            >
              <!-- 背景遮罩层，让文字更清晰 -->
              <div class="day-overlay" v-if="getDayBackgroundImage(day)"></div>
              
              <div class="day-content">
                <div class="day-header">
                  <span class="day-number">{{ day.day }}</span>
                  <span v-if="day.events.length > 0" class="event-count">
                    {{ day.events.length }}
                  </span>
                </div>
                
                <!-- 事项状态统计（底部显示） -->
                <div class="day-footer" v-if="day.events.length > 0">
                  <div class="status-summary">
                    <span 
                      v-if="getStatusCount(day, 'pending') > 0" 
                      class="status-item status-pending"
                    >
                      <span class="status-dot"></span>
                      {{ getStatusCount(day, 'pending') }}待完成
                    </span>
                    <span 
                      v-if="getStatusCount(day, 'in_progress') > 0" 
                      class="status-item status-in-progress"
                    >
                      <span class="status-dot"></span>
                      {{ getStatusCount(day, 'in_progress') }}进行中
                    </span>
                    <span 
                      v-if="getStatusCount(day, 'completed') > 0" 
                      class="status-item status-completed"
                    >
                      <span class="status-dot"></span>
                      {{ getStatusCount(day, 'completed') }}已完成
                    </span>
                  </div>
                </div>
              </div>
              
              <!-- 悬浮待办事项列表 -->
              <transition name="slide-fade">
                <div 
                  v-if="hoveredDay === day.date && day.events.length > 0"
                  class="day-hover-list"
                  @click.stop
                >
                  <div class="hover-list-header">
                    <span class="hover-list-date">{{ day.fullDate }}</span>
                    <span class="hover-list-count">共 {{ day.events.length }} 项</span>
                  </div>
                  <div class="hover-list-items">
                    <div
                      v-for="event in day.events"
                      :key="event.id"
                      class="hover-event-item"
                      :class="[`priority-${event.priority}`, `status-${event.status}`]"
                      @click="showEventDetail(event)"
                    >
                      <div class="hover-event-header">
                        <span class="hover-event-time" v-if="event.start_time">
                          {{ formatTime(event.start_time) }}
                        </span>
                        <el-tag 
                          :type="getStatusType(event.status)" 
                          size="small"
                          effect="plain"
                        >
                          {{ getStatusLabel(event.status) }}
                        </el-tag>
                      </div>
                      <div class="hover-event-title">{{ event.title }}</div>
                      <div class="hover-event-priority">
                        <el-tag 
                          :type="getPriorityType(event.priority)" 
                          size="small"
                        >
                          {{ getPriorityLabel(event.priority) }}
                        </el-tag>
                      </div>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- 日程列表弹窗 -->
    <el-dialog
      v-model="dayEventsVisible"
      :title="`${selectedDay?.fullDate} 的日程`"
      width="600px"
    >
      <div class="events-list">
        <el-empty v-if="selectedDay?.events.length === 0" description="当天没有日程" />
        <div
          v-for="event in selectedDay?.events"
          :key="event.id"
          class="event-card"
          @click="showEventDetail(event)"
        >
          <div class="event-card-header">
            <h4>{{ event.title }}</h4>
            <el-tag :type="getPriorityType(event.priority)" size="small">
              {{ getPriorityLabel(event.priority) }}
            </el-tag>
          </div>
          <div class="event-card-body">
            <p v-if="event.start_time">
              <el-icon><Clock /></el-icon>
              {{ event.start_time }} - {{ event.end_time || '未设置' }}
            </p>
            <el-tag :type="getStatusType(event.status)" size="small">
              {{ getStatusLabel(event.status) }}
            </el-tag>
          </div>
        </div>
      </div>
    </el-dialog>
    
    <!-- 日程详情弹窗 -->
    <el-dialog
      v-model="eventDetailVisible"
      title="日程详情"
      width="700px"
    >
      <div v-if="selectedEvent" class="event-detail">
        <div v-if="selectedEvent.background_image" class="event-image">
          <img 
            :src="getFullImageUrl(selectedEvent.background_image)" 
            :alt="selectedEvent.title"
            @error="handleImageError"
          />
        </div>
        
        <div class="event-info">
          <h2>{{ selectedEvent.title }}</h2>
          
          <div class="info-row">
            <el-icon><Calendar /></el-icon>
            <span>{{ selectedEvent.event_date }}</span>
          </div>
          
          <div class="info-row" v-if="selectedEvent.start_time">
            <el-icon><Clock /></el-icon>
            <span>{{ selectedEvent.start_time }} - {{ selectedEvent.end_time || '未设置' }}</span>
          </div>
          
          <div class="info-row">
            <el-icon><Flag /></el-icon>
            <el-tag :type="getPriorityType(selectedEvent.priority)">
              {{ getPriorityLabel(selectedEvent.priority) }}
            </el-tag>
          </div>
          
          <div class="info-row">
            <el-icon><Document /></el-icon>
            <el-tag :type="getStatusType(selectedEvent.status)">
              {{ getStatusLabel(selectedEvent.status) }}
            </el-tag>
          </div>
          
          <div class="info-row" v-if="selectedEvent.location">
            <el-icon><Location /></el-icon>
            <span>地点: {{ selectedEvent.location }}</span>
          </div>
          
          <div class="info-row" v-if="selectedEvent.organizer_department">
            <el-icon><OfficeBuilding /></el-icon>
            <span>举办部门: {{ selectedEvent.organizer_department }}</span>
          </div>
          
          <div class="info-row" v-if="selectedEvent.expected_participants">
            <el-icon><User /></el-icon>
            <span>预计人数: {{ selectedEvent.expected_participants }} 人</span>
          </div>
          
          <div class="info-row" v-if="selectedEvent.creator_name">
            <el-icon><User /></el-icon>
            <span>创建者: {{ selectedEvent.creator_name }}</span>
          </div>
          
          <div class="event-description" v-if="selectedEvent.description">
            <h4>描述</h4>
            <p>{{ selectedEvent.description }}</p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useEventsStore } from '@/stores/events'
import { getEvents } from '@/api/events'
import dayjs from 'dayjs'
import {
  Calendar, Setting, ArrowDown, ArrowLeft, ArrowRight,
  Clock, Flag, Document, User, DataAnalysis, UserFilled,
  Location, OfficeBuilding
} from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()
const eventsStore = useEventsStore()

const currentYear = ref(new Date().getFullYear())
const currentMonth = ref(new Date().getMonth() + 1)
const statusFilter = ref('')
const priorityFilter = ref('')
const allEvents = ref([])

const dayEventsVisible = ref(false)
const eventDetailVisible = ref(false)
const selectedDay = ref(null)
const selectedEvent = ref(null)
const hoveredDay = ref(null)

const weekdays = ['日', '一', '二', '三', '四', '五', '六']

// 计算日历天数
const calendarDays = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value
  
  // 当月第一天
  const firstDay = new Date(year, month - 1, 1)
  const firstDayWeek = firstDay.getDay()
  
  // 当月最后一天
  const lastDay = new Date(year, month, 0)
  const lastDate = lastDay.getDate()
  
  // 上个月最后几天
  const prevMonthLastDay = new Date(year, month - 1, 0)
  const prevMonthLastDate = prevMonthLastDay.getDate()
  
  const days = []
  
  // 填充上个月的日期
  for (let i = firstDayWeek - 1; i >= 0; i--) {
    const day = prevMonthLastDate - i
    const date = new Date(year, month - 2, day)
    days.push(createDayObject(date, true))
  }
  
  // 填充当月的日期
  for (let i = 1; i <= lastDate; i++) {
    const date = new Date(year, month - 1, i)
    days.push(createDayObject(date, false))
  }
  
  // 填充下个月的日期
  const remainingDays = 42 - days.length
  for (let i = 1; i <= remainingDays; i++) {
    const date = new Date(year, month, i)
    days.push(createDayObject(date, true))
  }
  
  return days
})

function createDayObject(date, isOtherMonth) {
  const dateStr = dayjs(date).format('YYYY-MM-DD')
  const today = dayjs().format('YYYY-MM-DD')
  
  // 获取该日期的事件
  const dayEvents = allEvents.value.filter(event => event.event_date === dateStr)
  
  return {
    date: dateStr,
    fullDate: dayjs(date).format('YYYY年M月D日'),
    day: date.getDate(),
    isOtherMonth,
    isToday: dateStr === today,
    events: dayEvents
  }
}

// 加载日历数据
async function loadCalendarData() {
  try {
    const params = {
      start_date: `${currentYear.value}-${String(currentMonth.value).padStart(2, '0')}-01`,
      end_date: dayjs(`${currentYear.value}-${currentMonth.value}-01`).endOf('month').format('YYYY-MM-DD')
    }
    
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    
    if (priorityFilter.value) {
      params.priority = priorityFilter.value
    }
    
    const response = await getEvents(params)
    allEvents.value = response.events || []
  } catch (error) {
    ElMessage.error('加载日历数据失败')
  }
}

function previousMonth() {
  if (currentMonth.value === 1) {
    currentMonth.value = 12
    currentYear.value--
  } else {
    currentMonth.value--
  }
  loadCalendarData()
}

function nextMonth() {
  if (currentMonth.value === 12) {
    currentMonth.value = 1
    currentYear.value++
  } else {
    currentMonth.value++
  }
  loadCalendarData()
}

function goToToday() {
  const today = new Date()
  currentYear.value = today.getFullYear()
  currentMonth.value = today.getMonth() + 1
  loadCalendarData()
}

function handleDayClick(day) {
  selectedDay.value = day
  dayEventsVisible.value = true
}

function showEventDetail(event) {
  selectedEvent.value = event
  eventDetailVisible.value = true
  dayEventsVisible.value = false
}

function getPriorityType(priority) {
  const types = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  }
  return types[priority] || 'info'
}

function getPriorityLabel(priority) {
  const labels = {
    high: '高优先级',
    medium: '中优先级',
    low: '低优先级'
  }
  return labels[priority] || priority
}

function getStatusType(status) {
  const types = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

function getStatusLabel(status) {
  const labels = {
    pending: '待处理',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return labels[status] || status
}

// 获取当天的背景图片（优先级：高 > 中 > 低，有图片的优先）
function getDayBackgroundImage(day) {
  if (!day.events || day.events.length === 0) {
    return null
  }
  
  // 找到所有带图片的事件
  const eventsWithImage = day.events.filter(event => event.background_image)
  
  if (eventsWithImage.length === 0) {
    return null
  }
  
  // 按优先级排序：high > medium > low
  const priorityOrder = { high: 3, medium: 2, low: 1 }
  const sortedEvents = eventsWithImage.sort((a, b) => {
    return (priorityOrder[b.priority] || 0) - (priorityOrder[a.priority] || 0)
  })
  
  // 返回优先级最高的事件的背景图片
  return sortedEvents[0].background_image
}

// 获取图片完整URL
function getFullImageUrl(url) {
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

// 生成背景样式
function getDayBackgroundStyle(day) {
  const bgImage = getDayBackgroundImage(day)
  if (!bgImage) {
    return {}
  }
  
  return {
    backgroundImage: `url(${getFullImageUrl(bgImage)})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat'
  }
}

// 获取某个状态的事项数量
function getStatusCount(day, status) {
  if (!day.events || day.events.length === 0) {
    return 0
  }
  return day.events.filter(event => event.status === status).length
}

// 格式化时间（显示为 HH:MM）
function formatTime(timeStr) {
  if (!timeStr) return ''
  return timeStr.substring(0, 5)
}

// 鼠标离开日期单元格
function handleMouseLeave(event) {
  // 检查鼠标是否移动到悬浮列表上
  const relatedTarget = event.relatedTarget
  if (relatedTarget && relatedTarget.closest('.day-hover-list')) {
    return // 如果移动到悬浮列表上，不隐藏
  }
  hoveredDay.value = null
}

// 图片加载错误处理
function handleImageError(event) {
  console.error('图片加载失败:', event.target.src)
  event.target.style.display = 'none'
}

function goToHome() {
  router.push('/')
}

function goToLogin() {
  router.push('/login')
}

function goToAdmin() {
  router.push('/admin')
}

function goToMembers() {
  router.push('/members')
}

function goToAnalytics() {
  router.push('/analytics')
}

function handleLogout() {
  authStore.logout()
  ElMessage.success('已退出登录')
}

onMounted(() => {
  loadCalendarData()
})
</script>

<style scoped>
.calendar-container {
  min-height: 100vh;
  background: var(--bg-color);
}

.calendar-header {
  background: white;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  cursor: pointer;
}

.logo-image {
  width: 36px;
  height: 36px;
  object-fit: contain;
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.calendar-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.calendar-wrapper {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.calendar-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.current-month {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.filter-controls {
  display: flex;
  gap: 10px;
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background: var(--border-color);
  border: 1px solid var(--border-color);
  border-radius: 10px 10px 0 0;
  overflow: hidden;
}

.weekday {
  background: var(--bg-color);
  padding: 15px;
  text-align: center;
  font-weight: 600;
  color: var(--text-secondary);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background: var(--border-color);
  border: 1px solid var(--border-color);
  border-top: none;
  border-radius: 0 0 10px 10px;
  overflow: hidden;
}

.calendar-day {
  position: relative;
  background: white;
  min-height: 120px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.3s;
  overflow: hidden;
}

.calendar-day:hover {
  transform: scale(1.02);
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 悬停时背景图片放大效果 */
.calendar-day.has-background {
  transition: all 0.3s ease;
}

.calendar-day.has-background.is-hovered {
  background-size: 110%; /* 背景放大 */
}

/* 有背景图片的日期 */
.calendar-day.has-background {
  color: white;
}

.calendar-day.has-background .day-number,
.calendar-day.has-background .event-title,
.calendar-day.has-background .event-time {
  color: white;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8);
}

/* 背景遮罩层 */
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

/* 内容容器（确保在背景图和遮罩层之上） */
.day-content {
  position: relative;
  z-index: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.calendar-day.other-month {
  opacity: 0.4;
}

.calendar-day.today {
  box-shadow: inset 0 0 0 2px var(--primary-color);
}

.calendar-day.has-events {
  border-left: 3px solid var(--primary-color);
}

.calendar-day.has-background.has-events {
  border-left: 3px solid rgba(255, 255, 255, 0.8);
}

.day-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.day-number {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.event-count {
  background: var(--primary-color);
  color: white;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 12px;
}

.calendar-day.has-background .event-count {
  background: rgba(255, 255, 255, 0.9);
  color: var(--primary-color);
}

/* 日期底部统计 */
.day-footer {
  position: absolute;
  bottom: 5px;
  left: 8px;
  right: 8px;
  z-index: 1;
}

.status-summary {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  font-size: 11px;
  line-height: 1.2;
}

.status-item {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  white-space: nowrap;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: inline-block;
  flex-shrink: 0;
}

.status-pending .status-dot {
  background-color: #909399; /* 灰色 - 待完成 */
}

.status-in-progress .status-dot {
  background-color: #e6a23c; /* 橙色 - 进行中 */
}

.status-completed .status-dot {
  background-color: #67c23a; /* 绿色 - 已完成 */
}

/* 有背景的情况下，文字颜色调整 */
.calendar-day.has-background .status-item {
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
}

/* 无背景的情况下，文字颜色 */
.calendar-day:not(.has-background) .status-item {
  color: var(--text-secondary);
}

/* 悬浮待办事项列表 */
.day-hover-list {
  position: absolute;
  top: 0;
  left: 100%;
  margin-left: 10px;
  width: 280px;
  max-height: 400px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  z-index: 100;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* 如果右侧空间不够，显示在左边 */
.calendar-day:nth-child(7n) .day-hover-list,
.calendar-day:nth-child(7n + 6) .day-hover-list {
  left: auto;
  right: 100%;
  margin-left: 0;
  margin-right: 10px;
}

.hover-list-header {
  padding: 12px 15px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hover-list-date {
  font-size: 14px;
  font-weight: 600;
}

.hover-list-count {
  font-size: 12px;
  opacity: 0.9;
}

.hover-list-items {
  overflow-y: auto;
  max-height: 350px;
  padding: 8px;
}

.hover-event-item {
  padding: 10px;
  margin-bottom: 8px;
  background: var(--bg-color);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.hover-event-item:hover {
  background: #f0f2f5;
  transform: translateX(3px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.hover-event-item:last-child {
  margin-bottom: 0;
}

.hover-event-item.priority-high {
  border-left-color: #f56c6c;
}

.hover-event-item.priority-medium {
  border-left-color: #e6a23c;
}

.hover-event-item.priority-low {
  border-left-color: #909399;
}

.hover-event-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.hover-event-time {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 500;
}

.hover-event-title {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 500;
  margin-bottom: 6px;
  line-height: 1.4;
}

.hover-event-priority {
  display: flex;
  align-items: center;
}

/* 过渡动画 */
.slide-fade-enter-active {
  transition: all 0.3s ease;
}

.slide-fade-leave-active {
  transition: all 0.2s ease;
}

.slide-fade-enter-from {
  transform: translateX(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateX(-10px);
  opacity: 0;
}

.day-events {
  position: relative;
  z-index: 1;
}

.event-item {
  background: white;
  border-radius: 5px;
  padding: 4px 8px;
  margin-bottom: 4px;
  font-size: 12px;
  border-left: 3px solid;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  gap: 5px;
  align-items: center;
}

.event-item:hover {
  transform: translateX(5px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.event-item.priority-high {
  border-left-color: var(--danger-color);
}

.event-item.priority-medium {
  border-left-color: var(--warning-color);
}

.event-item.priority-low {
  border-left-color: var(--info-color);
}

.event-time {
  color: var(--text-secondary);
  font-size: 11px;
}

.event-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.more-events {
  text-align: center;
  color: var(--text-secondary);
  font-size: 12px;
  padding: 2px;
}

.events-list {
  max-height: 500px;
  overflow-y: auto;
}

.event-card {
  padding: 15px;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.event-card:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.event-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.event-card-header h4 {
  margin: 0;
  font-size: 16px;
}

.event-card-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-secondary);
  font-size: 14px;
}

.event-card-body p {
  display: flex;
  align-items: center;
  gap: 5px;
  margin: 0;
}

.event-detail {
  animation: fadeIn 0.3s;
}

.event-image {
  width: 100%;
  height: 200px;
  border-radius: 10px;
  margin-bottom: 20px;
  overflow: hidden;
}

.event-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.event-info h2 {
  margin-bottom: 20px;
  color: var(--text-primary);
}

.info-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  color: var(--text-regular);
}

.event-description {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.event-description h4 {
  margin-bottom: 10px;
  color: var(--text-primary);
}

.event-description p {
  color: var(--text-regular);
  line-height: 1.6;
  white-space: pre-wrap;
}

@media (max-width: 768px) {
  .calendar-controls {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .calendar-day {
    min-height: 80px;
  }
  
  .event-item {
    font-size: 10px;
  }
}
</style>

