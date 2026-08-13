<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>班级数据统计分析</span>
          <el-select v-model="selectedClassId" placeholder="选择班级" style="width: 200px" @change="fetchData">
            <el-option
              v-for="org in classList"
              :key="org.orgId"
              :label="org.orgName"
              :value="org.orgId"
            />
          </el-select>
        </div>
      </template>

      <!-- 统计概览 -->
      <el-row :gutter="20" class="stats-row">
        <el-col :span="4">
          <el-statistic title="班级人数" :value="stats.totalStudents" />
        </el-col>
        <el-col :span="4">
          <el-statistic title="平均学分" :value="stats.avgScore" :precision="2" />
        </el-col>
        <el-col :span="4">
          <el-statistic title="最高学分" :value="stats.maxScore" />
        </el-col>
        <el-col :span="4">
          <el-statistic title="最低学分" :value="stats.minScore" />
        </el-col>
        <el-col :span="4">
          <el-statistic title="达标人数" :value="stats.passCount" />
        </el-col>
        <el-col :span="4">
          <el-statistic title="预警人数" :value="stats.warningCount" />
        </el-col>
      </el-row>

      <!-- 学生成绩列表 -->
      <el-table v-loading="loading" :data="studentList" border stripe style="margin-top: 20px">
        <el-table-column prop="stuNo" label="学号" width="120" />
        <el-table-column prop="stuName" label="姓名" width="100" />
        <el-table-column prop="className" label="班级" min-width="120" show-overflow-tooltip />
        <el-table-column prop="enrollYear" label="入学年份" width="100" />
        <el-table-column prop="trainLevel" label="培养层次" width="100" />
        <el-table-column prop="totalScore" label="总学分" width="100">
          <template #default="{ row }">
            <span :class="getScoreClass(row.totalScore)">{{ row.totalScore || 0 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="recordCount" label="获奖次数" width="100" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.totalScore)">
              {{ getStatusText(row.totalScore) }}
            </el-tag>
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
        @size-change="fetchData"
        @current-change="fetchData"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { getOrgTree } from '@/api/org'
import { getScoreSummary } from '@/api/score'
import { getScoreRequireList } from '@/api/scoreRequire'
import type { OrgInfo, ScoreRequire, ScoreSummary } from '@/types'
import { ElMessage } from 'element-plus'
import { computed, onMounted, reactive, ref } from 'vue'

const loading = ref(false)
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const selectedClassId = ref<number | undefined>()
const classList = ref<OrgInfo[]>([])
const studentList = ref<ScoreSummary[]>([])
const scoreRequires = ref<ScoreRequire[]>([])

const stats = reactive({
  totalStudents: 0,
  avgScore: 0,
  maxScore: 0,
  minScore: 0,
  passCount: 0,
  warningCount: 0,
})

const minRequiredScore = computed(() => {
  const min = scoreRequires.value.reduce((m, r) => Math.min(m, r.minScore || 0), 100)
  return min
})

const warningThreshold = computed(() => {
  return minRequiredScore.value * 0.6 // 60% 以下为预警
})

async function loadClasses() {
  try {
    const res = await getOrgTree()
    // 筛选出班级级别的机构
    classList.value = flattenOrgs(res.data || []).filter(o => o.orgLevel === 3)
  } catch {
    ElMessage.error('获取班级列表失败')
  }
}

async function loadRequires() {
  try {
    const res = await getScoreRequireList()
    scoreRequires.value = res.data || []
  } catch {
    // 忽略错误
  }
}

function flattenOrgs(orgs: OrgInfo[]): OrgInfo[] {
  const result: OrgInfo[] = []
  for (const org of orgs) {
    result.push(org)
    if (org.children) {
      result.push(...flattenOrgs(org.children))
    }
  }
  return result
}

async function fetchData() {
  if (!selectedClassId.value) {
    studentList.value = []
    return
  }

  loading.value = true
  try {
    const res = await getScoreSummary({
      page: page.value,
      pageSize: pageSize.value,
      classOrgId: selectedClassId.value,
    })
    studentList.value = res.data?.rows || []
    total.value = res.data?.total || 0

    // 计算统计数据
    calculateStats()
  } catch {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

function calculateStats() {
  if (studentList.value.length === 0) return

  stats.totalStudents = total.value
  const scores = studentList.value.map(s => s.totalScore || 0)
  stats.avgScore = scores.reduce((a, b) => a + b, 0) / scores.length
  stats.maxScore = Math.max(...scores)
  stats.minScore = Math.min(...scores)
  stats.passCount = studentList.value.filter(s => (s.totalScore || 0) >= minRequiredScore.value).length
  stats.warningCount = studentList.value.filter(s => (s.totalScore || 0) < warningThreshold.value).length
}

function getScoreClass(score: number): string {
  if (score >= minRequiredScore.value) return 'score-pass'
  if (score < warningThreshold.value) return 'score-warning'
  return 'score-normal'
}

function getStatusType(score: number): 'success' | 'warning' | 'danger' {
  if (score >= minRequiredScore.value) return 'success'
  if (score < warningThreshold.value) return 'danger'
  return 'warning'
}

function getStatusText(score: number): string {
  if (score >= minRequiredScore.value) return '达标'
  if (score < warningThreshold.value) return '预警'
  return '待达标'
}

onMounted(async () => {
  await loadClasses()
  await loadRequires()
  if (classList.value.length > 0) {
    selectedClassId.value = classList.value[0].orgId
    fetchData()
  }
})
</script>

<style scoped>
.page-container { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.stats-row { margin-bottom: 20px; padding: 20px 0; }
.score-pass { color: #67C23A; font-weight: bold; }
.score-warning { color: #F56C6C; font-weight: bold; }
.score-normal { color: #E6A23C; font-weight: bold; }
</style>