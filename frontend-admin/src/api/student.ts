import request from './request'
import type { ApiResult, PageResult, StudentInfo } from '../types'

export const getStudentList = (params: any) =>
    request.get<any, ApiResult<PageResult<StudentInfo>>>('/student/list', { params })
export const getStudentById = (id: number) => request.get<any, ApiResult<StudentInfo>>(`/student/${id}`)
export const createStudent = (data: StudentInfo) => request.post('/student', data)
export const updateStudent = (id: number, data: StudentInfo) => request.put(`/student/${id}`, data)
export const deleteStudents = (ids: number[]) => request.delete('/student', { params: { ids: ids.join(',') } })
