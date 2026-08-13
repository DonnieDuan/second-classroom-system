<template>
  <div class="org-manage">
    <!-- Search & Actions -->
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">添加机构</el-button>
      <el-button type="danger" :disabled="selectedIds.length === 0" @click="handleBatchDelete">
        批量删除
      </el-button>
    </div>

    <!-- Table -->
    <el-table
      v-loading="loading"
      :data="tableData"
      row-key="orgId"
      border
      stripe
      default-expand-all
       :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="50" />
      <el-table-column prop="orgId" label="机构ID" width="80" />
      <el-table-column prop="orgName" label="机构名称" min-width="180" />
      <el-table-column prop="orgCode" label="机构编码" width="160" />
      <el-table-column label="机构级别" width="100">
        <template #default="{ row }">
          {{ orgLevelLabel(row.orgLevel) }}
        </template>
      </el-table-column>
      <el-table-column prop="parentOrgCode" label="上级机构编码" width="150" />
      <el-table-column prop="remark" label="备注" min-width="160" show-overflow-tooltip />
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
      :title="isEdit ? '编辑机构' : '添加机构'"
      width="560px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="120px">
        <el-form-item label="机构名称" prop="orgName">
          <el-input v-model="form.orgName" placeholder="请输入机构名称" />
        </el-form-item>
        <el-form-item label="机构级别" prop="orgLevel">
          <el-select v-model="form.orgLevel" placeholder="请选择机构级别" style="width: 100%">
            <el-option label="学校" :value="1" />
            <el-option label="学院" :value="2" />
            <el-option label="班级" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="上级机构" prop="parentOrgCode">
          <el-select v-model="form.parentOrgCode" placeholder="请选择上级机构" style="width: 100%" clearable filterable>
            <el-option
              v-for="org in flattenOrgList"
              :key="org.orgCode"
              :label="org.orgName"
              :value="org.orgCode"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入备注" />
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
import { createOrg, deleteOrgs, getOrgTree, updateOrg } from '@/api/org'
import type { OrgInfo } from '@/types'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import { onMounted, reactive, ref } from 'vue'

const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitLoading = ref(false)
const tableData = ref<OrgInfo[]>([])
const selectedIds = ref<number[]>([])

const formRef = ref<FormInstance>()
const form = reactive<OrgInfo>({
  orgId: undefined,
  orgCode: '',
  orgName: '',
  orgLevel: 1,
  parentOrgCode: '',
  remark: '',
})

const formRules: FormRules = {
  orgName: [{ required: true, message: '请输入机构名称', trigger: 'blur' }],
  orgLevel: [{ required: true, message: '请选择机构级别', trigger: 'change' }],
}

function generateOrgCode(): string {
  const maxId = Math.max(...tableData.value.flatMap((o: OrgInfo) => [o.orgId!, ...(o.children || []).map((c: OrgInfo) => c.orgId!)], 0))
  return String(maxId + 1).padStart(10, '0')
}

// Flatten tree for parent org selection
function flattenTree(tree: OrgInfo[]): OrgInfo[] {
  const result: OrgInfo[] = []
  function walk(nodes: OrgInfo[]) {
    nodes.forEach((node) => {
      result.push(node)
      if (node.children && node.children.length > 0) {
        walk(node.children)
      }
    })
  }
  walk(tree)
  return result
}

const flattenOrgList = ref<OrgInfo[]>([])

function orgLevelLabel(level?: number): string {
  const map: Record<number, string> = { 1: '学校', 2: '学院', 3: '班级' }
  return level ? map[level] || '-' : '-'
}

function setHasChildren(nodes: OrgInfo[]): void {
  nodes.forEach((node) => {
    node.hasChildren = (node.children && node.children.length > 0) || false
    if (node.children && node.children.length > 0) {
      setHasChildren(node.children)
    }
  })
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getOrgTree()
    tableData.value = res.data
    setHasChildren(tableData.value)
    flattenOrgList.value = flattenTree(res.data)
  } finally {
    loading.value = false
  }
}

function handleSelectionChange(rows: OrgInfo[]) {
  selectedIds.value = rows.map((r) => r.orgId!).filter(Boolean)
}

function resetForm() {
  form.orgId = undefined
  form.orgCode = ''
  form.orgName = ''
  form.orgLevel = 1
  form.parentOrgCode = ''
  form.remark = ''
}

function handleAdd() {
  isEdit.value = false
  resetForm()
  form.orgCode = generateOrgCode()
  dialogVisible.value = true
}

function handleEdit(row: OrgInfo) {
  isEdit.value = true
  form.orgId = row.orgId
  form.orgCode = row.orgCode || ''
  form.orgName = row.orgName
  form.orgLevel = row.orgLevel || 1
  form.parentOrgCode = row.parentOrgCode || ''
  form.remark = row.remark || ''
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitLoading.value = true
  try {
    if (isEdit.value) {
      await updateOrg(form.orgId!, { ...form })
      ElMessage.success('更新成功')
    } else {
      await createOrg({ ...form })
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchData()
  } finally {
    submitLoading.value = false
  }
}

function handleDelete(row: OrgInfo) {
  ElMessageBox.confirm('确定删除该机构吗？若存在子机构也将被删除。', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    await deleteOrgs([row.orgId!])
    ElMessage.success('删除成功')
    fetchData()
  })
}

function handleBatchDelete() {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请至少选择一项')
    return
  }
  ElMessageBox.confirm(`确定删除选中的 ${selectedIds.value.length} 个机构吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    await deleteOrgs(selectedIds.value)
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
.org-manage {
  padding: 16px;
}
.toolbar {
  margin-bottom: 16px;
}
</style>
