<template>
  <div class="admin-container">
    <header class="admin-header">
      <div class="header-content">
        <h1 class="logo" @click="goToHome">
          <el-icon><Setting /></el-icon>
          管理面板
        </h1>
        <div class="header-actions">
          <el-button @click="goToCalendar">
            <el-icon><Calendar /></el-icon>
            日历视图
          </el-button>
          <el-dropdown>
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
    
    <main class="admin-main">
      <div class="admin-controls">
        <el-button type="primary" size="large" @click="showCreateDialog">
          <el-icon><Plus /></el-icon>
          创建日程
        </el-button>
        
        <div class="search-filters">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索日程..."
            prefix-icon="Search"
            clearable
            @input="handleSearch"
          />
          
          <el-select v-model="statusFilter" placeholder="状态" clearable @change="loadEvents">
            <el-option label="待处理" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
          
          <el-select v-model="priorityFilter" placeholder="优先级" clearable @change="loadEvents">
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </div>
      </div>
      
      <div class="events-table" v-loading="eventsStore.loading">
        <el-table
          :data="filteredEvents"
          stripe
          style="width: 100%"
          @row-click="handleRowClick"
        >
          <el-table-column prop="title" label="标题" min-width="150" />
          
          <el-table-column prop="event_date" label="日期" width="120" />
          
          <el-table-column label="时间" width="150">
            <template #default="{ row }">
              <span v-if="row.start_time">
                {{ row.start_time }} - {{ row.end_time || '--' }}
              </span>
              <span v-else class="text-secondary">未设置</span>
            </template>
          </el-table-column>
          
          <el-table-column label="优先级" width="100">
            <template #default="{ row }">
              <el-tag :type="getPriorityType(row.priority)" size="small">
                {{ getPriorityLabel(row.priority) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="背景图" width="100">
            <template #default="{ row }">
              <el-icon v-if="row.background_image" color="var(--success-color)">
                <Picture />
              </el-icon>
              <span v-else class="text-secondary">无</span>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click.stop="handleEdit(row)">
                编辑
              </el-button>
              <el-button
                size="small"
                type="danger"
                @click.stop="handleDelete(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </main>
    
    <!-- 创建/编辑日程对话框 -->
    <el-dialog
      v-model="eventDialogVisible"
      :title="isEditMode ? '编辑日程' : '创建日程'"
      width="600px"
      @close="resetForm"
    >
      <el-form
        ref="eventFormRef"
        :model="eventForm"
        :rules="eventRules"
        label-width="100px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="eventForm.title" placeholder="请输入日程标题" />
        </el-form-item>
        
        <el-form-item label="日期" prop="event_date">
          <el-date-picker
            v-model="eventForm.event_date"
            type="date"
            placeholder="选择日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="开始时间">
          <el-time-picker
            v-model="eventForm.start_time"
            placeholder="选择开始时间"
            format="HH:mm:ss"
            value-format="HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="结束时间">
          <el-time-picker
            v-model="eventForm.end_time"
            placeholder="选择结束时间"
            format="HH:mm:ss"
            value-format="HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="优先级" prop="priority">
          <el-radio-group v-model="eventForm.priority">
            <el-radio label="low">低</el-radio>
            <el-radio label="medium">中</el-radio>
            <el-radio label="high">高</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-select v-model="eventForm.status" style="width: 100%">
            <el-option label="待处理" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="背景图片">
          <div class="image-upload">
            <el-upload
              :action="uploadAction"
              :headers="uploadHeaders"
              :show-file-list="false"
              :on-success="handleUploadSuccess"
              :before-upload="beforeUpload"
              accept="image/*"
            >
              <el-button size="small" type="primary">
                <el-icon><Upload /></el-icon>
                上传图片
              </el-button>
            </el-upload>
            
            <div v-if="eventForm.background_image" class="preview-image">
              <img :src="eventForm.background_image" alt="背景图" />
              <el-button
                size="small"
                type="danger"
                circle
                @click="eventForm.background_image = ''"
              >
                <el-icon><Close /></el-icon>
              </el-button>
            </div>
          </div>
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input
            v-model="eventForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入日程描述"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="eventDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">
          {{ isEditMode ? '更新' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useEventsStore } from '@/stores/events'
import { uploadImage } from '@/api/events'
import {
  Setting, Calendar, ArrowDown, Plus, Search,
  Picture, Upload, Close
} from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()
const eventsStore = useEventsStore()

const searchKeyword = ref('')
const statusFilter = ref('')
const priorityFilter = ref('')
const eventDialogVisible = ref(false)
const isEditMode = ref(false)
const submitLoading = ref(false)
const eventFormRef = ref(null)
const currentEventId = ref(null)

const eventForm = reactive({
  title: '',
  event_date: '',
  start_time: '',
  end_time: '',
  priority: 'medium',
  status: 'pending',
  background_image: '',
  description: ''
})

const eventRules = {
  title: [
    { required: true, message: '请输入日程标题', trigger: 'blur' }
  ],
  event_date: [
    { required: true, message: '请选择日期', trigger: 'change' }
  ],
  priority: [
    { required: true, message: '请选择优先级', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

const uploadAction = computed(() => '/api/upload/image')
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${authStore.token}`
}))

const filteredEvents = computed(() => {
  if (!searchKeyword.value) {
    return eventsStore.events
  }
  
  return eventsStore.events.filter(event =>
    event.title.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
    (event.description && event.description.toLowerCase().includes(searchKeyword.value.toLowerCase()))
  )
})

async function loadEvents() {
  const params = {}
  
  if (statusFilter.value) {
    params.status = statusFilter.value
  }
  
  if (priorityFilter.value) {
    params.priority = priorityFilter.value
  }
  
  await eventsStore.fetchEvents(params)
}

function handleSearch() {
  // 搜索在 computed 中处理
}

function showCreateDialog() {
  isEditMode.value = false
  resetForm()
  eventDialogVisible.value = true
}

function handleEdit(row) {
  isEditMode.value = true
  currentEventId.value = row.id
  
  Object.assign(eventForm, {
    title: row.title,
    event_date: row.event_date,
    start_time: row.start_time || '',
    end_time: row.end_time || '',
    priority: row.priority,
    status: row.status,
    background_image: row.background_image || '',
    description: row.description || ''
  })
  
  eventDialogVisible.value = true
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(
      `确定要删除日程"${row.title}"吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const result = await eventsStore.removeEvent(row.id)
    
    if (result.success) {
      ElMessage.success('删除成功')
    } else {
      ElMessage.error(result.message)
    }
  } catch (error) {
    // 用户取消删除
  }
}

function handleRowClick(row) {
  handleEdit(row)
}

async function handleSubmit() {
  if (!eventFormRef.value) return
  
  await eventFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitLoading.value = true
    
    try {
      let result
      
      if (isEditMode.value) {
        result = await eventsStore.modifyEvent(currentEventId.value, { ...eventForm })
      } else {
        result = await eventsStore.addEvent({ ...eventForm })
      }
      
      if (result.success) {
        ElMessage.success(isEditMode.value ? '更新成功' : '创建成功')
        eventDialogVisible.value = false
        loadEvents()
      } else {
        ElMessage.error(result.message)
      }
    } finally {
      submitLoading.value = false
    }
  })
}

function resetForm() {
  Object.assign(eventForm, {
    title: '',
    event_date: '',
    start_time: '',
    end_time: '',
    priority: 'medium',
    status: 'pending',
    background_image: '',
    description: ''
  })
  
  if (eventFormRef.value) {
    eventFormRef.value.clearValidate()
  }
}

function beforeUpload(file) {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5
  
  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  
  return true
}

function handleUploadSuccess(response) {
  if (response.url) {
    eventForm.background_image = response.url
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error('图片上传失败')
  }
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
    high: '高',
    medium: '中',
    low: '低'
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

function goToHome() {
  router.push('/')
}

function goToCalendar() {
  router.push('/calendar')
}

function handleLogout() {
  authStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}

onMounted(() => {
  if (!authStore.isAdmin) {
    ElMessage.error('需要管理员权限')
    router.push('/')
    return
  }
  
  loadEvents()
})
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
  background: var(--bg-color);
}

.admin-header {
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

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.admin-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.admin-controls {
  background: white;
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.search-filters {
  display: flex;
  gap: 10px;
  flex: 1;
  justify-content: flex-end;
}

.search-filters .el-input {
  max-width: 300px;
}

.events-table {
  background: white;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.text-secondary {
  color: var(--text-secondary);
}

.image-upload {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.preview-image {
  position: relative;
  width: 200px;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
}

.preview-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-image .el-button {
  position: absolute;
  top: 5px;
  right: 5px;
}

@media (max-width: 768px) {
  .admin-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-filters {
    flex-direction: column;
  }
  
  .search-filters .el-input {
    max-width: 100%;
  }
}
</style>

