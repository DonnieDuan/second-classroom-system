<template>
  <div class="event-manage">
    <!-- Search -->
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="事件名称">
          <el-input v-model="searchForm.eventName" placeholder="请输入事件名称" clearable />
        </el-form-item>
        <el-form-item label="事件级别">
          <el-input v-model="searchForm.eventLevel" placeholder="请输入事件级别" clearable />
        </el-form-item>
        <el-form-item label="事件状态">
          <el-select v-model="searchForm.eventStatus" placeholder="请选择状态" clearable>
            <el-option label="未开始" :value="0" />
            <el-option label="进行中" :value="1" />
            <el-option label="已结束" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">添加赛事</el-button>
      <el-button type="danger" :disabled="selectedIds.length === 0" @click="handleBatchDelete">
        批量删除
      </el-button>
    </div>

    <!-- Table -->
    <el-table
      v-loading="loading"
      :data="tableData"
      border
      stripe
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="50" />
      <el-table-column prop="eventId" label="ID" width="80" />
      <el-table-column prop="eventNo" label="赛事编号" width="140" />
      <el-table-column prop="eventName" label="赛事名称" min-width="180" show-overflow-tooltip />
      <el-table-column prop="hostUnit" label="主办单位" min-width="160" show-overflow-tooltip />
      <el-table-column prop="eventLevel" label="赛事级别" width="120" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag v-if="row.eventStatus === 0" type="info">未开始</el-tag>
          <el-tag v-else-if="row.eventStatus === 1" type="success">进行中</el-tag>
          <el-tag v-else-if="row.eventStatus === 2">已结束</el-tag>
          <el-tag v-else type="info">-</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="baseScore" label="基础分" width="100" />
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
      <template #empty>
        <el-empty description="暂无数据" />
      </template>
    </el-table>

    <!-- Pagination -->
    <div class="pagination-wrapper">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchData"
        @current-change="fetchData"
      />
    </div>

    <!-- Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑赛事' : '添加赛事'"
      width="560px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="120px">
        <el-form-item label="赛事编号" prop="eventNo">
          <el-input v-model="form.eventNo" placeholder="请输入赛事编号" />
        </el-form-item>
        <el-form-item label="赛事名称" prop="eventName">
          <el-input v-model="form.eventName" placeholder="请输入赛事名称" />
        </el-form-item>
        <el-form-item label="主办单位" prop="hostUnit">
          <el-input v-model="form.hostUnit" placeholder="请输入主办单位" />
        </el-form-item>
        <el-form-item label="赛事级别" prop="eventLevel">
          <el-input v-model="form.eventLevel" placeholder="请输入赛事级别" />
        </el-form-item>
        <el-form-item label="赛事描述" prop="eventDesc">
          <el-input v-model="form.eventDesc" type="textarea" :rows="3" placeholder="请输入赛事描述" />
        </el-form-item>
        <el-form-item label="赛事状态" prop="eventStatus">
          <el-select v-model="form.eventStatus" placeholder="请选择状态" style="width: 100%">
            <el-option label="未开始" :value="0" />
            <el-option label="进行中" :value="1" />
            <el-option label="已结束" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="基础分" prop="baseScore">
          <el-input-number v-model="form.baseScore" :min="0" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { getEventList, createEvent, updateEvent, deleteEvents } from '@/api/event'
import type { EventInfo } from '@/types'

const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitLoading = ref(false)
const tableData = ref<EventInfo[]>([])
const selectedIds = ref<number[]>([])

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
})

const searchForm = reactive({
  eventName: '',
  eventLevel: '',
  eventStatus: undefined as number | undefined,
})

const formRef = ref<FormInstance>()
const form = reactive<EventInfo>({
  eventNo: '',
  eventName: '',
  hostUnit: '',
  eventLevel: '',
  eventDesc: '',
  eventStatus: 0,
  baseScore: 0,
})

const formRules: FormRules = {
  eventNo: [{ required: true, message: '请输入赛事编号', trigger: 'blur' }],
  eventName: [{ required: true, message: '请输入赛事名称', trigger: 'blur' }],
  eventStatus: [{ required: true, message: '请选择赛事状态', trigger: 'change' }],
  baseScore: [{ required: true, message: '请输入基础分', trigger: 'blur' }],
}

async function fetchData() {
  loading.value = true
  try {
    const params: any = {
      page: pagination.page,
      pageSize: pagination.pageSize,
    }
    if (searchForm.eventName) params.eventName = searchForm.eventName
    if (searchForm.eventLevel) params.eventLevel = searchForm.eventLevel
    if (searchForm.eventStatus !== undefined && searchForm.eventStatus !== null) {
      params.eventStatus = searchForm.eventStatus
    }

    const res = await getEventList(params)
    tableData.value = res.data.rows
    pagination.total = res.data.total
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.page = 1
  fetchData()
}

function handleReset() {
  searchForm.eventName = ''
  searchForm.eventLevel = ''
  searchForm.eventStatus = undefined
  pagination.page = 1
  fetchData()
}

function handleSelectionChange(rows: EventInfo[]) {
  selectedIds.value = rows.map((r) => r.eventId!).filter(Boolean)
}

function resetForm() {
  form.eventId = undefined
  form.eventNo = ''
  form.eventName = ''
  form.hostUnit = ''
  form.eventLevel = ''
  form.eventDesc = ''
  form.eventStatus = 0
  form.baseScore = 0
}

function handleAdd() {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function handleEdit(row: EventInfo) {
  isEdit.value = true
  form.eventId = row.eventId
  form.eventNo = row.eventNo
  form.eventName = row.eventName
  form.hostUnit = row.hostUnit || ''
  form.eventLevel = row.eventLevel || ''
  form.eventDesc = row.eventDesc || ''
  form.eventStatus = row.eventStatus
  form.baseScore = row.baseScore
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitLoading.value = true
  try {
    if (isEdit.value) {
      await updateEvent(form.eventId!, { ...form })
      ElMessage.success('更新成功')
    } else {
      await createEvent({ ...form })
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchData()
  } finally {
    submitLoading.value = false
  }
}

function handleDelete(row: EventInfo) {
  ElMessageBox.confirm('确定删除该赛事吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    await deleteEvents([row.eventId!])
    ElMessage.success('删除成功')
    fetchData()
  })
}

function handleBatchDelete() {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请至少选择一项')
    return
  }
  ElMessageBox.confirm(`确定删除选中的 ${selectedIds.value.length} 条数据吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    await deleteEvents(selectedIds.value)
    ElMessage.success('删除成功')
    selectedIds.value = []
    fetchData()
  })
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.event-manage {
  padding: 16px;
}
.search-bar {
  margin-bottom: 12px;
}
.toolbar {
  margin-bottom: 16px;
}
.pagination-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
