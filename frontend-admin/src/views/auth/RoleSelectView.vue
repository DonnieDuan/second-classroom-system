<template>
  <div class="landing-container">
    <div class="landing-box">
      <h1 class="landing-title">第二课堂成绩管理系统</h1>
      <p class="landing-subtitle">请选择您的身份登录</p>

      <div class="role-cards">
        <div class="role-card admin-card" @click="$router.push('/login/admin')">
          <div class="card-icon">
            <el-icon :size="42"><Management /></el-icon>
          </div>
          <h3>管理员</h3>
          <p>系统管理与数据维护</p>
        </div>

        <div class="role-card teacher-card" @click="$router.push('/login/teacher')">
          <div class="card-icon">
            <el-icon :size="42"><School /></el-icon>
          </div>
          <h3>老 师</h3>
          <p>成绩录入与审核管理</p>
        </div>

        <div class="role-card student-card" @click="$router.push('/login/student')">
          <div class="card-icon">
            <el-icon :size="42"><UserFilled /></el-icon>
          </div>
          <h3>学 生</h3>
          <p>成绩查询与报名参赛</p>
        </div>
      </div>

      <div class="landing-footer">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Management, School, UserFilled } from '@element-plus/icons-vue'
</script>

<style scoped>
.landing-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}

.landing-box {
  width: 720px;
  padding: 48px 40px;
  text-align: center;
}

.landing-title {
  font-size: 28px;
  color: #fff;
  margin-bottom: 8px;
  letter-spacing: 2px;
}

.landing-subtitle {
  font-size: 16px;
  color: #a0aec0;
  margin-bottom: 48px;
}

.role-cards {
  display: flex;
  gap: 24px;
  justify-content: center;
}

.role-card {
  width: 200px;
  padding: 32px 20px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  cursor: pointer;
  transition: all 0.3s ease;
}

.role-card:hover {
  transform: translateY(-6px);
}

.role-card .card-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.role-card h3 {
  font-size: 18px;
  color: #fff;
  margin-bottom: 8px;
}

.role-card p {
  font-size: 13px;
  color: #a0aec0;
}

.admin-card:hover {
  background: rgba(26, 26, 46, 0.7);
  border-color: #667eea;
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.35);
}

.admin-card .card-icon { color: #667eea; }

.teacher-card:hover {
  background: rgba(107, 58, 42, 0.5);
  border-color: #e07b39;
  box-shadow: 0 12px 40px rgba(224, 123, 57, 0.35);
}

.teacher-card .card-icon { color: #e07b39; }

.student-card:hover {
  background: rgba(45, 106, 79, 0.5);
  border-color: #48bb78;
  box-shadow: 0 12px 40px rgba(72, 187, 120, 0.35);
}

.student-card .card-icon { color: #48bb78; }

.landing-footer {
  margin-top: 48px;
  font-size: 14px;
  color: #a0aec0;
}

.landing-footer a {
  color: #409eff;
  text-decoration: none;
}

.landing-footer a:hover {
  text-decoration: underline;
}
</style>
