<template>
  <div class="analytics-container">
    <div class="header">
      <h1>数据分析</h1>
      <div class="date-picker">
        <el-date-picker
          v-model="selectedMonth"
          type="month"
          placeholder="选择月份"
          format="YYYY年MM月"
          @change="loadData"
        />
      </div>
    </div>

    <!-- 数据总览卡片 -->
    <div class="overview-cards">
      <el-card class="stat-card">
        <div class="stat-content">
          <el-icon class="stat-icon" color="#409EFF"><Calendar /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ overview.total_events || 0 }}</div>
            <div class="stat-label">总活动数</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <el-icon class="stat-icon" color="#67C23A"><Check /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ overview.completed_events || 0 }}</div>
            <div class="stat-label">已完成活动</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <el-icon class="stat-icon" color="#E6A23C"><TrendCharts /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ overview.completion_rate || 0 }}%</div>
            <div class="stat-label">完成率</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <el-icon class="stat-icon" color="#F56C6C"><User /></el-icon>
          <div class="stat-info">
            <div class="stat-value">{{ overview.unique_participants || 0 }}</div>
            <div class="stat-label">参与人数</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 图表区域 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <!-- 状态分布饼图 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <h3>活动状态分布</h3>
          </template>
          <div ref="statusChartRef" style="width: 100%; height: 300px"></div>
        </el-card>
      </el-col>

      <!-- 优先级分布饼图 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <h3>活动优先级分布</h3>
          </template>
          <div ref="priorityChartRef" style="width: 100%; height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 每日趋势折线图 -->
    <el-row style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <h3>每日活动数量趋势</h3>
          </template>
          <div ref="trendChartRef" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- TOP活动排行 -->
    <el-row style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <h3>参与人数 TOP 5 活动</h3>
          </template>
          <el-table :data="topEvents" style="width: 100%">
            <el-table-column type="index" label="排名" width="80" />
            <el-table-column prop="title" label="活动名称" />
            <el-table-column prop="event_date" label="日期" width="120" />
            <el-table-column prop="participant_count" label="参与人数" width="120">
              <template #default="{ row }">
                <el-tag type="success">{{ row.participant_count }} 人</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="优先级" width="100">
              <template #default="{ row }">
                <el-tag :type="getPriorityType(row.priority)">
                  {{ getPriorityLabel(row.priority) }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 人员参与分析 -->
    <el-row style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <h3>人员参与度 TOP 10</h3>
          </template>
          <el-table :data="topParticipants" style="width: 100%">
            <el-table-column type="index" label="排名" width="80" />
            <el-table-column prop="name" label="姓名" width="120" />
            <el-table-column prop="department" label="部门" width="150" />
            <el-table-column prop="event_count" label="参与活动数" width="120">
              <template #default="{ row }">
                <el-tag type="primary">{{ row.event_count }} 次</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="活跃度">
              <template #default="{ row }">
                <el-progress
                  :percentage="calcActiveRate(row.event_count)"
                  :color="getProgressColor(row.event_count)"
                />
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Calendar, Check, TrendCharts, User } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { getAnalyticsOverview, getAnalyticsEvents, getAnalyticsMembers } from '@/api/analytics'

const selectedMonth = ref(new Date())
const overview = reactive({
  total_events: 0,
  completed_events: 0,
  completion_rate: 0,
  unique_participants: 0,
  total_participants: 0
})

const statusDistribution = ref([])
const priorityDistribution = ref([])
const dailyTrend = ref([])
const topEvents = ref([])
const topParticipants = ref([])

const statusChartRef = ref(null)
const priorityChartRef = ref(null)
const trendChartRef = ref(null)

let statusChart = null
let priorityChart = null
let trendChart = null

