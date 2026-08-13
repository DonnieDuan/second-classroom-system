export interface ApiResult<T = any> {
  code: number
  msg: string
  data: T
}

export interface PageResult<T> {
  total: number
  rows: T[]
}

export interface OrgInfo {
  orgId?: number
  orgCode?: string
  orgName: string
  orgLevel?: number
  parentOrgCode?: string
  remark?: string
  children?: OrgInfo[]
  hasChildren?: boolean
}

export interface StudentInfo {
  stuId?: number
  stuNo: string
  stuName: string
  gender?: string
  phone?: string
  classOrgId?: number
  className?: string
  enrollYear?: string
  idCard: string
  birthDate?: string
  trainLevel?: string
}

export interface ScoreRequire {
  reqId?: number
  levelName: string
  minScore?: number
  maxScore?: number
}

export interface EventInfo {
  eventId?: number
  eventNo: string
  eventName: string
  hostUnit?: string
  eventLevel?: string
  eventDesc?: string
  charterPath?: string
  eventStatus: number
  baseScore: number
  backStr1?: string
}

export interface ItemInfo {
  itemId?: number
  eventId: number
  eventName?: string
  itemNo: string
  itemName: string
  trackName?: string
  majorDesc?: string
  teamType?: string
  openCond?: string
  deptName?: string
}

export interface EventLevelInfo {
  levelId?: number
  levelCode: string
  levelName: string
  levelIndex: number
}

export interface StuScoreRecord {
  scoreId?: number
  stuId: number
  eventId: number
  eventName?: string
  itemId: number
  itemName?: string
  levelId: number
  levelName?: string
  baseScore?: number
  levelIndex?: number
  finalScore?: number
  certDate?: string
  certPath?: string
  auditStatus?: number
  auditRemark?: string
  stuNo?: string
  stuName?: string
  className?: string
}

export interface ScoreSummary {
  stuId: number
  stuNo: string
  stuName: string
  className: string
  enrollYear: string
  trainLevel: string
  totalScore: number
  recordCount: number
}

export interface StudentScoreDetail {
  stuId: number
  stuNo: string
  stuName: string
  totalScore: number
  scoreList: StuScoreRecord[]
}
