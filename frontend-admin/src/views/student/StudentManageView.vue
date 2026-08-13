<template>
  <div class="student-manage">
    <!-- Search -->
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="学生姓名">
          <el-input v-model="searchForm.stuName" placeholder="请输入姓名" clearable />
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="searchForm.gender" placeholder="请选择性别" clearable>
            <el-option label="男" value="男" />
            <el-option label="女" value="女" />
          </el-select>
        </el-form-item>
        <el-form-item label="班级">
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
          <el-input v-model="searchForm.enrollYear" placeholder="请输入年份" clearable />
        </el-form-item>
        <el-form-item label="培养层次">
          <el-input v-model="searchForm.trainLevel" placeholder="请输入培养层次" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">添加学生</el-button>
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
      <el-table-column prop="stuId" label="ID" width="80" />
      <el-table-column prop="stuNo" label="学号" width="140" />
      <el-table-column prop="stuName" label="姓名" width="120" />
      <el-table-column label="性别" width="80">
        <template #default="{ row }">
          <el-tag v-if="row.gender === '男'" type="primary">男</el-tag>
          <el-tag v-else-if="row.gender === '女'" type="danger">女</el-tag>
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column prop="className" label="班级" min-width="160" show-overflow-tooltip />
      <el-table-column prop="enrollYear" label="入学年份" width="110" />
      <el-table-column prop="trainLevel" label="培养层次" width="120" />
      <el-table-column prop="phone" label="手机号" width="140" />
      <el-table-column label="身份证号" width="180">
        <template #default="{ row }">
          {{ maskIdCard(row.idCard) }}
        </template>
      </el-table-column>
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
      :title="isEdit ? '编辑学生' : '添加学生'"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="120px">
        <el-form-item label="学号" prop="stuNo">
          <el-input v-model="form.stuNo" placeholder="请输入学号" />
        </el-form-item>
        <el-form-item label="姓名" prop="stuName">
          <el-input v-model="form.stuName" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="form.gender">
            <el-radio value="男">男</el-radio>
            <el-radio value="女">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="班级" prop="classOrgId">
          <el-tree-select
            v-model="form.classOrgId"
            :data="orgTreeData"
            :props="{ label: 'orgName', value: 'orgId', children: 'children' }"
            placeholder="请选择班级"
            check-strictly
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="入学年份" prop="enrollYear">
          <el-input v-model="form.enrollYear" placeholder="请输入入学年份" />
        </el-form-item>
        <el-form-item label="身份证号" prop="idCard">
          <el-input v-model="form.idCard" placeholder="请输入身份证号" />
        </el-form-item>
        <el-form-item label="出生日期" prop="birthDate">
          <el-date-picker
            v-model="form.birthDate"
            type="date"
            placeholder="请选择出生日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="培养层次" prop="trainLevel">
          <el-select v-model="form.trainLevel" placeholder="请选择培养层次" style="width: 100%" clearable>
            <el-option label="本科" value="本科" />
            <el-option label="专科" value="专科" />
            <el-option label="专升本" value="专升本" />
          </el-select>
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
import { getStudentList, createStudent, updateStudent, deleteStudents } from '@/api/student'
import { getOrgTree } from '@/api/org'
import type { StudentInfo, OrgInfo } from '@/types'

const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitLoading = ref(false)
const tableData = ref<StudentInfo[]>([])
const orgTreeData = ref<OrgInfo[]>([])
const selectedIds = ref<number[]>([])

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
})

const searchForm = reactive({
  stuName: '',
  gender: '',
  classOrgId: undefined as number | undefined,
  enrollYear: '',
  trainLevel: '',
})

const formRef = ref<FormInstance>()
const form = reactive<StudentInfo & { birthDate?: string }>({
  stuNo: '',
  stuName: '',
  gender: '男',
  phone: '',
  classOrgId: undefined,
  enrollYear: '',
  idCard: '',
  birthDate: '',
  trainLevel: '',
})

const formRules: FormRules = {
  stuNo: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  stuName: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  classOrgId: [{ required: true, message: '请选择班级', trigger: 'change' }],
  idCard: [{ required: true, message: '请输入身份证号', trigger: 'blur' }],
}

function maskIdCard(idCard?: string): string {
  if (!idCard) return '-'
  if (idCard.length <= 10) return idCard
  return idCard.substring(0, 6) + '****' + idCard.substring(idCard.length - 4)
}

async function fetchOrgTree() {
  try {
    const res = await getOrgTree()
    orgTreeData.value = res.data
  } catch {
    ElMessage.warning('加载组织树失败')
  }
}

async function fetchData() {
  loading.value = true
  try {
    const params: any = {
      page: pagination.page,
      pageSize: pagination.pageSize,
    }
    if (searchForm.stuName) params.stuName = searchForm.stuName
    if (searchForm.gender) params.gender = searchForm.gender
    if (searchForm.classOrgId) params.classOrgId = searchForm.classOrgId
    if (searchForm.enrollYear) params.enrollYear = searchForm.enrollYear
    if (searchForm.trainLevel) params.trainLevel = searchForm.trainLevel

    const res = await getStudentList(params)
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
  searchForm.stuName = ''
  searchForm.gender = ''
  searchForm.classOrgId = undefined
  searchForm.enrollYear = ''
  searchForm.trainLevel = ''
  pagination.page = 1
  fetchData()
}

function handleSelectionChange(rows: StudentInfo[]) {
  selectedIds.value = rows.map((r) => r.stuId!).filter(Boolean)
}

function resetForm() {
  form.stuId = undefined
  form.stuNo = ''
  form.stuName = ''
  form.gender = '男'
  form.phone = ''
  form.classOrgId = undefined
  form.enrollYear = ''
  form.idCard = ''
  form.birthDate = ''
  form.trainLevel = ''
}

function handleAdd() {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function handleEdit(row: StudentInfo) {
  isEdit.value = true
  form.stuId = row.stuId
  form.stuNo = row.stuNo
  form.stuName = row.stuName
  form.gender = row.gender || '男'
  form.phone = row.phone || ''
  form.classOrgId = row.classOrgId
  form.enrollYear = row.enrollYear || ''
  form.idCard = row.idCard
  form.birthDate = row.birthDate || ''
  form.trainLevel = row.trainLevel || ''
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitLoading.value = true
  try {
    if (isEdit.value) {
      await updateStudent(form.stuId!, { ...form })
      ElMessage.success('更新成功')
    } else {
      await createStudent({ ...form })
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchData()
  } finally {
    submitLoading.value = false
  }
}

function handleDelete(row: StudentInfo) {
  ElMessageBox.confirm('确定删除该学生吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    await deleteStudents([row.stuId!])
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
    await deleteStudents(selectedIds.value)
    ElMessage.success('删除成功')
    selectedIds.value = []
    fetchData()
  })
}

onMounted(() => {
  fetchOrgTree()
  fetchData()
})
</script>

<style scoped>
.student-manage {
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
