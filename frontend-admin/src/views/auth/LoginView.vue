<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="auth-title">第二课堂成绩管理系统</h1>
      <p class="auth-subtitle">登录到您的账户</p>

      <div class="role-tabs">
        <div
          v-for="role in roles"
          :key="role.value"
          class="role-tab"
          :class="{ active: activeRole === role.value }"
          @click="activeRole = role.value"
        >
          <el-icon :size="18"><component :is="role.icon" /></el-icon>
          <span>{{ role.label }}</span>
        </div>
      </div>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="0"
        size="large"
        @keyup.enter="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            :placeholder="usernamePlaceholder"
            :prefix-icon="User"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" class="auth-btn" :loading="loading" @click="handleLogin">
            登 录
          </el-button>
        </el-form-item>
      </el-form>

      <div class="auth-footer">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance } from 'element-plus'
import { User, Lock, UserFilled, School, Management } from '@element-plus/icons-vue'
import { loginApi } from '@/api/auth'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

interface Role {
  label: string
  value: string
  icon: any
}

const roles: Role[] = [
  { label: '管理员', value: 'admin', icon: Management },
  { label: '老师', value: 'teacher', icon: School },
  { label: '学生', value: 'student', icon: UserFilled },
]

const activeRole = ref('admin')

const form = ref({
  username: '',
  password: '',
})

const usernamePlaceholder = computed(() => {
  const map: Record<string, string> = {
    admin: '请输入管理员账号',
    teacher: '请输入教师工号',
    student: '请输入学号',
  }
  return map[activeRole.value]
})

const rules = {
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
  ],
}

async function handleLogin() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      const res: any = await loginApi({
        username: form.value.username,
        password: form.value.password,
        role: activeRole.value,
      })
      const { token, username, name, role } = res.data
      localStorage.setItem('token', token)
      localStorage.setItem('userRole', role)
      localStorage.setItem('username', name || username)
      const roleLabel = role === 'admin' ? '管理员' : role === 'teacher' ? '老师' : '同学'
      ElMessage.success(`欢迎回来，${roleLabel}！`)
      router.push('/dashboard')
    } catch {
      // 错误已在拦截器中处理
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}

.auth-card {
  width: 420px;
  padding: 40px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.auth-title {
  text-align: center;
  font-size: 22px;
  color: #303133;
  margin-bottom: 6px;
}

.auth-subtitle {
  text-align: center;
  font-size: 14px;
  color: #909399;
  margin-bottom: 28px;
}

.role-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 32px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
}

.role-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 0;
  font-size: 14px;
  color: #606266;
  cursor: pointer;
  background: #f5f7fa;
  transition: all 0.3s;
}

.role-tab:hover {
  color: #409eff;
}

.role-tab.active {
  background: #409eff;
  color: #fff;
}

.auth-btn {
  width: 100%;
  letter-spacing: 4px;
}

.auth-footer {
  text-align: center;
  font-size: 14px;
  color: #909399;
}

.auth-footer a {
  color: #409eff;
  text-decoration: none;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>
