<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户权限管理</span>
        </div>
      </template>

      <!-- 角色统计 -->
      <el-row :gutter="20" class="stats-row">
        <el-col :span="6">
          <el-statistic title="管理员" :value="stats.admin" />
        </el-col>
        <el-col :span="6">
          <el-statistic title="教师" :value="stats.teacher" />
        </el-col>
        <el-col :span="6">
          <el-statistic title="学生" :value="stats.student" />
        </el-col>
        <el-col :span="6">
          <el-statistic title="总用户数" :value="stats.total" />
        </el-col>
      </el-row>

      <!-- 筛选 -->
      <el-form :inline="true" class="filter-form">
        <el-form-item label="角色">
          <el-select v-model="selectedRole" placeholder="全部" clearable @change="fetchUsers">
            <el-option label="管理员" value="admin" />
            <el-option label="教师" value="teacher" />
            <el-option label="学生" value="student" />
          </el-select>
        </el-form-item>
      </el-form>

      <!-- 用户列表 -->
      <el-table v-loading="loading" :data="userList" border stripe>
        <el-table-column prop="userId" label="ID" width="80" />
        <el-table-column prop="username" label="账号" width="120" />
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="getRoleTagType(row.role)">{{ getRoleLabel(row.role) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="电话" width="120" />
        <el-table-column prop="deptName" label="部门" min-width="120" show-overflow-tooltip />
        <el-table-column prop="title" label="职称" width="100" />
        <el-table-column prop="createTime" label="创建时间" width="160" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="editUser(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="deleteUser(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        style="margin-top: 20px; justify-content: flex-end"
        @size-change="fetchUsers"
        @current-change="fetchUsers"
      />
    </el-card>

    <!-- 编辑对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑用户" width="500px">
      <el-form ref="editFormRef" :model="editForm" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="editForm.role" style="width: 100%">
            <el-option label="管理员" value="admin" />
            <el-option label="教师" value="teacher" />
            <el-option label="学生" value="student" />
          </el-select>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="editForm.phone" />
        </el-form-item>
        <el-form-item label="部门">
          <el-input v-model="editForm.deptName" />
        </el-form-item>
        <el-form-item label="职称">
          <el-input v-model="editForm.title" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitEdit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import request from '@/api/request'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { onMounted, reactive, ref } from 'vue'

interface UserInfo {
  userId: number
  username: string
  name: string
  role: string
  phone: string
  deptName: string
  title: string
  createTime: string
}

const loading = ref(false)
const submitting = ref(false)
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const selectedRole = ref('')
const userList = ref<UserInfo[]>([])
const editDialogVisible = ref(false)
const editFormRef = ref<FormInstance>()

const stats = reactive({
  admin: 0,
  teacher: 0,
  student: 0,
  total: 0,
})

const editForm = reactive({
  userId: 0,
  name: '',
  role: '',
  phone: '',
  deptName: '',
  title: '',
})

function getRoleTagType(role: string): 'danger' | 'warning' | 'success' {
  const map: Record<string, 'danger' | 'warning' | 'success'> = {
    admin: 'danger',
    teacher: 'warning',
    student: 'success',
  }
  return map[role] || 'info'
}

function getRoleLabel(role: string): string {
  const map: Record<string, string> = {
    admin: '管理员',
    teacher: '教师',
    student: '学生',
  }
  return map[role] || role
}

async function fetchUsers() {
  loading.value = true
  try {
    const res = await request.get('/user/list', {
      params: {
        page: page.value,
        pageSize: pageSize.value,
        role: selectedRole.value,
      },
    })
    userList.value = res.data?.rows || []
    total.value = res.data?.total || 0
    calculateStats()
  } catch {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

function calculateStats() {
  // 简化统计，使用当前页数据估算
  stats.total = total.value
  stats.admin = userList.value.filter(u => u.role === 'admin').length
  stats.teacher = userList.value.filter(u => u.role === 'teacher').length
  stats.student = userList.value.filter(u => u.role === 'student').length
}

function editUser(user: UserInfo) {
  editForm.userId = user.userId
  editForm.name = user.name
  editForm.role = user.role
  editForm.phone = user.phone || ''
  editForm.deptName = user.deptName || ''
  editForm.title = user.title || ''
  editDialogVisible.value = true
}

async function submitEdit() {
  submitting.value = true
  try {
    await request.put(`/user/${editForm.userId}`, editForm)
    ElMessage.success('更新成功')
    editDialogVisible.value = false
    fetchUsers()
  } catch {
    ElMessage.error('更新失败')
  } finally {
    submitting.value = false
  }
}

async function deleteUser(user: UserInfo) {
  await ElMessageBox.confirm(`确定删除用户 ${user.name}？`, '提示', { type: 'warning' })
  try {
    await request.delete(`/user/${user.userId}`)
    ElMessage.success('删除成功')
    fetchUsers()
  } catch {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.stats-row { margin-bottom: 20px; padding: 20px 0; }
.filter-form { margin-bottom: 20px; }
</style>