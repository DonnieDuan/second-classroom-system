import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: 'http://localhost:8080/second-class/api',
  timeout: 10000,
})

request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

request.interceptors.response.use(
  (response) => {
    const data = response.data
    if (data.code === 200) {
      return data
    } else {
      ElMessage.error(data.msg || '请求失败')
      return Promise.reject(new Error(data.msg))
    }
  },
  (error) => {
    ElMessage.error('网络错误，请稍后重试')
    return Promise.reject(error)
  }
)

export default request
