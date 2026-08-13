<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>预警通知</span>
          <div class="header-actions">
            <el-select v-model="selectedClassId" placeholder="选择班级" style="width: 200px" @change="fetchWarnings">
              <el-option
                v-for="org in classList"
                :key="org.orgId"
                :label="org.orgName"
                :value="org.orgId"
              />
            </el-select>
            <el-button type="primary" size="small" :loading="loading" @click="fetchWarnings">刷新</el-button>
          </div>
        </div>
      </template>

      <!-- 预警统计 -->
      <el-row :gutter="20" class="stats-row">
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card danger">
            <div class="stat-content">
              <div class="stat-value">{{ warningList.length }}</div>
              <div class="stat-label">预警学生数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card warning">
            <div class="stat-content">
              <div class="stat-value">{{ nearWarningList.length }}</div>
              <div class="stat-label">接近预警数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card success">
            <div class="stat-content">
              <div class="stat-value">{{ passedList.length }}</div>
              <div class="stat-label">达标学生数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card info">
            <div class="stat-content">
              <div class="stat-value">{{ totalStudents }}</div>
              <div class="stat-label">班级总人数</div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 预警学生列表 -->
      <el-tabs v-model="activeTab">
        <el-tab-pane label="预警学生" name="warning">
          <el-table v-loading="loading" :data="warningList" border stripe>
            <el-table-column prop="stuNo" label="学号" width="120" />
            <el-table-column prop="stuName" label="姓名" width="100" />
            <el-table-column prop="className" label="班级" min-width="120" show-overflow-tooltip />
            <el-table-column prop="enrollYear" label="入学年份" width="100" />
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
                <el-tag type="danger">严重预警</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="建议" min-width="150">
              <template #default>
                <span>建议尽快参加学科竞赛获取学分</span>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="接近预警" name="nearWarning">
          <el-table v-loading="loading" :data="nearWarningList" border stripe>
            <el-table-column prop="stuNo" label="学号" width="120" />
            <el-table-column prop="stuName" label="姓名" width="100" />
            <el-table-column prop="className" label="班级" min-width="120" show-overflow-tooltip />
            <el-table-column prop="totalScore" label="当前学分" width="100">
              <template #default="{ row }">
                <span class="score-warning">{{ row.totalScore || 0 }}</span>
              </template>
            </el-table-column>
            <el-table-column label="差距" width="80">
              <template #default="{ row }">
                <span class="gap-warning">{{ minRequiredScore - (row.totalScore || 0) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="预警等级" width="100">
              <template #default>
                <el-tag type="warning">轻度预警</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="达标学生" name="passed">
          <el-table v-loading="loading" :data="passedList" border stripe>
            <el-table-column prop="stuNo" label="学号" width="120" />
            <el-table-column prop="stuName" label="姓名" width="100" />
            <el-table-column prop="className" label="班级" min-width="120" show-overflow-tooltip />
            <el-table-column prop="totalScore" label="当前学分" width="100">
              <template #default="{ row }">
                <span class="score-success">{{ row.totalScore || 0 }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="recordCount" label="获奖次数" width="100" />
          </el-table>
        </el-tab-pane>
      </el-tabs>

      <el-empty v-if="!selectedClassId" description="请先选择班级查看预警信息" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { getOrgTree } from '@/api/org'
import { getScoreSummary } from '@/api/score'
import { getScoreRequireList } from '@/api/scoreRequire'
import type { OrgInfo, ScoreRequire, ScoreSummary } from '@/types'
import { ElMessage } from 'element-plus'
import { computed, onMounted, ref } from 'vue'

const loading = ref(false)
const selectedClassId = ref<number | undefined>()
const classList = ref<OrgInfo[]>([])
const allStudents = ref<ScoreSummary[]>([])
const scoreRequires = ref<ScoreRequire[]>([])
const activeTab = ref('warning')

const minRequiredScore = computed(() => {
  const min = scoreRequires.value.reduce((m, r) => Math.min(m, r.minScore || 0), 100)
  return min
})

const warningThreshold = computed(() => minRequiredScore.value * 0.6)
const nearWarningThreshold = computed(() => minRequiredScore.value * 0.8)

const warningList = computed(() =>
  allStudents.value.filter(s => (s.totalScore || 0) < warningThreshold.value)
)

const nearWarningList = computed(() =>
  allStudents.value.filter(s =>
    (s.totalScore || 0) >= warningThreshold.value &&
    (s.totalScore || 0) < nearWarningThreshold.value
  )
)

const passedList = computed(() =>
  allStudents.value.filter(s => (s.totalScore || 0) >= nearWarningThreshold.value)
)

const totalStudents = computed(() => allStudents.value.length)

async function loadClasses() {
  try {
    const res = await getOrgTree()
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

async function fetchWarnings() {
  if (!selectedClassId.value) {
    allStudents.value = []
    return
  }

  loading.value = true
  try {
    const res = await getScoreSummary({
      page: 1,
      pageSize: 1000, // 获取全部学生
      classOrgId: selectedClassId.value,
    })
    allStudents.value = res.data?.rows || []
  } catch {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadClasses()
  await loadRequires()
  if (classList.value.length > 0) {
    selectedClassId.value = classList.value[0].orgId
    fetchWarnings()
  }
})
</script>

<style scoped>
.page-container { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.header-actions { display: flex; gap: 10px; }
.stats-row { margin-bottom: 20px; }
.stat-card { text-align: center; }
.stat-card.danger .stat-value { color: #F56C6C; }
.stat-card.warning .stat-value { color: #E6A23C; }
.stat-card.success .stat-value { color: #67C23A; }
.stat-card.info .stat-value { color: #409EFF; }
.stat-content { padding: 15px 0; }
.stat-value { font-size: 24px; font-weight: bold; }
.stat-label { font-size: 12px; color: #909399; margin-top: 5px; }
.score-danger { color: #F56C6C; font-weight: bold; }
.score-warning { color: #E6A23C; font-weight: bold; }
.score-success { color: #67C23A; font-weight: bold; }
.gap-danger { color: #F56C6C; font-weight: bold; }
.gap-warning { color: #E6A23C; font-weight: bold; }
</style>