<template>
  <div class="home-container">
    <header class="header">
      <div class="header-content">
        <h1 class="logo">
          <el-icon><Calendar /></el-icon>
          QD日历
        </h1>
        <nav class="nav">
          <el-button link @click="goToCalendar">
            <el-icon><Calendar /></el-icon>
            日历视图
          </el-button>
          <el-button v-if="authStore.isAdmin" type="primary" @click="goToAdmin">
            管理面板
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
        </nav>
      </div>
    </header>
    
    <main class="main-content">
      <div class="hero-section">
        <div class="hero-content">
          <h2 class="hero-title">共享日程管理</h2>
          <p class="hero-subtitle">
            一个优雅的日历应用，让团队协作更高效
          </p>
          <div class="hero-buttons">
            <el-button type="primary" size="large" @click="goToCalendar">
              <el-icon><Calendar /></el-icon>
              查看日历
            </el-button>
            <el-button v-if="!authStore.isAuthenticated" size="large" @click="goToLogin">
              立即开始
            </el-button>
          </div>
        </div>
        <div class="hero-animation">
          <div class="float-card card-1">
            <el-icon size="40"><Calendar /></el-icon>
            <p>日程管理</p>
          </div>
          <div class="float-card card-2">
            <el-icon size="40"><Clock /></el-icon>
            <p>时间追踪</p>
          </div>
          <div class="float-card card-3">
            <el-icon size="40"><Bell /></el-icon>
            <p>智能提醒</p>
          </div>
        </div>
      </div>
      
      <div class="features-section">
        <h3 class="section-title">核心功能</h3>
        <div class="features-grid">
          <div class="feature-card" v-for="feature in features" :key="feature.title">
            <div class="feature-icon">
              <el-icon :size="40">
                <component :is="feature.icon" />
              </el-icon>
            </div>
            <h4>{{ feature.title }}</h4>
            <p>{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </main>
    
    <footer class="footer">
      <p>&copy; 2025 QD日历. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { Calendar, Clock, Bell, User, Lock, Picture, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const features = [
  {
    icon: Calendar,
    title: '日程管理',
    description: '直观的日历视图，轻松管理所有日程事项'
  },
  {
    icon: User,
    title: '权限控制',
    description: '管理员创建日程，普通用户和游客只能查看'
  },
  {
    icon: Picture,
    title: '图片背景',
    description: '为每个日程添加精美的背景图片'
  },
  {
    icon: Bell,
    title: '优先级管理',
    description: '支持高、中、低三种优先级标记'
  },
  {
    icon: Clock,
    title: '时间安排',
    description: '精确到分钟的时间规划'
  },
  {
    icon: Lock,
    title: '安全可靠',
    description: 'JWT认证机制，确保数据安全'
  }
]

const goToCalendar = () => {
  router.push('/calendar')
}

const goToLogin = () => {
  router.push('/login')
}

const goToAdmin = () => {
  router.push('/admin')
}

const handleLogout = () => {
  authStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-color);
}

.header-content {
  max-width: 1200px;
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
}

.nav {
  display: flex;
  gap: 10px;
  align-items: center;
}

.main-content {
  flex: 1;
}

.hero-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.hero-content {
  animation: fadeIn 0.8s ease-out;
}

.hero-title {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 20px;
  color: var(--text-secondary);
  margin-bottom: 30px;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 15px;
}

.hero-animation {
  position: relative;
  height: 400px;
}

.float-card {
  position: absolute;
  padding: 30px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  text-align: center;
  animation: bounce 3s ease-in-out infinite;
}

.float-card p {
  margin-top: 10px;
  font-weight: 600;
  color: var(--text-primary);
}

.card-1 {
  top: 50px;
  left: 50px;
  animation-delay: 0s;
}

.card-2 {
  top: 150px;
  right: 50px;
  animation-delay: 1s;
}

.card-3 {
  bottom: 50px;
  left: 100px;
  animation-delay: 2s;
}

.features-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
  background: white;
}

.section-title {
  font-size: 36px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 50px;
  color: var(--text-primary);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.feature-card {
  padding: 30px;
  background: var(--bg-color);
  border-radius: 15px;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
}

.feature-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  color: white;
}

.feature-card h4 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 10px;
  color: var(--text-primary);
}

.feature-card p {
  color: var(--text-secondary);
  line-height: 1.6;
}

.footer {
  padding: 30px 20px;
  text-align: center;
  background: var(--bg-color);
  color: var(--text-secondary);
  border-top: 1px solid var(--border-color);
}

@media (max-width: 768px) {
  .hero-section {
    grid-template-columns: 1fr;
    padding: 40px 20px;
  }
  
  .hero-animation {
    display: none;
  }
  
  .hero-title {
    font-size: 36px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>

