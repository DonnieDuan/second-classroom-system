<template>
  <div class="auth-container student-bg">
    <div class="auth-card">
      <div class="auth-icon-wrap">
        <el-icon :size="48"><UserFilled /></el-icon>
      </div>
      <h1 class="auth-title">学生登录</h1>
      <p class="auth-subtitle">第二课堂成绩管理系统 · 学生中心</p>

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
            placeholder="请输入学号"
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
        <span class="divider">|</span>
        <router-link to="/login/teacher">老师登录</router-link>
      </div>

      <div class="auth-footer">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance } from 'element-plus'
import { User, Lock, UserFilled } from '@element-plus/icons-vue'
import { loginApi } from '@/api/auth'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = ref({ username: '', password: '' })

const rules = {
  username: [{ required: true, message: '请输入学号', trigger: 'blur' }],
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
        role: 'student',
      })
      const { token, username, name, role, stuId, classOrgId } = res.data
      localStorage.setItem('token', token)
      localStorage.setItem('userRole', role)
      localStorage.setItem('username', name || username)
      if (stuId) localStorage.setItem('stuId', String(stuId))
      if (classOrgId) localStorage.setItem('classOrgId', String(classOrgId))
      ElMessage.success('欢迎回来，同学！')
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
.student-bg {
  background: linear-gradient(135deg, #0d2818 0%, #1a4a2e 50%, #2d6a4f 100%);
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
  color: #2d6a4f;
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

.auth-footer {
  text-align: center;
  font-size: 14px;
  color: #909399;
  margin-top: 12px;
}

.auth-footer a {
  color: #409eff;
  text-decoration: none;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>
