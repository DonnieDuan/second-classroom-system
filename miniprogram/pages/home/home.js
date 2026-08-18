// pages/home/home.js
const { getMyTotalScore, getMyScores } = require('../../utils/api.js');
const { showLoading, hideLoading } = require('../../utils/util.js');
const app = getApp();

Page({
  data: {
    userInfo: {},
    totalScore: 0,
    scoreCount: 0
  },

  onShow() {
    this.loadUserData();
  },

  // 加载用户数据
  async loadUserData() {
    // 获取用户信息
    const userInfo = app.getUserInfo() || wx.getStorageSync('userInfo') || {};
    this.setData({ userInfo });

    if (!userInfo.id) return;

    showLoading('加载中...');
    try {
      // 并行请求总积分和成绩数量
      const [totalRes, scoresRes] = await Promise.all([
        getMyTotalScore(userInfo.id),
        getMyScores(userInfo.id)
      ]);

      this.setData({
        totalScore: totalRes.data || 0,
        scoreCount: (scoresRes.data && scoresRes.data.length) || 0
      });
    } catch (err) {
      console.error('加载数据失败:', err);
    } finally {
      hideLoading();
    }
  },

  // 跳转到我的成绩
  goScores() {
    wx.switchTab({ url: '/pages/scores/scores' });
  },

  // 跳转到成绩填报
  goSubmit() {
    wx.switchTab({ url: '/pages/submit/submit' });
  },

  // 跳转到赛事列表
  goEvents() {
    wx.switchTab({ url: '/pages/events/events' });
  },

  // 跳转到学习计划
  goPlan() {
    wx.navigateTo({ url: '/pages/plan/plan' });
  }
});