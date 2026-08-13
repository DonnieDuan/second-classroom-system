<template>
  <div class="item-manage">
    <!-- Search -->
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="所属赛事">
          <el-select v-model="searchForm.eventId" placeholder="请选择赛事" clearable filterable>
            <el-option
              v-for="ev in eventList"
              :key="ev.eventId"
              :label="ev.eventName"
              :value="ev.eventId"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="项目名称">
          <el-input v-model="searchForm.itemName" placeholder="请输入项目名称" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">添加项目</el-button>
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
      <el-table-column prop="itemId" label="ID" width="80" />
      <el-table-column prop="eventName" label="所属赛事" min-width="160" show-overflow-tooltip />
      <el-table-column prop="itemNo" label="项目编号" width="140" />
      <el-table-column prop="itemName" label="项目名称" min-width="180" show-overflow-tooltip />
      <el-table-column prop="trackName" label="赛道名称" width="140" />
      <el-table-column prop="teamType" label="团队类型" width="120" />
      <el-table-column prop="deptName" label="承办部门" width="150" />
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
      :title="isEdit ? '编辑项目' : '添加项目'"
      width="560px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="120px">
        <el-form-item label="所属赛事" prop="eventId">
          <el-select v-model="form.eventId" placeholder="请选择赛事" style="width: 100%" filterable>
            <el-option
              v-for="ev in eventList"
              :key="ev.eventId"
              :label="ev.eventName"
              :value="ev.eventId"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="项目编号" prop="itemNo">
          <el-input v-model="form.itemNo" placeholder="请输入项目编号" />
        </el-form-item>
        <el-form-item label="项目名称" prop="itemName">
          <el-input v-model="form.itemName" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="赛道名称" prop="trackName">
          <el-input v-model="form.trackName" placeholder="请输入赛道名称" />
        </el-form-item>
        <el-form-item label="团队类型" prop="teamType">
          <el-input v-model="form.teamType" placeholder="请输入团队类型" />
        </el-form-item>
        <el-form-item label="专业描述" prop="majorDesc">
          <el-input v-model="form.majorDesc" type="textarea" :rows="3" placeholder="请输入专业描述" />
        </el-form-item>
        <el-form-item label="开放条件" prop="openCond">
          <el-input v-model="form.openCond" placeholder="请输入开放条件" />
        </el-form-item>
        <el-form-item label="承办部门" prop="deptName">
          <el-input v-model="form.deptName" placeholder="请输入承办部门" />
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
import { getItemList, createItem, updateItem, deleteItems } from '@/api/item'
import { getAllEvents } from '@/api/event'
import type { ItemInfo, EventInfo } from '@/types'

const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitLoading = ref(false)
const tableData = ref<ItemInfo[]>([])
const eventList = ref<EventInfo[]>([])
const selectedIds = ref<number[]>([])

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
})

const searchForm = reactive({
  eventId: undefined as number | undefined,
  itemName: '',
})

const formRef = ref<FormInstance>()
const form = reactive<ItemInfo>({
  eventId: 0,
  itemNo: '',
  itemName: '',
  trackName: '',
  teamType: '',
  majorDesc: '',
  openCond: '',
  deptName: '',
})

const formRules: FormRules = {
  eventId: [{ required: true, message: '请选择所属赛事', trigger: 'change' }],
  itemNo: [{ required: true, message: '请输入项目编号', trigger: 'blur' }],
  itemName: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
}

async function fetchEvents() {
  try {
    const res = await getAllEvents()
    eventList.value = res.data
  } catch {
    ElMessage.warning('加载赛事列表失败')
  }
}

async function fetchData() {
  loading.value = true
  try {
    const params: any = {
      page: pagination.page,
      pageSize: pagination.pageSize,
    }
    if (searchForm.eventId) params.eventId = searchForm.eventId
    if (searchForm.itemName) params.itemName = searchForm.itemName

    const res = await getItemList(params)
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
  searchForm.eventId = undefined
  searchForm.itemName = ''
  pagination.page = 1
  fetchData()
}

function handleSelectionChange(rows: ItemInfo[]) {
  selectedIds.value = rows.map((r) => r.itemId!).filter(Boolean)
}

function resetForm() {
  form.itemId = undefined
  form.eventId = 0
  form.itemNo = ''
  form.itemName = ''
  form.trackName = ''
  form.teamType = ''
  form.majorDesc = ''
  form.openCond = ''
  form.deptName = ''
}

function handleAdd() {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function handleEdit(row: ItemInfo) {
  isEdit.value = true
  form.itemId = row.itemId
  form.eventId = row.eventId
  form.itemNo = row.itemNo
  form.itemName = row.itemName
  form.trackName = row.trackName || ''
  form.teamType = row.teamType || ''
  form.majorDesc = row.majorDesc || ''
  form.openCond = row.openCond || ''
  form.deptName = row.deptName || ''
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitLoading.value = true
  try {
    if (isEdit.value) {
      await updateItem(form.itemId!, { ...form })
      ElMessage.success('更新成功')
    } else {
      await createItem({ ...form })
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchData()
  } finally {
    submitLoading.value = false
  }
}

function handleDelete(row: ItemInfo) {
  ElMessageBox.confirm('确定删除该项目吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    await deleteItems([row.itemId!])
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
    await deleteItems(selectedIds.value)
    ElMessage.success('删除成功')
    selectedIds.value = []
    fetchData()
  })
}

onMounted(() => {
  fetchEvents()
  fetchData()
})
</script>

<style scoped>
.item-manage {
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
