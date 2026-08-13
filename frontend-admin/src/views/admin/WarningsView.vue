<template>
  <div class="page-container">
    <!-- 全局预警统计 -->
    <el-card class="stats-card">
      <template #header>
        <div class="card-header">
          <span>全校预警统计</span>
          <el-button type="primary" size="small" :loading="loading" @click="fetchAllData">刷新数据</el-button>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="4">
          <el-statistic title="总学生数" :value="totalStudents" />
        </el-col>
        <el-col :span="4">
          <el-statistic title="达标人数" :value="passedCount" />
        </el-col>
        <el-col :span="4">
          <el-statistic title="接近预警" :value="nearWarningCount" />
        </el-col>
        <el-col :span="4">
          <el-statistic title="预警人数" :value="warningCount" />
        </el-col>
        <el-col :span="4">
          <el-statistic title="达标率" :value="passRate" suffix="%" :precision="2" />
        </el-col>
        <el-col :span="4">
          <el-statistic title="预警率" :value="warningRate" suffix="%" :precision="2" />
        </el-col>
      </el-row>
    </el-card>

    <!-- 班级预警排行 -->
    <el-card class="ranking-card">
      <template #header>
        <span>班级预警排行（按预警人数）</span>
      </template>
      <el-table :data="classWarningRanking" border stripe>
        <el-table-column prop="className" label="班级名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="totalStudents" label="班级人数" width="100" />
        <el-table-column prop="warningCount" label="预警人数" width="100">
          <template #default="{ row }">
            <el-tag :type="row.warningCount > 5 ? 'danger' : 'warning'">{{ row.warningCount }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="warningRate" label="预警率" width="100">
          <template #default="{ row }">
            {{ row.warningRate.toFixed(1) }}%
          </template>
        </el-table-column>
        <el-table-column prop="avgScore" label="平均学分" width="100">
          <template #default="{ row }">
            <span :class="getScoreClass(row.avgScore)">{{ row.avgScore.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewClassDetail(row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 预警学生名单 -->
    <el-card class="list-card">
      <template #header>
        <div class="card-header">
          <span>预警学生名单</span>
          <el-button type="danger" size="small" @click="exportWarnings">导出名单</el-button>
        </div>
      </template>
      <el-table v-loading="loading" :data="warningStudents" border stripe>
        <el-table-column prop="stuNo" label="学号" width="120" />
        <el-table-column prop="stuName" label="姓名" width="100" />
        <el-table-column prop="className" label="班级" min-width="150" show-overflow-tooltip />
        <el-table-column prop="enrollYear" label="入学年份" width="100" />
        <el-table-column prop="trainLevel" label="培养层次" width="100" />
        <el-table-column prop="totalScore" label="当前学分" width="100">
          <template #default="{ row }">
            <span class="score-danger">{{ row.totalScore || 0 }}</span>
          </template>
        </el-table-column>
        <el-table-column label="差距" width="80">
          <template #default="{ row }">
            <span class="gap-danger">{{ minRequiredScore - (row.totalScore || 0) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="预警等级" width="100">
          <template #default="{ row }">
            <el-tag :type="getWarningLevel(row.totalScore)">
              {{ getWarningLevelText(row.totalScore) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        style="margin-top: 20px; justify-content: flex-end"
        @size-change="fetchWarningStudents"
        @current-change="fetchWarningStudents"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getOrgTree } from '@/api/org'
import { getScoreSummary } from '@/api/score'
import { getScoreRequireList } from '@/api/scoreRequire'
import type { OrgInfo, ScoreSummary, ScoreRequire } from '@/types'

interface ClassWarningInfo {
  classOrgId: number
  className: string
  totalStudents: number
  warningCount: number
  warningRate: number
  avgScore: number
}

const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const allStudents = ref<ScoreSummary[]>([])
const classList = ref<OrgInfo[]>([])
const scoreRequires = ref<ScoreRequire[]>([])

const minRequiredScore = computed(() => {
  const min = scoreRequires.value.reduce((m, r) => Math.min(m, r.minScore || 0), 100)
  return min
})

const warningThreshold = computed(() => minRequiredScore.value * 0.6)
const nearWarningThreshold = computed(() => minRequiredScore.value * 0.8)

const totalStudents = computed(() => allStudents.value.length)
const passedCount = computed(() => allStudents.value.filter(s => (s.totalScore || 0) >= nearWarningThreshold.value).length)
const nearWarningCount = computed(() => allStudents.value.filter(s =>
  (s.totalScore || 0) >= warningThreshold.value && (s.totalScore || 0) < nearWarningThreshold.value
).length)
const warningCount = computed(() => allStudents.value.filter(s => (s.totalScore || 0) < warningThreshold.value).length)

const passRate = computed(() => totalStudents.value > 0 ? (passedCount.value / totalStudents.value) * 100 : 0)
const warningRate = computed(() => totalStudents.value > 0 ? (warningCount.value / totalStudents.value) * 100 : 0)

const warningStudents = computed(() => {
  const warnings = allStudents.value.filter(s => (s.totalScore || 0) < warningThreshold.value)
  total.value = warnings.length
  const start = (page.value - 1) * pageSize.value
  return warnings.slice(start, start + pageSize.value)
})

const classWarningRanking = computed(() => {
  const classMap = new Map<number, ClassWarningInfo>()

  for (const student of allStudents.value) {
    const classOrgId = student.classOrgId || 0
    if (!classMap.has(classOrgId)) {
      classMap.set(classOrgId, {
        classOrgId,
        className: student.className || '未知班级',
        totalStudents: 0,
        warningCount: 0,
        warningRate: 0,
        avgScore: 0,
      })
    }
    const info = classMap.get(classOrgId)!
    info.totalStudents++
    if ((student.totalScore || 0) < warningThreshold.value) {
      info.warningCount++
    }
    info.avgScore += student.totalScore || 0
  }

  // 计算预警率和平均分
  for (const info of classMap.values()) {
    info.warningRate = info.totalStudents > 0 ? (info.warningCount / info.totalStudents) * 100 : 0
    info.avgScore = info.totalStudents > 0 ? info.avgScore / info.totalStudents : 0
  }

  // 按预警人数排序
  return Array.from(classMap.values()).sort((a, b) => b.warningCount - a.warningCount)
})

function getScoreClass(score: number): string {
  if (score >= minRequiredScore.value) return 'score-pass'
  return 'score-danger'
}

function getWarningLevel(score: number): 'danger' | 'warning' {
  return score < warningThreshold.value * 0.5 ? 'danger' : 'warning'
}

function getWarningLevelText(score: number): string {
  return score < warningThreshold.value * 0.5 ? '严重' : '轻度'
}

function viewClassDetail(row: ClassWarningInfo) {
  ElMessage.info(`查看班级 ${row.className} 详情`)
}

function exportWarnings() {
  ElMessage.info('导出功能开发中')
}

async function fetchAllData() {
  loading.value = true
  try {
    const res = await getScoreSummary({ page: 1, pageSize: 10000 })
    allStudents.value = res.data?.rows || []
  } catch {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

async function loadClasses() {
  try {
    const res = await getOrgTree()
    classList.value = flattenOrgs(res.data || [])
  } catch {
    // 忽略错误
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

function fetchWarningStudents() {
  // 已在 computed 中处理分页
}

onMounted(() => {
  loadClasses()
  loadRequires()
  fetchAllData()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.stats-card, .ranking-card, .list-card { margin-bottom: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.score-pass { color: #67C23A; font-weight: bold; }
.score-danger { color: #F56C6C; font-weight: bold; }
.gap-danger { color: #F56C6C; font-weight: bold; }
</style>