<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="auth-title">创建账号</h1>
      <p class="auth-subtitle">注册成功后即可使用系统</p>

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
      >
        <!-- 通用字段 -->
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            :placeholder="usernamePlaceholder"
            :prefix-icon="User"
          />
        </el-form-item>

        <el-form-item prop="name">
          <el-input
            v-model="form.name"
            placeholder="请输入姓名"
            :prefix-icon="UserFilled"
          />
        </el-form-item>

        <!-- 管理员特有字段 -->
        <el-form-item v-if="activeRole === 'admin'" prop="adminCode">
          <el-input
            v-model="form.adminCode"
            placeholder="请输入管理员授权码"
            :prefix-icon="Key"
          />
        </el-form-item>

        <!-- 教师特有字段 -->
        <template v-if="activeRole === 'teacher'">
          <el-form-item prop="deptName">
            <el-input
              v-model="form.deptName"
              placeholder="请输入所属院系"
              :prefix-icon="School"
            />
          </el-form-item>
          <el-form-item prop="title">
            <el-select v-model="form.title" placeholder="请选择职称" style="width: 100%">
              <el-option label="教授" value="教授" />
              <el-option label="副教授" value="副教授" />
              <el-option label="讲师" value="讲师" />
              <el-option label="助教" value="助教" />
            </el-select>
          </el-form-item>
        </template>

        <!-- 学生特有字段 -->
        <template v-if="activeRole === 'student'">
          <el-form-item prop="classOrgId">
            <el-input
              v-model="form.classOrgId"
              placeholder="请输入班级（如：软件工程2024-1班）"
              :prefix-icon="Tickets"
            />
          </el-form-item>
          <el-form-item prop="enrollYear">
            <el-input
              v-model="form.enrollYear"
              placeholder="请输入入学年份（如：2024）"
              :prefix-icon="Calendar"
            />
          </el-form-item>
          <el-form-item prop="phone">
            <el-input
              v-model="form.phone"
              placeholder="请输入手机号"
              :prefix-icon="Phone"
            />
          </el-form-item>
        </template>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="请确认密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" class="auth-btn" :loading="loading" @click="handleRegister">
            注 册
          </el-button>
        </el-form-item>
      </el-form>

      <div class="auth-footer">
        已有账号？<router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance } from 'element-plus'
import { registerApi } from '@/api/auth'
import {
  User, Lock, UserFilled, School, Management,
  Key, Tickets, Calendar, Phone,
} from '@element-plus/icons-vue'

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

const activeRole = ref('student')

const form = ref({
  username: '',
  name: '',
  password: '',
  confirmPassword: '',
  adminCode: '',
  deptName: '',
  title: '',
  classOrgId: '',
  enrollYear: '',
  phone: '',
})

const usernamePlaceholder = computed(() => {
  const map: Record<string, string> = {
    admin: '请输入管理员账号',
    teacher: '请输入教师工号',
    student: '请输入学号',
  }
  return map[activeRole.value]
})

const validateConfirmPassword = (_rule: any, value: string, callback: any) => {
  if (value !== form.value.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = computed(() => {
  const base: Record<string, any> = {
    username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
    name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
    ],
    confirmPassword: [
      { required: true, message: '请确认密码', trigger: 'blur' },
      { validator: validateConfirmPassword, trigger: 'blur' },
    ],
  }

  if (activeRole.value === 'admin') {
    base.adminCode = [{ required: true, message: '请输入管理员授权码', trigger: 'blur' }]
  }
  if (activeRole.value === 'teacher') {
    base.deptName = [{ required: true, message: '请输入所属院系', trigger: 'blur' }]
    base.title = [{ required: true, message: '请选择职称', trigger: 'change' }]
  }
  if (activeRole.value === 'student') {
    base.classOrgId = [{ required: true, message: '请输入班级', trigger: 'blur' }]
    base.enrollYear = [
      { required: true, message: '请输入入学年份', trigger: 'blur' },
      { pattern: /^\d{4}$/, message: '请输入正确的年份格式', trigger: 'blur' },
    ]
    base.phone = [
      { required: true, message: '请输入手机号', trigger: 'blur' },
      { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' },
    ]
  }

  return base
})

async function handleRegister() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      await registerApi({
        username: form.value.username,
        password: form.value.password,
        name: form.value.name,
        role: activeRole.value,
        phone: form.value.phone || undefined,
        adminCode: form.value.adminCode || undefined,
        deptName: form.value.deptName || undefined,
        title: form.value.title || undefined,
        classOrgId: form.value.classOrgId || undefined,
        enrollYear: form.value.enrollYear || undefined,
      })
      ElMessage.success('注册成功，请登录')
      router.push('/login')
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
  width: 440px;
  padding: 36px 40px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-height: 90vh;
  overflow-y: auto;
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
  margin-bottom: 24px;
}

.role-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 28px;
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
  margin-top: 4px;
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
