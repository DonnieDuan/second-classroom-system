import request from './request'
import type { ApiResult, PageResult, StuScoreRecord, ScoreSummary, StudentScoreDetail } from '../types'

export const getScoreList = (params: any) =>
    request.get<any, ApiResult<PageResult<StuScoreRecord>>>('/score/list', { params })
export const getScoreSummary = (params: any) =>
    request.get<any, ApiResult<PageResult<ScoreSummary>>>('/score/summary', { params })
export const getStudentScoreDetail = (stuId: number) =>
    request.get<any, ApiResult<StudentScoreDetail>>(`/score/student/${stuId}`)
export const getScoreById = (id: number) => request.get<any, ApiResult<StuScoreRecord>>(`/score/${id}`)
export const createScore = (data: StuScoreRecord) => request.post('/score', data)
export const updateScore = (id: number, data: StuScoreRecord) => request.put(`/score/${id}`, data)
export const deleteScores = (ids: number[]) => request.delete('/score', { params: { ids: ids.join(',') } })

// 学生端成绩接口
export const getMyScores = (stuId: number) =>
    request.get<any, ApiResult<StuScoreRecord[]>>('/app/score/myScores', { params: { stuId } })
export const getMyTotalScore = (stuId: number) =>
    request.get<any, ApiResult<number>>('/app/score/myTotal', { params: { stuId } })
export const submitStudentScore = (data: any) =>
    request.post<any, ApiResult<string>>('/app/score/submit', data)