// 加载数据
async function loadData() {
  const date = new Date(selectedMonth.value)
  const params = {
    year: date.getFullYear(),
    month: date.getMonth() + 1
  }

  try {
    // 加载总览数据
    const overviewRes = await getAnalyticsOverview(params)
    Object.assign(overview, overviewRes.overview)
    statusDistribution.value = overviewRes.status_distribution || []
    priorityDistribution.value = overviewRes.priority_distribution || []
    dailyTrend.value = overviewRes.daily_trend || []

    // 加载活动分析
    const eventsRes = await getAnalyticsEvents(params)
    topEvents.value = eventsRes.top_events || []

    // 加载人员参与分析
    const membersRes = await getAnalyticsMembers(params)
    topParticipants.value = membersRes.top_participants || []

    // 渲染图表
    await nextTick()
    renderCharts()
  } catch (error) {
    ElMessage.error('加载数据失败')
    console.error(error)
  }
}

// 渲染图表
function renderCharts() {
  renderStatusChart()
  renderPriorityChart()
  renderTrendChart()
}

// 渲染状态分布饼图
function renderStatusChart() {
  if (!statusChartRef.value) return

  if (!statusChart) {
    statusChart = echarts.init(statusChartRef.value)
  }

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      bottom: '0%',
      left: 'center'
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{c}'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: statusDistribution.value.map(item => ({
          name: item.label,
          value: item.count
        }))
      }
    ]
  }

  statusChart.setOption(option)
}

// 渲染优先级分布饼图
function renderPriorityChart() {
  if (!priorityChartRef.value) return

  if (!priorityChart) {
    priorityChart = echarts.init(priorityChartRef.value)
  }

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      bottom: '0%',
      left: 'center'
    },
    color: ['#F56C6C', '#E6A23C', '#909399'],
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{c}'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: priorityDistribution.value.map(item => ({
          name: item.label,
          value: item.count
        }))
      }
    ]
  }

  priorityChart.setOption(option)
}

// 渲染趋势折线图
function renderTrendChart() {
  if (!trendChartRef.value) return

  if (!trendChart) {
    trendChart = echarts.init(trendChartRef.value)
  }

  const dates = dailyTrend.value.map(item => item.date.substring(5))
  const counts = dailyTrend.value.map(item => item.count)

  const option = {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates
    },
    yAxis: {
      type: 'value',
      minInterval: 1
    },
    series: [
      {
        type: 'line',
        smooth: true,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(64, 158, 255, 0.5)' },
              { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
            ]
          }
        },
        lineStyle: {
          color: '#409EFF',
          width: 2
        },
        itemStyle: {
          color: '#409EFF'
        },
        data: counts
      }
    ]
  }

  trendChart.setOption(option)
}

// 计算活跃度百分比
function calcActiveRate(count) {
  const maxCount = Math.max(...topParticipants.value.map(p => p.event_count), 1)
  return Math.round((count / maxCount) * 100)
}

// 获取进度条颜色
function getProgressColor(count) {
  if (count >= 5) return '#67C23A'
  if (count >= 3) return '#E6A23C'
  return '#909399'
}

// 获取状态类型
function getStatusType(status) {
  const types = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态标签
function getStatusLabel(status) {
  const labels = {
    pending: '待处理',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return labels[status] || status
}

// 获取优先级类型
function getPriorityType(priority) {
  const types = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  }
  return types[priority] || 'info'
}

// 获取优先级标签
function getPriorityLabel(priority) {
  const labels = {
    high: '高',
    medium: '中',
    low: '低'
  }
  return labels[priority] || priority
}

onMounted(() => {
  loadData()
  
  // 监听窗口大小变化，重新渲染图表
  window.addEventListener('resize', () => {
    statusChart?.resize()
    priorityChart?.resize()
    trendChart?.resize()
  })
})
</script>

<style scoped>
.analytics-container {
  padding: 20px;
  min-height: 100vh;
  background: var(--bg-color);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  margin: 0;
  font-size: 24px;
  color: var(--text-primary);
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  font-size: 40px;
  margin-right: 15px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: var(--text-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 5px;
}

@media (max-width: 1200px) {
  .overview-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .overview-cards {
    grid-template-columns: 1fr;
  }
}
</style>




