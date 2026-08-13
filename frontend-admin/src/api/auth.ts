import request from './request'

export interface LoginParams {
  username: string
  password: string
  role: string
}

export interface RegisterParams {
  username: string
  password: string
  name: string
  role: string
  phone?: string
  adminCode?: string
  deptName?: string
  title?: string
  classOrgId?: string
  enrollYear?: string
}

export function loginApi(params: LoginParams) {
  return request.post('/auth/login', params)
}

export function registerApi(params: RegisterParams) {
  return request.post('/auth/register', params)
}
