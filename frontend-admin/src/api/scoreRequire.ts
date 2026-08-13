import request from './request'
import type { ApiResult, ScoreRequire } from '../types'

export const getScoreRequireList = () => request.get<any, ApiResult<ScoreRequire[]>>('/score-require/list')
export const getScoreRequireById = (id: number) => request.get<any, ApiResult<ScoreRequire>>(`/score-require/${id}`)
export const createScoreRequire = (data: ScoreRequire) => request.post('/score-require', data)
export const updateScoreRequire = (id: number, data: ScoreRequire) => request.put(`/score-require/${id}`, data)
export const deleteScoreRequires = (ids: number[]) => request.delete('/score-require', { params: { ids: ids.join(',') } })
