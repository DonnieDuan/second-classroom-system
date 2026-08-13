<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>成绩填报与证书上传</span>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        style="max-width: 600px"
      >
        <el-form-item label="赛事名称" prop="eventId">
          <el-select
            v-model="form.eventId"
            placeholder="请选择赛事"
            filterable
            style="width: 100%"
            @change="handleEventChange"
          >
            <el-option
              v-for="event in eventList"
              :key="event.eventId"
              :label="`${event.eventName}${event.backStr1 === 'exam' ? ' (考试)' : ''}`"
              :value="event.eventId"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="赛项名称" prop="itemId">
          <el-select
            v-model="form.itemId"
            placeholder="请先选择赛事"
            filterable
            style="width: 100%"
            :disabled="!form.eventId"
          >
            <el-option
              v-for="item in itemList"
              :key="item.itemId"
              :label="item.itemName"
              :value="item.itemId"
            />
          </el-select>
        </el-form-item>

        <!-- 竞赛类：选择获奖级别 -->
        <el-form-item v-if="!isExamType" label="获奖级别" prop="levelId">
          <el-select v-model="form.levelId" placeholder="请选择获奖级别" style="width: 100%">
            <el-option
              v-for="level in levelList"
              :key="level.levelId"
              :label="`${level.levelName} (系数: ${level.levelIndex})`"
              :value="level.levelId"
            />
          </el-select>
        </el-form-item>

        <!-- 考试类：输入分数 -->
        <el-form-item v-else label="考试分数" prop="score">
          <el-input-number
            v-model="form.score"
            :min="0"
            :max="750"
            :precision="1"
            placeholder="请输入考试分数"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="获奖日期" prop="certDate">
          <el-date-picker
            v-model="form.certDate"
            type="date"
            placeholder="请选择获奖日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="证书上传" prop="certPath">
          <el-upload
            class="cert-upload"
            :action="uploadUrl"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
          >
            <el-button type="primary" :loading="uploading">
              {{ uploading ? '上传中...' : '上传证书' }}
            </el-button>
            <template #tip>
              <div class="upload-tip">只能上传 jpg/png/pdf 文件，且不超过 10MB</div>
            </template>
          </el-upload>
          <div v-if="form.certPath" class="cert-preview">
            <el-tag type="success">已上传</el-tag>
            <el-button type="primary" link size="small" @click="previewCert">预览</el-button>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            提交成绩
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 预计得分提示 -->
      <el-alert
        v-if="estimatedScore"
        :title="`预计得分: ${estimatedScore} 分`"
        type="success"
        :closable="false"
        show-icon
        style="max-width: 600px; margin-top: 20px"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { getAllEvents } from '@/api/event'
import { getEventLevelList } from '@/api/eventLevel'
import { getItemsByEventId } from '@/api/item'
import { submitStudentScore } from '@/api/score'
import type { EventInfo, EventLevelInfo, ItemInfo } from '@/types'
import { ElMessage, type FormInstance, type FormRules, type UploadProps } from 'element-plus'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const formRef = ref<FormInstance>()
const submitting = ref(false)
const uploading = ref(false)

const eventList = ref<EventInfo[]>([])
const itemList = ref<ItemInfo[]>([])
const levelList = ref<EventLevelInfo[]>([])

const uploadUrl = 'http://localhost:8080/second-class/api/upload/cert'

const form = ref({
  eventId: undefined as number | undefined,
  itemId: undefined as number | undefined,
  levelId: undefined as number | undefined,
  score: undefined as number | undefined,
  certDate: '',
  certPath: '',
})

// 判断是否考试类型
const isExamType = computed(() => {
  const event = eventList.value.find(e => e.eventId === form.value.eventId)
  return event?.backStr1 === 'exam'
})

// 动态表单规则
const rules = computed<FormRules>(() => {
  const baseRules: FormRules = {
    eventId: [{ required: true, message: '请选择赛事', trigger: 'change' }],
    itemId: [{ required: true, message: '请选择赛项', trigger: 'change' }],
    certDate: [{ required: true, message: '请选择获奖日期', trigger: 'change' }],
  }
  if (isExamType.value) {
    baseRules.score = [{ required: true, message: '请输入考试分数', trigger: 'blur' }]
  } else {
    baseRules.levelId = [{ required: true, message: '请选择获奖级别', trigger: 'change' }]
  }
  return baseRules
})

// 计算预计得分
const estimatedScore = computed(() => {
  if (isExamType.value) {
    return form.value.score?.toFixed(1) || null
  }
  if (!form.value.eventId || !form.value.levelId) return null
  const event = eventList.value.find(e => e.eventId === form.value.eventId)
  const level = levelList.value.find(l => l.levelId === form.value.levelId)
  if (event && level) {
    return (event.baseScore * level.levelIndex).toFixed(2)
  }
  return null
})

async function loadEvents() {
  try {
    const res = await getAllEvents()
    eventList.value = res.data || []
  } catch {
    ElMessage.error('获取赛事列表失败')
  }
}

async function loadLevels() {
  try {
    const res = await getEventLevelList()
    levelList.value = res.data || []
  } catch {
    ElMessage.error('获取获奖级别失败')
  }
}

async function handleEventChange(eventId: number) {
  form.value.itemId = undefined
  itemList.value = []
  if (eventId) {
    try {
      const res = await getItemsByEventId(eventId)
      itemList.value = res.data || []
    } catch {
      ElMessage.error('获取赛项列表失败')
    }
  }
}

const beforeUpload: UploadProps['beforeUpload'] = (rawFile) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf']
  if (!allowedTypes.includes(rawFile.type)) {
    ElMessage.error('只能上传 JPG/PNG/PDF 格式的文件')
    return false
  }
  if (rawFile.size / 1024 / 1024 > 10) {
    ElMessage.error('文件大小不能超过 10MB')
    return false
  }
  uploading.value = true
  return true
}

const handleUploadSuccess: UploadProps['onSuccess'] = (response: any) => {
  uploading.value = false
  if (response.code === 200) {
    form.value.certPath = response.data
    ElMessage.success('证书上传成功')
  } else {
    ElMessage.error(response.msg || '上传失败')
  }
}

function previewCert() {
  if (form.value.certPath) {
    window.open(form.value.certPath, '_blank')
  }
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return

    const stuId = localStorage.getItem('stuId')
    if (!stuId) {
      ElMessage.warning('请先登录')
      return
    }

    submitting.value = true
    try {
      await submitStudentScore({
        stuId: Number(stuId),
        eventId: form.value.eventId,
        itemId: form.value.itemId,
        levelId: form.value.levelId,
        score: form.value.score,
        certDate: form.value.certDate,
        certPath: form.value.certPath,
      })
      ElMessage.success('成绩填报成功！')
      router.push('/student/my-scores')
    } catch {
      ElMessage.error('填报失败，请重试')
    } finally {
      submitting.value = false
    }
  })
}

function resetForm() {
  formRef.value?.resetFields()
  form.value.certPath = ''
  itemList.value = []
}

onMounted(() => {
  loadEvents()
  loadLevels()
})
</script>

<style scoped>
.page-container { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.cert-upload { display: inline-block; }
.upload-tip { font-size: 12px; color: #909399; margin-top: 8px; }
.cert-preview { margin-top: 10px; display: flex; align-items: center; gap: 10px; }
</style>