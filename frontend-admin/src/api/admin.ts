import type { ApiResult } from '../types'
import request from './request'

export interface DashboardStats {
  totalStudents: number
  totalEvents: number
  totalScoreRecords: number
  avgScore: number
  eventTrend: { eventName: string; count: number }[]
  levelDistribution: { levelName: string; count: number }[]
}

export interface ScoreAuditDTO {
  scoreId: number
  auditStatus: number
  auditRemark?: string
}

export const getDashboardStats = () =>
  request.get<any, ApiResult<DashboardStats>>('/admin/dashboard')

export const auditScore = (data: ScoreAuditDTO) =>
  request.post<any, ApiResult<string>>('/admin/audit', data)
