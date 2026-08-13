import axios from 'axios'
import { ElMessage } from 'element-plus'

const uploadAxios = axios.create({
  baseURL: 'http://localhost:8080/second-class/api',
  timeout: 30000,
})

uploadAxios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

uploadAxios.interceptors.response.use(
  (response) => {
    const data = response.data
    if (data.code === 200) {
      return data
    } else {
      ElMessage.error(data.msg || '上传失败')
      return Promise.reject(new Error(data.msg))
    }
  },
  (error) => {
    ElMessage.error('上传失败，请稍后重试')
    return Promise.reject(error)
  }
)

export const uploadFile = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return uploadAxios.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}
