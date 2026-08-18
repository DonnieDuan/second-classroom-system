// utils/api.js - 接口封装层，对接 Spring Boot 后端
const { get, post } = require('./request.js');

// ==================== 用户认证 ====================

/**
 * 学生账号密码登录
 * @param {Object} data - { username, password }
 * @returns {Promise} 登录响应
 */
function studentLogin(data) {
  return post('/auth/login', {
    username: data.username,
    password: data.password,
    role: 'student'
  });
}

/**
 * 微信小程序一键登录
 * @param {Object} data - { code, stuNo }
 * @returns {Promise} 登录响应
 */
function wxLogin(data) {
  return post('/auth/wx-login', {
    code: data.code,
    stuNo: data.stuNo || ''
  });
}

// ==================== 成绩管理 ====================

/**
 * 获取学生我的成绩列表
 * @param {number} stuId - 学生ID
 */
function getMyScores(stuId) {
  return get(`/app/score/my/${stuId}`);
}

/**
 * 获取学生总积分
 * @param {number} stuId - 学生ID
 */
function getMyTotalScore(stuId) {
  return get(`/app/score/total/${stuId}`);
}

/**
 * 提交成绩
 * @param {Object} form - 成绩表单数据
 */
function submitScore(form) {
  return post('/app/score/submit', form);
}

// ==================== 赛事管理 ====================

/**
 * 获取所有赛事列表
 */
function getAllEvents() {
  return get('/event/all');
}

/**
 * 根据赛事ID获取赛项列表
 * @param {number} eventId - 赛事ID
 */
function getItemsByEvent(eventId) {
  return get(`/item/event/${eventId}`);
}

/**
 * 获取所有获奖级别
 */
function getAllLevels() {
  return get('/level/all');
}

module.exports = {
  studentLogin,
  wxLogin,
  getMyScores,
  getMyTotalScore,
  submitScore,
  getAllEvents,
  getItemsByEvent,
  getAllLevels
};
