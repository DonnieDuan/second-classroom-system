<template>
  <div class="score-require-view">
    <!-- Toolbar -->
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">添加积分要求</el-button>
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
      <el-table-column prop="reqId" label="ID" width="80" />
      <el-table-column prop="levelName" label="等级名称" min-width="180" />
      <el-table-column prop="minScore" label="最低分数" width="120" />
      <el-table-column prop="maxScore" label="最高分数" width="120" />
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
      :title="isEdit ? '编辑积分要求' : '添加积分要求'"
      width="520px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="120px">
        <el-form-item label="等级名称" prop="levelName">
          <el-input v-model="form.levelName" placeholder="请输入等级名称" />
        </el-form-item>
        <el-form-item label="最低分数" prop="minScore">
          <el-input-number v-model="form.minScore" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="最高分数" prop="maxScore">
          <el-input-number v-model="form.maxScore" :min="0" style="width: 100%" />
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
import { getScoreRequireList, createScoreRequire, updateScoreRequire, deleteScoreRequires } from '@/api/scoreRequire'
import type { ScoreRequire } from '@/types'

const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitLoading = ref(false)
const tableData = ref<ScoreRequire[]>([])
const selectedIds = ref<number[]>([])

const formRef = ref<FormInstance>()
const form = reactive<ScoreRequire>({
  levelName: '',
  minScore: undefined,
  maxScore: undefined,
})

const formRules: FormRules = {
  levelName: [{ required: true, message: '请输入等级名称', trigger: 'blur' }],
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getScoreRequireList()
    tableData.value = res.data
  } finally {
    loading.value = false
  }
}

function handleSelectionChange(rows: ScoreRequire[]) {
  selectedIds.value = rows.map((r) => r.reqId!).filter(Boolean)
}

function resetForm() {
  form.reqId = undefined
  form.levelName = ''
  form.minScore = undefined
  form.maxScore = undefined
}

function handleAdd() {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function handleEdit(row: ScoreRequire) {
  isEdit.value = true
  form.reqId = row.reqId
  form.levelName = row.levelName
  form.minScore = row.minScore
  form.maxScore = row.maxScore
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitLoading.value = true
  try {
    if (isEdit.value) {
      await updateScoreRequire(form.reqId!, { ...form })
      ElMessage.success('更新成功')
    } else {
      await createScoreRequire({ ...form })
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchData()
  } finally {
    submitLoading.value = false
  }
}

function handleDelete(row: ScoreRequire) {
  ElMessageBox.confirm('确定删除该积分要求吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    await deleteScoreRequires([row.reqId!])
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
    await deleteScoreRequires(selectedIds.value)
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
.score-require-view {
  padding: 16px;
}
.toolbar {
  margin-bottom: 16px;
}
</style>
