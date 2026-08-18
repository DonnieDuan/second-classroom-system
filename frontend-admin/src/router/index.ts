import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/auth/RoleSelectView.vue'),
      meta: { title: '选择登录身份' },
    },
    {
      path: '/login/admin',
      name: 'LoginAdmin',
      component: () => import('../views/auth/LoginAdmin.vue'),
      meta: { title: '管理员登录' },
    },
    {
      path: '/login/teacher',
      name: 'LoginTeacher',
      component: () => import('../views/auth/LoginTeacher.vue'),
      meta: { title: '教师登录' },
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('../views/auth/RegisterView.vue'),
      meta: { title: '注册' },
    },
    {
      path: '/',
      component: () => import('../layouts/MainLayout.vue'),
      redirect: '/dashboard',
      meta: { requiresAuth: true },
      children: [
        // ========== 公共路由 ==========
        { path: 'dashboard', name: 'Dashboard', component: () => import('../views/dashboard/DashboardView.vue'), meta: { title: '仪表盘', roles: ['admin', 'teacher', 'student'] } },

        // ========== 学生路由（学生端已迁移至微信小程序，后台不再提供学生页面） ==========
        { path: 'events', name: 'Events', component: () => import('../views/event/EventManageView.vue'), meta: { title: '赛事信息', roles: ['student'] } },

        // ========== 老师路由 ==========
        { path: 'teacher/class-stats', name: 'TeacherClassStats', component: () => import('../views/teacher/ClassStatsView.vue'), meta: { title: '班级统计', roles: ['teacher'] } },
        { path: 'teacher/warnings', name: 'TeacherWarnings', component: () => import('../views/teacher/WarningsView.vue'), meta: { title: '预警通知', roles: ['teacher'] } },
        { path: 'scores', name: 'Scores', component: () => import('../views/score/ScoreManageView.vue'), meta: { title: '成绩审核', roles: ['teacher'] } },
        { path: 'scores/summary', name: 'ScoreSummary', component: () => import('../views/score/ScoreSummaryView.vue'), meta: { title: '成绩汇总', roles: ['teacher'] } },

        // ========== 管理员路由 ==========
        { path: 'admin/orgs', name: 'AdminOrgs', component: () => import('../views/org/OrgManageView.vue'), meta: { title: '机构管理', roles: ['admin'] } },
        { path: 'admin/students', name: 'AdminStudents', component: () => import('../views/student/StudentManageView.vue'), meta: { title: '学生管理', roles: ['admin'] } },
        { path: 'admin/permissions', name: 'AdminPermissions', component: () => import('../views/admin/PermissionsView.vue'), meta: { title: '权限管理', roles: ['admin'] } },
        { path: 'admin/events', name: 'AdminEvents', component: () => import('../views/event/EventManageView.vue'), meta: { title: '赛事管理', roles: ['admin'] } },
        { path: 'admin/items', name: 'AdminItems', component: () => import('../views/item/ItemManageView.vue'), meta: { title: '赛项管理', roles: ['admin'] } },
        { path: 'admin/event-levels', name: 'AdminEventLevels', component: () => import('../views/event-level/EventLevelView.vue'), meta: { title: '赛事级别', roles: ['admin'] } },
        { path: 'admin/scores', name: 'AdminScores', component: () => import('../views/score/ScoreManageView.vue'), meta: { title: '成绩管理', roles: ['admin'] } },
        { path: 'admin/summary', name: 'AdminSummary', component: () => import('../views/score/ScoreSummaryView.vue'), meta: { title: '成绩汇总', roles: ['admin'] } },
        { path: 'admin/warnings', name: 'AdminWarnings', component: () => import('../views/admin/WarningsView.vue'), meta: { title: '预警管理', roles: ['admin'] } },
        { path: 'admin/rules', name: 'AdminRules', component: () => import('../views/score-require/ScoreRequireView.vue'), meta: { title: '规范制定', roles: ['admin'] } },

        // ========== 兼容旧路由（重定向到新路由） ==========
        { path: 'orgs', redirect: '/admin/orgs' },
        { path: 'students', redirect: '/admin/students' },
        { path: 'score-requires', redirect: '/admin/rules' },
        { path: 'items', redirect: '/admin/items' },
        { path: 'event-levels', redirect: '/admin/event-levels' },
      ],
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole') || ''
  const loginPaths = ['/login', '/login/admin', '/login/teacher']

  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }

  if ((loginPaths.includes(to.path) || to.path === '/register') && token) {
    next('/dashboard')
    return
  }

  // 角色权限校验
  const routeRoles = to.meta.roles as string[] | undefined
  if (routeRoles && !routeRoles.includes(userRole)) {
    next('/dashboard')
    return
  }

  next()
})

export default router
