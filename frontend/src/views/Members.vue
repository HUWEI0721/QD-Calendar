<template>
  <div class="members-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>人员管理</h2>
          <el-button type="primary" @click="showAddDialog" v-if="authStore.isAdmin">
            <el-icon><Plus /></el-icon>
            添加人员
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索姓名、部门、职位"
          style="width: 300px"
          clearable
          @clear="loadMembers"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select
          v-model="statusFilter"
          placeholder="状态筛选"
          clearable
          style="width: 150px; margin-left: 10px"
          @change="loadMembers"
        >
          <el-option label="激活" :value="true" />
          <el-option label="停用" :value="false" />
        </el-select>
        <el-button type="primary" @click="loadMembers" style="margin-left: 10px">
          搜索
        </el-button>
      </div>

      <!-- 人员列表 -->
      <el-table
        :data="members"
        v-loading="loading"
        style="width: 100%; margin-top: 20px"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="department" label="部门" width="120" />
        <el-table-column prop="position" label="职位" width="120" />
        <el-table-column prop="phone" label="电话" width="150" />
        <el-table-column prop="email" label="邮箱" width="200" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '激活' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="showEditDialog(row)">
              编辑
            </el-button>
            <el-popconfirm
              title="确定要删除这个人员吗？"
              @confirm="handleDelete(row.id)"
            >
              <template #reference>
                <el-button type="danger" size="small">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        style="margin-top: 20px; justify-content: center"
        @size-change="loadMembers"
        @current-change="loadMembers"
      />
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form :model="memberForm" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="memberForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="memberForm.department" placeholder="请输入部门" />
        </el-form-item>
        <el-form-item label="职位" prop="position">
          <el-input v-model="memberForm.position" placeholder="请输入职位" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="memberForm.phone" placeholder="请输入电话" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="memberForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="memberForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { getMembers, createMember, updateMember, deleteMember } from '@/api/members'

const authStore = useAuthStore()

const members = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const searchKeyword = ref('')
const statusFilter = ref(null)

const dialogVisible = ref(false)
const dialogTitle = ref('添加人员')
const isEdit = ref(false)
const editId = ref(null)
const formRef = ref(null)

const memberForm = reactive({
  name: '',
  department: '',
  position: '',
  phone: '',
  email: '',
  is_active: true
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
}

// 加载人员列表
async function loadMembers() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value
    }
    
    if (searchKeyword.value) {
      params.search = searchKeyword.value
    }
    
    if (statusFilter.value !== null) {
      params.is_active = statusFilter.value
    }
    
    const response = await getMembers(params)
    members.value = response.members
    total.value = response.total
  } catch (error) {
    ElMessage.error('加载人员列表失败')
  } finally {
    loading.value = false
  }
}

// 显示添加对话框
function showAddDialog() {
  dialogTitle.value = '添加人员'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

// 显示编辑对话框
function showEditDialog(row) {
  dialogTitle.value = '编辑人员'
  isEdit.value = true
  editId.value = row.id
  Object.assign(memberForm, {
    name: row.name,
    department: row.department,
    position: row.position,
    phone: row.phone,
    email: row.email,
    is_active: row.is_active
  })
  dialogVisible.value = true
}

// 重置表单
function resetForm() {
  memberForm.name = ''
  memberForm.department = ''
  memberForm.position = ''
  memberForm.phone = ''
  memberForm.email = ''
  memberForm.is_active = true
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 提交表单
async function handleSubmit() {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      if (isEdit.value) {
        await updateMember(editId.value, memberForm)
        ElMessage.success('更新成功')
      } else {
        await createMember(memberForm)
        ElMessage.success('添加成功')
      }
      dialogVisible.value = false
      loadMembers()
    } catch (error) {
      ElMessage.error(isEdit.value ? '更新失败' : '添加失败')
    }
  })
}

// 删除人员
async function handleDelete(id) {
  try {
    await deleteMember(id)
    ElMessage.success('删除成功')
    loadMembers()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  loadMembers()
})
</script>

<style scoped>
.members-container {
  padding: 20px;
  min-height: 100vh;
  background: var(--bg-color);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 20px;
  color: var(--text-primary);
}

.search-bar {
  display: flex;
  align-items: center;
}
</style>




