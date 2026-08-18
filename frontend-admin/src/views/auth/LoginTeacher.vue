<template>
  <div class="auth-container teacher-bg">
    <div class="auth-card">
      <div class="auth-icon-wrap">
        <el-icon :size="48"><School /></el-icon>
      </div>
      <h1 class="auth-title">教师登录</h1>
      <p class="auth-subtitle">第二课堂成绩管理系统 · 教师工作台</p>

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
            placeholder="请输入教师工号"
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

      <div class="switch-links">
        <router-link to="/login/admin">管理员登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance } from 'element-plus'
import { User, Lock, School } from '@element-plus/icons-vue'
import { loginApi } from '@/api/auth'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = ref({ username: '', password: '' })

const rules = {
  username: [{ required: true, message: '请输入教师工号', trigger: 'blur' }],
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
        role: 'teacher',
      })
      const { token, username, name, role } = res.data
      localStorage.setItem('token', token)
      localStorage.setItem('userRole', role)
      localStorage.setItem('username', name || username)
      ElMessage.success('欢迎回来，老师！')
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
.teacher-bg {
  background: linear-gradient(135deg, #2d1b00 0%, #4a2c17 50%, #6b3a2a 100%);
}

.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-card {
  width: 420px;
  padding: 40px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.auth-icon-wrap {
  text-align: center;
  color: #6b3a2a;
  margin-bottom: 16px;
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
  margin-bottom: 32px;
}

.auth-btn {
  width: 100%;
  letter-spacing: 4px;
}

.switch-links {
  text-align: center;
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
}

.switch-links a {
  color: #409eff;
  text-decoration: none;
}

.switch-links a:hover {
  text-decoration: underline;
}

.switch-links .divider {
  margin: 0 8px;
}
</style>
