<template>
  <div class="page-container">
    <!-- 成绩统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-value">{{ totalScore }}</div>
            <div class="stat-label">总成绩</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-value">{{ scoreList.length }}</div>
            <div class="stat-label">获奖次数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-value">{{ nationalCount }}</div>
            <div class="stat-label">国家级获奖</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-value">{{ provincialCount }}</div>
            <div class="stat-label">省级获奖</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 成绩列表 -->
    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>我的成绩记录</span>
          <el-button type="primary" size="small" @click="$router.push('/student/submit')">填报成绩</el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="scoreList" border stripe>
        <el-table-column prop="eventName" label="赛事名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="itemName" label="赛项名称" min-width="120" show-overflow-tooltip />
        <el-table-column prop="levelName" label="获奖级别" width="120">
          <template #default="{ row }">
            <el-tag :type="getLevelTagType(row.levelName)">{{ row.levelName }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="baseScore" label="基础分" width="80" />
        <el-table-column prop="levelIndex" label="级别系数" width="80" />
        <el-table-column prop="finalScore" label="最终得分" width="100">
          <template #default="{ row }">
            <span class="score-value">{{ row.finalScore }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="certDate" label="获奖日期" width="110" />
        <el-table-column label="证书" width="80">
          <template #default="{ row }">
            <el-button v-if="row.certPath" type="primary" link size="small" @click="viewCert(row.certPath)">
              查看
            </el-button>
            <span v-else>-</span>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!loading && scoreList.length === 0" description="暂无成绩记录，快去填报吧！" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { getMyScores, getMyTotalScore } from '@/api/score'
import type { StuScoreRecord } from '@/types'
import { ElMessage } from 'element-plus'
import { computed, onMounted, ref } from 'vue'

const loading = ref(false)
const scoreList = ref<StuScoreRecord[]>([])
const totalScore = ref(0)

const nationalCount = computed(() =>
  scoreList.value.filter(s => s.levelName?.includes('国家') || s.levelName?.includes('全国')).length
)
const provincialCount = computed(() =>
  scoreList.value.filter(s => s.levelName?.includes('省') || s.levelName?.includes('省级')).length
)

function getLevelTagType(levelName: string): 'danger' | 'warning' | 'success' | 'info' {
  if (levelName?.includes('国家') || levelName?.includes('全国')) return 'danger'
  if (levelName?.includes('省') || levelName?.includes('省级')) return 'warning'
  if (levelName?.includes('校') || levelName?.includes('校级')) return 'success'
  return 'info'
}

function viewCert(certPath: string) {
  // TODO: 实现证书查看功能
  ElMessage.info('证书查看功能开发中')
}

async function fetchData() {
  const stuId = localStorage.getItem('stuId')
  if (!stuId) {
    ElMessage.warning('请先登录')
    return
  }

  loading.value = true
  try {
    const [scoresRes, totalRes] = await Promise.all([
      getMyScores(Number(stuId)),
      getMyTotalScore(Number(stuId))
    ])
    scoreList.value = scoresRes.data || []
    totalScore.value = totalRes.data || 0
  } catch {
    ElMessage.error('获取成绩失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.stats-row { margin-bottom: 20px; }
.stat-card { text-align: center; }
.stat-content { padding: 10px 0; }
.stat-value { font-size: 28px; font-weight: bold; color: #409EFF; }
.stat-label { font-size: 14px; color: #909399; margin-top: 8px; }
.table-card { margin-top: 0; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.score-value { font-weight: bold; color: #67C23A; }
</style>