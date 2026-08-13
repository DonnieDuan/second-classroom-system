<template>
  <div class="score-summary">
    <!-- Filters -->
    <el-card class="filter-card" shadow="never">
      <el-form :inline="true" :model="searchForm" class="filter-form">
        <el-form-item label="班级组织">
          <el-tree-select
            v-model="searchForm.classOrgId"
            :data="orgTreeData"
            :props="{ label: 'orgName', value: 'orgId', children: 'children' }"
            placeholder="请选择班级"
            clearable
            check-strictly
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="入学年份">
          <el-input v-model="searchForm.enrollYear" placeholder="如 2023" clearable style="width: 140px" />
        </el-form-item>
        <el-form-item label="培养层次">
          <el-select v-model="searchForm.trainLevel" placeholder="请选择" clearable style="width: 140px">
            <el-option label="本科" value="本科" />
            <el-option label="专科" value="专科" />
            <el-option label="硕士" value="硕士" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            查询
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Summary bar -->
    <el-card class="summary-bar-card" shadow="never">
      <div class="summary-bar">
        <div class="summary-item">
          <span class="summary-label">总人数</span>
          <span class="summary-value">{{ summaryStats.totalCount }}</span>
        </div>
        <el-divider direction="vertical" />
        <div class="summary-item">
          <span class="summary-label">平均分</span>
          <span class="summary-value">{{ summaryStats.avgScore }}</span>
        </div>
        <el-divider direction="vertical" />
        <div class="summary-item">
          <span class="summary-label">最高分</span>
          <span class="summary-value highlight">{{ summaryStats.maxScore }}</span>
        </div>
        <el-divider direction="vertical" />
        <div class="summary-item">
          <span class="summary-label">最低分</span>
          <span class="summary-value">{{ summaryStats.minScore }}</span>
        </div>
      </div>
    </el-card>

    <!-- Table -->
    <el-card class="table-card" shadow="never">
      <el-table
        :data="tableData"
        v-loading="loading"
        border
        stripe
        highlight-current-row
        @row-click="handleRowClick"
        style="cursor: pointer"
      >
        <el-table-column prop="stuNo" label="学号" width="120" />
        <el-table-column prop="stuName" label="学生姓名" width="100" />
        <el-table-column prop="className" label="班级" width="140" show-overflow-tooltip />
        <el-table-column prop="enrollYear" label="入学年份" width="100" />
        <el-table-column prop="trainLevel" label="培养层次" width="100" />
        <el-table-column prop="totalScore" label="总成绩" width="100" sortable>
          <template #default="{ row }">
            <span :class="{ 'score-high': row.totalScore >= 80 }">{{ row.totalScore }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="recordCount" label="记录数" width="80" />
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadData"
          @current-change="loadData"
        />
      </div>
    </el-card>

    <!-- Student detail dialog -->
    <el-dialog
      v-model="detailVisible"
      :title="`成绩明细 - ${detailStudent?.stuName} (${detailStudent?.stuNo})`"
      width="900px"
      :close-on-click-modal="false"
    >
      <div v-if="detailLoading" v-loading="detailLoading" style="min-height: 200px" />
      <template v-else>
        <div class="detail-total">
          总成绩：<span class="detail-total-score">{{ detailStudent?.totalScore }}</span>
        </div>
        <el-table :data="detailRecords" border stripe style="margin-top: 12px">
          <el-table-column prop="eventName" label="赛事" min-width="140" show-overflow-tooltip />
          <el-table-column prop="itemName" label="赛项" width="120" />
          <el-table-column prop="levelName" label="级别" width="100" />
          <el-table-column prop="baseScore" label="基础分" width="80" />
          <el-table-column prop="levelIndex" label="等级系数" width="90" />
          <el-table-column prop="finalScore" label="最终得分" width="90">
            <template #default="{ row }">
              <span class="final-score">{{ row.finalScore }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="certDate" label="证书日期" width="110" />
          <el-table-column label="证书附件" width="100">
            <template #default="{ row }">
              <el-link v-if="row.certPath" type="primary" :href="row.certPath" target="_blank" :underline="false">
                查看
              </el-link>
              <span v-else>-</span>
            </template>
          </el-table-column>
        </el-table>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { ScoreSummary, StudentScoreDetail, OrgInfo, StuScoreRecord } from '@/types'
import { getScoreSummary, getStudentScoreDetail } from '@/api/score'
import { getOrgTree } from '@/api/org'

// ---- Filters ----
const searchForm = reactive({
  classOrgId: undefined as number | undefined,
  enrollYear: '',
  trainLevel: '',
})

const orgTreeData = ref<OrgInfo[]>([])

// ---- Table ----
const tableData = ref<ScoreSummary[]>([])
const loading = ref(false)
const pagination = reactive({ page: 1, pageSize: 10, total: 0 })

// ---- Summary stats (from server-side aggregation) ----
const summaryStats = reactive({
  totalCount: 0,
  avgScore: '0.00',
  maxScore: '0.00',
  minScore: '0.00',
})

// ---- Student detail ----
const detailVisible = ref(false)
const detailLoading = ref(false)
const detailStudent = ref<StudentScoreDetail | null>(null)
const detailRecords = ref<StuScoreRecord[]>([])

// ---- Methods ----
const loadData = async () => {
  loading.value = true
  try {
    const params: any = { page: pagination.page, pageSize: pagination.pageSize }
    if (searchForm.classOrgId) params.classOrgId = searchForm.classOrgId
    if (searchForm.enrollYear) params.enrollYear = searchForm.enrollYear
    if (searchForm.trainLevel) params.trainLevel = searchForm.trainLevel
    const res = await getScoreSummary(params)
    const pageData = res.data.page
    tableData.value = pageData.rows || []
    pagination.total = pageData.total || 0
    if (res.data.stats) {
      summaryStats.totalCount = pageData.total || 0
      summaryStats.avgScore = Number(res.data.stats.avgScore || 0).toFixed(2)
      summaryStats.maxScore = Number(res.data.stats.maxScore || 0).toFixed(2)
      summaryStats.minScore = Number(res.data.stats.minScore || 0).toFixed(2)
    }
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadData()
}

const handleReset = () => {
  searchForm.classOrgId = undefined
  searchForm.enrollYear = ''
  searchForm.trainLevel = ''
  pagination.page = 1
  loadData()
}

const handleRowClick = async (row: ScoreSummary) => {
  detailVisible.value = true
  detailLoading.value = true
  try {
    const res = await getStudentScoreDetail(row.stuId)
    detailStudent.value = res.data
    detailRecords.value = res.data.scoreList || []
  } finally {
    detailLoading.value = false
  }
}

// ---- Lifecycle ----
onMounted(async () => {
  loadData()
  const orgRes = await getOrgTree()
  orgTreeData.value = orgRes.data || []
})
</script>

<style scoped>
.score-summary {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.filter-card {
  border-radius: 4px;
}

.filter-form {
  margin-bottom: 0;
}

.summary-bar-card {
  border-radius: 4px;
}

.summary-bar {
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.summary-label {
  font-size: 13px;
  color: #909399;
}

.summary-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.summary-value.highlight {
  color: #e6a23c;
}

.table-card {
  border-radius: 4px;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.score-high {
  font-weight: bold;
  color: #f56c6c;
}

.detail-total {
  font-size: 16px;
  font-weight: 600;
}

.detail-total-score {
  color: #409eff;
  font-size: 20px;
}

.final-score {
  font-weight: bold;
  color: #409eff;
}
</style>
