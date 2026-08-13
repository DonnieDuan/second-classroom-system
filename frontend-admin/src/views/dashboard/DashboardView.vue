<template>
  <div class="dashboard">
    <!-- Stat cards -->
    <el-row :gutter="20" class="stat-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-inner">
            <div class="stat-icon event-icon">
              <el-icon :size="32"><Notebook /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">赛事总数</div>
              <div class="stat-value">{{ stats.eventCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-inner">
            <div class="stat-icon student-icon">
              <el-icon :size="32"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">学生总数</div>
              <div class="stat-value">{{ stats.studentCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-inner">
            <div class="stat-icon score-icon">
              <el-icon :size="32"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">成绩记录数</div>
              <div class="stat-value">{{ stats.scoreCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-inner">
            <div class="stat-icon avg-icon">
              <el-icon :size="32"><DataAnalysis /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">平均成绩</div>
              <div class="stat-value">{{ stats.avgScore }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Charts -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <span>各赛事参赛人数</span>
          </template>
          <div ref="barChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <span>成绩等级分布</span>
          </template>
          <div ref="pieChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getDashboardStats, type DashboardStats } from '@/api/admin'

const stats = reactive({
  eventCount: 0,
  studentCount: 0,
  scoreCount: 0,
  avgScore: '0.00',
})

const barChartRef = ref<HTMLElement>()
const pieChartRef = ref<HTMLElement>()

let barChart: echarts.ECharts | null = null
let pieChart: echarts.ECharts | null = null

const loadData = async () => {
  const res = await getDashboardStats()
  const data: DashboardStats = res.data

  stats.eventCount = data.totalEvents
  stats.studentCount = data.totalStudents
  stats.scoreCount = data.totalScoreRecords
  stats.avgScore = typeof data.avgScore === 'number' ? data.avgScore.toFixed(2) : '0.00'

  // Bar chart: event trend from server
  const eventTrend = data.eventTrend || []
  const barXAxis = eventTrend.map((d) => d.eventName)
  const barSeries = eventTrend.map((d) => d.count)

  // Pie chart: level distribution from server
  const levelDist = data.levelDistribution || []
  const pieData = levelDist.map((d) => ({ name: d.levelName, value: d.count }))

  await nextTick()
  renderCharts(barXAxis, barSeries, pieData)
}

const renderCharts = (
  barXAxis: string[],
  barSeries: number[],
  pieData: { name: string; value: number }[]
) => {
  if (barChartRef.value) {
    if (!barChart) {
      barChart = echarts.init(barChartRef.value)
    }
    barChart.setOption({
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: {
        type: 'category', data: barXAxis,
        axisLabel: {
          rotate: 30, interval: 0,
          formatter: (value: string) => value.length > 8 ? value.substring(0, 8) + '...' : value,
        },
      },
      yAxis: { type: 'value', name: '参赛人数' },
      series: [{
        name: '参赛人数', type: 'bar', data: barSeries,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#409EFF' }, { offset: 1, color: '#79bbff' },
          ]),
          borderRadius: [4, 4, 0, 0],
        },
        emphasis: { itemStyle: { color: '#337ecc' } },
      }],
    })
  }

  if (pieChartRef.value) {
    if (!pieChart) {
      pieChart = echarts.init(pieChartRef.value)
    }
    pieChart.setOption({
      tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
      legend: { orient: 'vertical', left: 'left', top: 'center' },
      series: [{
        name: '成绩等级', type: 'pie',
        radius: ['40%', '70%'], center: ['60%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 4, borderColor: '#fff', borderWidth: 2 },
        label: { show: true, formatter: '{b}: {c}' },
        emphasis: { label: { fontSize: 16, fontWeight: 'bold' } },
        data: pieData,
      }],
    })
  }
}

const handleResize = () => {
  barChart?.resize()
  pieChart?.resize()
}

onMounted(async () => {
  await loadData()
  window.addEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 20px; }
.stat-row { margin: 0; }
.stat-card { border-radius: 4px; cursor: default; }
.stat-inner { display: flex; align-items: center; gap: 16px; padding: 4px 0; }
.stat-icon { width: 60px; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #fff; }
.event-icon { background: linear-gradient(135deg, #409eff, #79bbff); }
.student-icon { background: linear-gradient(135deg, #67c23a, #95d475); }
.score-icon { background: linear-gradient(135deg, #e6a23c, #f3d19e); }
.avg-icon { background: linear-gradient(135deg, #f56c6c, #fab6b6); }
.stat-info { display: flex; flex-direction: column; gap: 4px; }
.stat-label { font-size: 14px; color: #909399; }
.stat-value { font-size: 28px; font-weight: bold; color: #303133; }
.chart-row { margin: 0; }
.chart-card { border-radius: 4px; }
.chart-container { width: 100%; height: 380px; }
</style>
