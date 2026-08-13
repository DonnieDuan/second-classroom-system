<template>
  <div class="score-manage">
    <!-- Search filters -->
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="学生姓名">
          <el-input v-model="searchForm.stuName" placeholder="请输入学生姓名" clearable @keyup.enter="handleSearch" />
        </el-form-item>
        <el-form-item label="赛事名称">
          <el-input v-model="searchForm.eventName" placeholder="请输入赛事名称" clearable @keyup.enter="handleSearch" />
        </el-form-item>
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
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Table card -->
    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>成绩列表</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            添加成绩
          </el-button>
        </div>
      </template>
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="scoreId" label="ID" width="60" />
        <el-table-column prop="stuNo" label="学号" width="120" />
        <el-table-column prop="stuName" label="学生" width="100" />
        <el-table-column prop="className" label="班级" width="140" />
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
            <template v-if="row.certPath">
              <el-link v-if="isImageFile(row.certPath)" type="primary" :underline="false" @click="previewImage(row.certPath)">
                预览
              </el-link>
              <el-link v-else type="primary" :href="row.certPath" target="_blank" :underline="false">
                下载
              </el-link>
            </template>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="审核状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getAuditTagType(row.auditStatus)">{{ getAuditStatusText(row.auditStatus) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="审核操作" width="180" fixed="right">
          <template #default="{ row }">
            <template v-if="row.auditStatus === 0">
              <el-button type="success" size="small" link @click="handleAuditPass(row)">
                通过
              </el-button>
              <el-button type="danger" size="small" link @click="handleAuditReject(row)">
                拒绝
              </el-button>
            </template>
            <template v-else-if="row.auditStatus === 1">
              <el-button type="warning" size="small" link @click="handleAuditReset(row)">
                重置审核
              </el-button>
            </template>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button type="warning" size="small" link @click="handleEdit(row)">
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-button type="danger" size="small" link @click="handleDelete(row)">
              <el-icon><Delete /></el-icon> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
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

    <!-- Add / Edit Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑成绩' : '添加成绩'"
      width="600px"
      :close-on-click-modal="false"
      @closed="handleDialogClosed"
    >
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="学生" prop="stuId">
          <el-select
            v-model="formData.stuId"
            filterable
            remote
            reserve-keyword
            placeholder="搜索并选择学生"
            :remote-method="searchStudents"
            :loading="studentLoading"
            style="width: 100%"
          >
            <el-option
              v-for="s in studentOptions"
              :key="s.stuId"
              :label="`${s.stuNo} - ${s.stuName}`"
              :value="s.stuId!"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="赛事" prop="eventId">
          <el-select
            v-model="formData.eventId"
            placeholder="请选择赛事"
            style="width: 100%"
            @change="onEventChange"
          >
            <el-option
              v-for="evt in allEvents"
              :key="evt.eventId"
              :label="evt.eventName"
              :value="evt.eventId!"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="赛项" prop="itemId">
          <el-select
            v-model="formData.itemId"
            placeholder="请选择赛项"
            :disabled="!formData.eventId"
            style="width: 100%"
          >
            <el-option
              v-for="it in filteredItems"
              :key="it.itemId"
              :label="it.itemName"
              :value="it.itemId!"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="级别" prop="levelId">
          <el-select
            v-model="formData.levelId"
            placeholder="请选择级别"
            style="width: 100%"
            @change="onLevelChange"
          >
            <el-option
              v-for="lv in eventLevels"
              :key="lv.levelId"
              :label="`${lv.levelName} (系数: ${lv.levelIndex})`"
              :value="lv.levelId!"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="证书日期" prop="certDate">
          <el-date-picker
            v-model="formData.certDate"
            type="date"
            placeholder="请选择证书日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="证书附件">
          <el-upload
            :http-request="handleUpload"
            :limit="1"
            :on-exceed="handleExceed"
            :file-list="uploadFileList"
            list-type="text"
            :before-upload="beforeUpload"
          >
            <el-button type="primary" size="small">上传文件</el-button>
            <template #tip>
              <div class="el-upload__tip">支持 jpg/png/pdf 格式文件</div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="最终得分">
          <el-input :model-value="computedFinalScore" disabled>
            <template #suffix>={{ selectedEvent?.baseScore ?? 0 }} x {{ selectedLevel?.levelIndex ?? 0 }}</template>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ isEdit ? '保存修改' : '确认添加' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- Image preview dialog -->
    <el-dialog v-model="previewVisible" title="证书预览" width="600px">
      <img :src="previewUrl" style="width: 100%" alt="证书预览" />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { auditScore } from '@/api/admin'
import { getAllEvents } from '@/api/event'
import { getEventLevelList } from '@/api/eventLevel'
import { getItemsByEventId } from '@/api/item'
import { getOrgTree } from '@/api/org'
import { createScore, deleteScores, getScoreList, updateScore } from '@/api/score'
import { getStudentList } from '@/api/student'
import { uploadFile } from '@/api/upload'
import type { EventInfo, EventLevelInfo, ItemInfo, OrgInfo, StuScoreRecord, StudentInfo } from '@/types'
import type { FormInstance, FormRules, UploadFile, UploadRequestOptions } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, onMounted, reactive, ref } from 'vue'

// ---- Search ----
const searchForm = reactive({
  stuName: '',
  eventName: '',
  classOrgId: undefined as number | undefined,
})

const orgTreeData = ref<OrgInfo[]>([])

// ---- Table ----
const tableData = ref<StuScoreRecord[]>([])
const loading = ref(false)
const pagination = reactive({ page: 1, pageSize: 10, total: 0 })

// ---- Dialog ----
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref<FormInstance>()
const editScoreId = ref<number | undefined>(undefined)

const formData = reactive<StuScoreRecord>({
  stuId: 0,
  eventId: 0,
  itemId: 0,
  levelId: 0,
  certDate: '',
  certPath: '',
})

const formRules: FormRules = {
  stuId: [{ required: true, message: '请选择学生', trigger: 'change' }],
  eventId: [{ required: true, message: '请选择赛事', trigger: 'change' }],
  itemId: [{ required: true, message: '请选择赛项', trigger: 'change' }],
  levelId: [{ required: true, message: '请选择级别', trigger: 'change' }],
}

// ---- Student select ----
const studentOptions = ref<StudentInfo[]>([])
const studentLoading = ref(false)

const searchStudents = async (query: string) => {
  studentLoading.value = true
  try {
    const res = await getStudentList({ stuName: query, page: 1, pageSize: 30 })
    studentOptions.value = res.data.rows || []
  } finally {
    studentLoading.value = false
  }
}

// ---- Events, Items, Levels ----
const allEvents = ref<EventInfo[]>([])
const filteredItems = ref<ItemInfo[]>([])
const eventLevels = ref<EventLevelInfo[]>([])

// ---- Upload ----
const uploadFileList = ref<UploadFile[]>([])

const beforeUpload = (file: File) => {
  const isValid = ['image/jpeg', 'image/png', 'application/pdf'].includes(file.type)
  if (!isValid) {
    ElMessage.error('仅支持 jpg、png、pdf 格式文件')
  }
  return isValid
}

const handleUpload = async (options: UploadRequestOptions) => {
  try {
    const res = await uploadFile(options.file as File)
    formData.certPath = res.data
    ElMessage.success('上传成功')
  } catch {
    ElMessage.error('上传失败')
  }
}

const handleExceed = () => {
  ElMessage.warning('只能上传一个文件')
}

// ---- Computed ----
const selectedEvent = computed(() =>
  allEvents.value.find((e) => e.eventId === formData.eventId)
)

const selectedLevel = computed(() =>
  eventLevels.value.find((l) => l.levelId === formData.levelId)
)

const computedFinalScore = computed(() => {
  const base = selectedEvent.value?.baseScore ?? 0
  const idx = selectedLevel.value?.levelIndex ?? 0
  return Number((base * idx).toFixed(2))
})

// ---- Methods ----
const loadData = async () => {
  loading.value = true
  try {
    const params: any = { page: pagination.page, pageSize: pagination.pageSize }
    if (searchForm.stuName) params.stuName = searchForm.stuName
    if (searchForm.eventName) params.eventName = searchForm.eventName
    if (searchForm.classOrgId) params.classOrgId = searchForm.classOrgId
    const res = await getScoreList(params)
    tableData.value = res.data.rows || []
    pagination.total = res.data.total || 0
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadData()
}

const handleReset = () => {
  searchForm.stuName = ''
  searchForm.eventName = ''
  searchForm.classOrgId = undefined
  pagination.page = 1
  loadData()
}

const handleAdd = async () => {
  isEdit.value = false
  editScoreId.value = undefined
  dialogVisible.value = true
  await loadDialogData()
}

const handleEdit = async (row: StuScoreRecord) => {
  isEdit.value = true
  editScoreId.value = row.scoreId
  dialogVisible.value = true
  await loadDialogData()

  // populate form
  Object.assign(formData, {
    stuId: row.stuId,
    eventId: row.eventId,
    itemId: row.itemId,
    levelId: row.levelId,
    certDate: row.certDate,
    certPath: row.certPath || '',
  })

  // load items for the event
  if (row.eventId) {
    const items = await getItemsByEventId(row.eventId)
    filteredItems.value = items.data || []
  }

  // load student into options so the select can display the current value
  if (row.stuId && row.stuName) {
    studentOptions.value = [{ stuId: row.stuId, stuNo: row.stuNo || '', stuName: row.stuName, idCard: '' } as StudentInfo]
  }

  // show existing file in upload list
  if (row.certPath) {
    uploadFileList.value = [{ name: row.certPath, url: row.certPath } as UploadFile]
  }
}

const handleDelete = (row: StuScoreRecord) => {
  ElMessageBox.confirm(`确定要删除学生 ${row.stuName} 的成绩记录吗？`, '删除确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    await deleteScores([row.scoreId!])
    ElMessage.success('删除成功')
    loadData()
  }).catch(() => {})
}

const loadDialogData = async () => {
  // load all events
  const eventsRes = await getAllEvents()
  allEvents.value = eventsRes.data || []

  // load event levels
  const levelsRes = await getEventLevelList()
  eventLevels.value = levelsRes.data || []

  // preload students
  const stuRes = await getStudentList({ page: 1, pageSize: 30 })
  studentOptions.value = stuRes.data.rows || []
}

const onEventChange = async (eventId: number) => {
  formData.itemId = 0
  filteredItems.value = []
  if (eventId) {
    const res = await getItemsByEventId(eventId)
    filteredItems.value = res.data || []
  }
}

const onLevelChange = () => {
  // Just triggers recomputation of computedFinalScore (reactive already)
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const payload: StuScoreRecord = {
      stuId: formData.stuId,
      eventId: formData.eventId,
      itemId: formData.itemId,
      levelId: formData.levelId,
      finalScore: computedFinalScore.value,
      certDate: formData.certDate,
      certPath: formData.certPath,
    }

    if (isEdit.value && editScoreId.value) {
      payload.scoreId = editScoreId.value
      await updateScore(editScoreId.value!, payload)
      ElMessage.success('修改成功')
    } else {
      await createScore(payload)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    loadData()
  } finally {
    submitting.value = false
  }
}

const handleDialogClosed = () => {
  formRef.value?.resetFields()
  formData.stuId = 0
  formData.eventId = 0
  formData.itemId = 0
  formData.levelId = 0
  formData.certDate = ''
  formData.certPath = ''
  uploadFileList.value = []
  filteredItems.value = []
}

// ---- Audit ----
const getAuditStatusText = (auditStatus?: number): string => {
  if (auditStatus === 0) return '待审核'
  if (auditStatus === 1) return '已通过'
  if (auditStatus === 2) return '未通过'
  return '未知'
}

const getAuditTagType = (auditStatus?: number): string => {
  if (auditStatus === 0) return 'warning'
  if (auditStatus === 1) return 'success'
  if (auditStatus === 2) return 'danger'
  return 'info'
}

const handleAuditPass = async (row: StuScoreRecord) => {
  console.log('audit row:', row)
  console.log('scoreId:', row.scoreId)
  ElMessageBox.confirm('确定要通过这条成绩记录吗？', '审核确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'success',
  }).then(async () => {
    try {
      const result = await auditScore({ scoreId: row.scoreId!, auditStatus: 1 })
      console.log('audit result:', result)
      ElMessage.success('审核通过')
      loadData()
    } catch (error: any) {
      console.error('audit error:', error)
      ElMessage.error('审核失败')
    }
  }).catch(() => {})
}

