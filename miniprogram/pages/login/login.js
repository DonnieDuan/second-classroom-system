// pages/login/login.js
const { studentLogin } = require('../../utils/api.js');
const { showLoading, hideLoading, showError } = require('../../utils/util.js');
const app = getApp();

Page({
  data: {
    username: '',
    password: '',
    loading: false,
    errorMsg: ''
  },

  onLoad() {
    // 检查是否已登录，已登录则跳转首页
    const token = wx.getStorageSync('token');
    if (token) {
      wx.reLaunch({ url: '/pages/home/home' });
    }
  },

  onUsernameInput(e) {
    this.setData({ username: e.detail.value });
  },

  onPasswordInput(e) {
    this.setData({ password: e.detail.value });
  },

  // 执行登录
  async doLogin() {
    const { username, password } = this.data;

    // 表单校验
    if (!username.trim()) {
      this.setData({ errorMsg: '请输入学号' });
      return;
    }
    if (!password.trim()) {
      this.setData({ errorMsg: '请输入密码' });
      return;
    }

    this.setData({ loading: true, errorMsg: '' });
    showLoading('登录中...');

    try {
      const res = await studentLogin({ username, password });
      // 保存登录状态
      app.saveLoginState(res.data.token, res.data.userInfo);
      showSuccess('登录成功');
      // 登录成功后跳转首页
      setTimeout(() => {
        wx.reLaunch({ url: '/pages/home/home' });
      }, 800);
    } catch (err) {
      this.setData({ errorMsg: err.message || '登录失败，请检查学号和密码' });
      showError(err.message || '登录失败');
    } finally {
      this.setData({ loading: false });
      hideLoading();
    }
  }
});