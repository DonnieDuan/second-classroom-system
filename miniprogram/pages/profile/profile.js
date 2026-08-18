// pages/profile/profile.js
const app = getApp();

Page({
  data: {
    userInfo: {}
  },

  onShow() {
    this.loadUserInfo();
  },

  // 加载用户信息
  loadUserInfo() {
    const userInfo = app.getUserInfo() || wx.getStorageSync('userInfo') || {};
    this.setData({ userInfo });
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
  },

  // 跳转到设置
  goSettings() {
    wx.showToast({ title: '设置页面开发中', icon: 'none' });
  },

  // 退出登录
  doLogout() {
    wx.showModal({
      title: '提示',
      content: '确定要退出登录吗？',
      confirmColor: '#409EFF',
      success: (res) => {
        if (res.confirm) {
          app.clearLoginState();
          wx.showToast({ title: '已退出登录', icon: 'success' });
          setTimeout(() => {
            wx.reLaunch({ url: '/pages/login/login' });
          }, 800);
        }
      }
    });
  }
});