const handleAuditReject = async (row: StuScoreRecord) => {
  ElMessageBox.prompt('请输入拒绝原因', '审核拒绝', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async ({ value }) => {
    try {
      await auditScore({ scoreId: row.scoreId!, auditStatus: 2, auditRemark: value })
      ElMessage.success('已拒绝')
      loadData()
    } catch {
      ElMessage.error('操作失败')
    }
  }).catch(() => {})
}

const handleAuditReset = async (row: StuScoreRecord) => {
  ElMessageBox.confirm('确定要重置审核状态吗？', '重置确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      await auditScore({ scoreId: row.scoreId!, auditStatus: 0 })
      ElMessage.success('已重置')
      loadData()
    } catch {
      ElMessage.error('操作失败')
    }
  }).catch(() => {})
}

// ---- Image preview ----
const previewVisible = ref(false)
const previewUrl = ref('')

const previewImage = (url: string) => {
  previewUrl.value = url
  previewVisible.value = true
}

const isImageFile = (path: string) => {
  return /\.(jpg|jpeg|png|gif|bmp|webp)$/i.test(path)
}

// ---- Lifecycle ----
onMounted(async () => {
  loadData()
  const orgRes = await getOrgTree()
  orgTreeData.value = orgRes.data || []
})
</script>

<style scoped>
.score-manage {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.search-card {
  border-radius: 4px;
}

.search-form {
  margin-bottom: 0;
}

.table-card {
  border-radius: 4px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.final-score {
  font-weight: bold;
  color: #409eff;
}
</style>
