import request from './request'
import type { ApiResult, PageResult, EventInfo } from '../types'

export const getEventList = (params: any) =>
    request.get<any, ApiResult<PageResult<EventInfo>>>('/event/list', { params })
export const getAllEvents = () => request.get<any, ApiResult<EventInfo[]>>('/event/all')
export const getEventById = (id: number) => request.get<any, ApiResult<EventInfo>>(`/event/${id}`)
export const createEvent = (data: EventInfo) => request.post('/event', data)
export const updateEvent = (id: number, data: EventInfo) => request.put(`/event/${id}`, data)
export const deleteEvents = (ids: number[]) => request.delete('/event', { params: { ids: ids.join(',') } })
