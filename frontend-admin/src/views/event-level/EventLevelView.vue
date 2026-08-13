<template>
  <div class="event-level-view">
    <!-- Toolbar -->
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">添加事件级别</el-button>
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
      <el-table-column prop="levelId" label="ID" width="80" />
      <el-table-column prop="levelCode" label="级别编码" width="140" />
      <el-table-column prop="levelName" label="级别名称" min-width="180" />
      <el-table-column prop="levelIndex" label="级别序号" width="120" />
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

    <!-- Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑事件级别' : '添加事件级别'"
      width="520px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="120px">
        <el-form-item label="级别编码" prop="levelCode">
          <el-input v-model="form.levelCode" placeholder="请输入级别编码" />
        </el-form-item>
        <el-form-item label="级别名称" prop="levelName">
          <el-input v-model="form.levelName" placeholder="请输入级别名称" />
        </el-form-item>
        <el-form-item label="级别序号" prop="levelIndex">
          <el-input-number v-model="form.levelIndex" :min="0" style="width: 100%" />
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
import { getEventLevelList, createEventLevel, updateEventLevel, deleteEventLevels } from '@/api/eventLevel'
import type { EventLevelInfo } from '@/types'

const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitLoading = ref(false)
const tableData = ref<EventLevelInfo[]>([])
const selectedIds = ref<number[]>([])

const formRef = ref<FormInstance>()
const form = reactive<EventLevelInfo>({
  levelCode: '',
  levelName: '',
  levelIndex: 0,
})

const formRules: FormRules = {
  levelCode: [{ required: true, message: '请输入级别编码', trigger: 'blur' }],
  levelName: [{ required: true, message: '请输入级别名称', trigger: 'blur' }],
  levelIndex: [{ required: true, message: '请输入级别序号', trigger: 'blur' }],
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getEventLevelList()
    tableData.value = res.data
  } finally {
    loading.value = false
  }
}

function handleSelectionChange(rows: EventLevelInfo[]) {
  selectedIds.value = rows.map((r) => r.levelId!).filter(Boolean)
}

function resetForm() {
  form.levelId = undefined
  form.levelCode = ''
  form.levelName = ''
  form.levelIndex = 0
}

function handleAdd() {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function handleEdit(row: EventLevelInfo) {
  isEdit.value = true
  form.levelId = row.levelId
  form.levelCode = row.levelCode
  form.levelName = row.levelName
  form.levelIndex = row.levelIndex
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitLoading.value = true
  try {
    if (isEdit.value) {
      await updateEventLevel(form.levelId!, { ...form })
      ElMessage.success('更新成功')
    } else {
      await createEventLevel({ ...form })
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchData()
  } finally {
    submitLoading.value = false
  }
}

function handleDelete(row: EventLevelInfo) {
  ElMessageBox.confirm('确定删除该事件级别吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    await deleteEventLevels([row.levelId!])
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
    await deleteEventLevels(selectedIds.value)
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
.event-level-view {
  padding: 16px;
}
.toolbar {
  margin-bottom: 16px;
}
</style>
