import { httpClient, ApiResult } from '../utils/http';

export interface StuScoreRecord {
  scoreId: number;
  eventName: string;
  itemName: string;
  levelName: string;
  baseScore: number;
  levelIndex: number;
  finalScore: number;
  rawScore?: number;
  certDate: string;
  auditStatus: number;
  auditRemark?: string;
}

export interface ScoreSubmitForm {
  stuId: number;
  eventId: number;
  itemId: number;
  score?: number;
  levelId?: number;
  certDate: string;
  certPath?: string;
}

export interface EventInfo {
  eventId: number;
  eventName: string;
  backStr1?: string;
}

export interface ItemInfo {
  itemId: number;
  itemName: string;
}

export async function getMyScores(stuId: number): Promise<ApiResult<StuScoreRecord[]>> {
  return await httpClient.get(`/app/score/my/${stuId}`);
}

export async function getMyTotalScore(stuId: number): Promise<ApiResult<number>> {
  return await httpClient.get(`/app/score/total/${stuId}`);
}

export async function submitScore(form: ScoreSubmitForm): Promise<ApiResult<string>> {
  return await httpClient.post('/app/score/submit', form);
}

export async function getAllEvents(): Promise<ApiResult<EventInfo[]>> {
  return await httpClient.get('/event/all');
}

export async function getEventById(eventId: number): Promise<ApiResult<EventInfo>> {
  return await httpClient.get(`/event/${eventId}`);
}

export async function getItemsByEvent(eventId: number): Promise<ApiResult<ItemInfo[]>> {
  return await httpClient.get(`/item/event/${eventId}`);
}
