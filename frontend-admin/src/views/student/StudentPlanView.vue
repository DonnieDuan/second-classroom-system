<template>
  <div class="page-container">
    <!-- 学分进度卡片 -->
    <el-card class="progress-card">
      <template #header>
        <div class="card-header">
          <span>学分进度概览</span>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="progress-item">
            <div class="progress-label">当前已获得学分</div>
            <div class="progress-value">{{ currentScore }}</div>
            <el-progress
              :percentage="progressPercent"
              :color="progressColor"
              :stroke-width="20"
            />
          </div>
        </el-col>
        <el-col :span="12">
          <div class="require-list">
            <div class="require-title">学分要求</div>
            <el-table :data="scoreRequires" border size="small">
              <el-table-column prop="levelName" label="等级" width="100" />
              <el-table-column prop="minScore" label="最低学分" width="80" />
              <el-table-column prop="maxScore" label="最高学分" width="80" />
              <el-table-column label="状态" width="80">
                <template #default="{ row }">
                  <el-tag :type="getRequireStatus(row)">
                    {{ currentScore >= (row.minScore || 0) ? '达标' : '未达标' }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 推荐赛事 -->
    <el-card class="recommend-card">
      <template #header>
        <div class="card-header">
          <span>推荐赛事</span>
          <el-button type="primary" size="small" @click="$router.push('/student/submit')">填报成绩</el-button>
        </div>
      </template>
      <el-table :data="recommendedEvents" border stripe>
        <el-table-column prop="eventName" label="赛事名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="eventLevel" label="赛事级别" width="100" />
        <el-table-column prop="baseScore" label="基础分" width="80" />
        <el-table-column prop="hostUnit" label="主办单位" min-width="120" show-overflow-tooltip />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="$router.push('/student/submit')">
              参赛报名
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 学习建议 -->
    <el-card class="tips-card">
      <template #header>
        <span>学习建议</span>
      </template>
      <el-alert
        v-if="progressPercent < 50"
        title="建议积极参加学科竞赛，获取更多学分"
        type="warning"
        :closable="false"
        show-icon
      />
      <el-alert
        v-else-if="progressPercent < 80"
        title="学分进度良好，继续保持！"
        type="info"
        :closable="false"
        show-icon
      />
      <el-alert
        v-else
        title="学分即将达标，冲刺一下！"
        type="success"
        :closable="false"
        show-icon
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { getAllEvents } from '@/api/event'
import { getMyTotalScore } from '@/api/score'
import { getScoreRequireList } from '@/api/scoreRequire'
import type { EventInfo, ScoreRequire } from '@/types'
import { ElMessage } from 'element-plus'
import { computed, onMounted, ref } from 'vue'

const currentScore = ref(0)
const scoreRequires = ref<ScoreRequire[]>([])
const allEvents = ref<EventInfo[]>([])

const targetScore = computed(() => {
  // 取最高要求作为目标
  const maxReq = scoreRequires.value.reduce((max, r) => Math.max(max, r.maxScore || 0), 0)
  return maxReq || 100
})

const progressPercent = computed(() => {
  const percent = (currentScore.value / targetScore.value) * 100
  return Math.min(Math.round(percent), 100)
})

const progressColor = computed(() => {
  if (progressPercent.value < 50) return '#E6A23C'
  if (progressPercent.value < 80) return '#409EFF'
  return '#67C23A'
})

const recommendedEvents = computed(() => {
  // 推荐基础分较高的赛事
  return allEvents.value
    .filter(e => e.eventStatus === 1)
    .sort((a, b) => b.baseScore - a.baseScore)
    .slice(0, 10)
})

function getRequireStatus(row: ScoreRequire): 'success' | 'warning' | 'danger' {
  return currentScore.value >= (row.minScore || 0) ? 'success' : 'warning'
}

async function fetchData() {
  const stuId = localStorage.getItem('stuId')
  if (!stuId) {
    ElMessage.warning('请先登录')
    return
  }

  try {
    const [scoreRes, requireRes, eventsRes] = await Promise.all([
      getMyTotalScore(Number(stuId)),
      getScoreRequireList(),
      getAllEvents()
    ])
    currentScore.value = scoreRes.data || 0
    scoreRequires.value = requireRes.data || []
    allEvents.value = eventsRes.data || []
  } catch {
    ElMessage.error('获取数据失败')
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.progress-card, .recommend-card, .tips-card { margin-bottom: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.progress-item { padding: 20px; }
.progress-label { font-size: 14px; color: #909399; margin-bottom: 10px; }
.progress-value { font-size: 32px; font-weight: bold; color: #409EFF; margin-bottom: 20px; }
.require-list { padding: 10px; }
.require-title { font-size: 14px; color: #303133; margin-bottom: 10px; }
</style>