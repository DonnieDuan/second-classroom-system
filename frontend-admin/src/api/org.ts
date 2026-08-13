import request from './request'
import type { ApiResult, OrgInfo } from '../types'

export const getOrgTree = () => request.get<any, ApiResult<OrgInfo[]>>('/org/tree')
export const getOrgById = (id: number) => request.get<any, ApiResult<OrgInfo>>(`/org/${id}`)
export const createOrg = (data: OrgInfo) => request.post('/org', data)
export const updateOrg = (id: number, data: OrgInfo) => request.put(`/org/${id}`, data)
export const deleteOrgs = (ids: number[]) => request.delete('/org', { params: { ids: ids.join(',') } })
