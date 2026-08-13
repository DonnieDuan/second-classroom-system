import request from './request'
import type { ApiResult, EventLevelInfo } from '../types'

export const getEventLevelList = () => request.get<any, ApiResult<EventLevelInfo[]>>('/event-level/list')
export const getEventLevelById = (id: number) => request.get<any, ApiResult<EventLevelInfo>>(`/event-level/${id}`)
export const createEventLevel = (data: EventLevelInfo) => request.post('/event-level', data)
export const updateEventLevel = (id: number, data: EventLevelInfo) => request.put(`/event-level/${id}`, data)
export const deleteEventLevels = (ids: number[]) => request.delete('/event-level', { params: { ids: ids.join(',') } })
