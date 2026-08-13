<template>
  <el-container class="layout-container">
    <el-aside width="220px">
      <div class="logo">第二课堂成绩管理</div>
      <el-menu
        :default-active="route.path"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item v-for="item in visibleMenus" :key="item.path" :index="item.path">
          <el-icon>
            <component :is="item.icon" />
          </el-icon>
          <span>{{ item.title }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="route.meta.title">{{ route.meta.title }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-tag :type="roleTagType" size="small">{{ roleLabel }}</el-tag>
          <span class="username">{{ username }}</span>
          <el-button type="danger" text size="small" @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import {
  DataAnalysis, OfficeBuilding, User, Trophy,
  Notebook, Collection, Rank, Document, PieChart,
  Calendar, Upload, Bell, Setting, TrendCharts,
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const username = ref(localStorage.getItem('username') || '用户')
const userRole = ref(localStorage.getItem('userRole') || 'admin')

interface MenuItem {
  path: string
  title: string
  icon: any
  roles: string[]
}

const allMenus: MenuItem[] = [
  // ========== 学生菜单 ==========
  { path: '/dashboard', title: '仪表盘', icon: DataAnalysis, roles: ['admin', 'teacher', 'student'] },
  { path: '/student/plan', title: '学习计划', icon: Calendar, roles: ['student'] },
  { path: '/student/submit', title: '成绩填报', icon: Upload, roles: ['student'] },
  { path: '/student/my-scores', title: '我的成绩', icon: PieChart, roles: ['student'] },
  { path: '/events', title: '赛事信息', icon: Notebook, roles: ['student'] },

  // ========== 老师菜单 ==========
  { path: '/teacher/class-stats', title: '班级统计', icon: PieChart, roles: ['teacher'] },
  { path: '/teacher/warnings', title: '预警通知', icon: Bell, roles: ['teacher'] },
  { path: '/scores', title: '成绩审核', icon: Document, roles: ['teacher'] },
  { path: '/scores/summary', title: '成绩汇总', icon: TrendCharts, roles: ['teacher'] },

  // ========== 管理员菜单 ==========
  { path: '/admin/orgs', title: '机构管理', icon: OfficeBuilding, roles: ['admin'] },
  { path: '/admin/students', title: '学生管理', icon: User, roles: ['admin'] },
  { path: '/admin/permissions', title: '权限管理', icon: Setting, roles: ['admin'] },
  { path: '/admin/events', title: '赛事管理', icon: Notebook, roles: ['admin'] },
  { path: '/admin/items', title: '赛项管理', icon: Collection, roles: ['admin'] },
  { path: '/admin/event-levels', title: '赛事级别', icon: Rank, roles: ['admin'] },
  { path: '/admin/scores', title: '成绩管理', icon: Document, roles: ['admin'] },
  { path: '/admin/summary', title: '成绩汇总', icon: TrendCharts, roles: ['admin'] },
  { path: '/admin/warnings', title: '预警管理', icon: Bell, roles: ['admin'] },
  { path: '/admin/rules', title: '规范制定', icon: Trophy, roles: ['admin'] },
]

const visibleMenus = computed(() =>
  allMenus.filter((m) => m.roles.includes(userRole.value))
)

const roleLabel = computed(() => {
  const map: Record<string, string> = { admin: '管理员', teacher: '老师', student: '学生' }
  return map[userRole.value] || '用户'
})

const roleTagType = computed(() => {
  const map: Record<string, string> = { admin: 'danger', teacher: 'warning', student: 'success' }
  return (map[userRole.value] as 'danger' | 'warning' | 'success') || 'info'
})

async function handleLogout() {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    localStorage.removeItem('token')
    localStorage.removeItem('userRole')
    localStorage.removeItem('username')
    router.push('/login')
  } catch {
    // 用户取消
  }
}
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
.layout-container { height: 100vh; }
.el-aside { background-color: #304156; overflow-y: auto; }
.logo { color: #fff; text-align: center; padding: 16px 0; font-size: 16px; font-weight: bold; border-bottom: 1px solid #4a5a6a; }
.el-header {
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}
.header-left { display: flex; align-items: center; }
.header-right { display: flex; align-items: center; gap: 12px; }
.username { font-size: 14px; color: #606266; }
.el-main { background: #f0f2f5; padding: 20px; }
</style>
