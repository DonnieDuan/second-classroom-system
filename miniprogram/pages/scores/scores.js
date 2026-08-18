// pages/scores/scores.js
const { getMyScores, getMyTotalScore } = require('../../utils/api.js');
const { showLoading, hideLoading, showError } = require('../../utils/util.js');
const app = getApp();

Page({
  data: {
    scores: [],
    totalScore: 0,
    loading: false,
    page: 1,
    total: 0
  },

  onShow() {
    this.loadScores();
  },

  // 加载成绩列表
  async loadScores() {
    const userInfo = app.getUserInfo() || wx.getStorageSync('userInfo');
    if (!userInfo || !userInfo.id) {
      showError('请先登录');
      return;
    }

    this.setData({ loading: true });
    showLoading('加载中...');

    try {
      // 并行获取成绩列表和总积分
      const [scoresRes, totalRes] = await Promise.all([
        getMyScores(userInfo.id),
        getMyTotalScore(userInfo.id)
      ]);

      const scores = scoresRes.data || [];
      this.setData({
        scores,
        totalScore: totalRes.data || 0,
        total: scores.length
      });
    } catch (err) {
      showError(err.message || '加载失败');
    } finally {
      this.setData({ loading: false });
      hideLoading();
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.setData({ page: 1 });
    this.loadScores().then(() => {
      wx.stopPullDownRefresh();
    });
  },

  // 上拉加载更多
  onReachBottom() {
    // 当前为模拟分页，实际项目中可根据后端分页接口实现
    if (this.data.scores.length < this.data.total) {
      this.loadMore();
    }
  },

  async loadMore() {
    const nextPage = this.data.page + 1;
    this.setData({ page: nextPage });
    // 实际项目中调用分页接口
    // const res = await getMyScores(userInfo.id, nextPage);
    // this.setData({ scores: [...this.data.scores, ...res.data] });
  },

  // 跳转到填报页
  goSubmit() {
    wx.switchTab({ url: '/pages/submit/submit' });
  },

  // 点击成绩详情
  goDetail(e) {
    const id = e.currentTarget.dataset.id;
    // 可以跳转到详情页，此处暂时提示
    wx.showToast({ title: '成绩ID: ' + id, icon: 'none' });
  }
});