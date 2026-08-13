import request from './request'
import type { ApiResult, PageResult, ItemInfo } from '../types'

export const getItemList = (params: any) =>
    request.get<any, ApiResult<PageResult<ItemInfo>>>('/item/list', { params })
export const getItemsByEventId = (eventId: number) =>
    request.get<any, ApiResult<ItemInfo[]>>(`/item/event/${eventId}`)
export const getItemById = (id: number) => request.get<any, ApiResult<ItemInfo>>(`/item/${id}`)
export const createItem = (data: ItemInfo) => request.post('/item', data)
export const updateItem = (id: number, data: ItemInfo) => request.put(`/item/${id}`, data)
export const deleteItems = (ids: number[]) => request.delete('/item', { params: { ids: ids.join(',') } })
