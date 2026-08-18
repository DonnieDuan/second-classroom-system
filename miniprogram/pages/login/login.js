// pages/login/login.js
const { wxLogin } = require('../../utils/api.js');
const app = getApp();

Page({
  data: {
    loading: false,
    errorMsg: '',
    stuNo: ''
  },

  onLoad() {
    const token = wx.getStorageSync('token');
    if (token) {
      wx.reLaunch({ url: '/pages/home/home' });
    }
  },

  onStuNoInput(e) {
    this.setData({ stuNo: e.detail.value });
  },

  // 微信一键登录
  async onWxLogin() {
    this.setData({ loading: true, errorMsg: '' });

    try {
      // 1. 调用 wx.login 获取 code
      const loginRes = await new Promise((resolve, reject) => {
        wx.login({
          success: resolve,
          fail: reject
        });
      });

      if (!loginRes.code) {
        throw new Error('微信登录失败，未获取到 code');
      }

      // 2. 发送 code + 学号 到后端换取 token
      const res = await wxLogin({
        code: loginRes.code,
        stuNo: this.data.stuNo || ''
      });

      // 3. 保存登录状态
      app.saveLoginState(res.data.token, res.data);
      wx.showToast({ title: '登录成功', icon: 'success' });

      setTimeout(() => {
        wx.reLaunch({ url: '/pages/home/home' });
      }, 800);
    } catch (err) {
      this.setData({ errorMsg: err.message || '登录失败，请重试' });
      wx.showToast({ title: err.message || '登录失败', icon: 'none' });
    } finally {
      this.setData({ loading: false });
    }
  },

  // 账号密码登录（保留作备选）
  onAccountLogin() {
    wx.showModal({
      title: '账号登录',
      editable: true,
      placeholderText: '请输入学号',
      success: (res) => {
        if (res.confirm && res.content) {
          const stuNo = res.content.trim();
          const passwordPrompt = wx.showModal({
            title: '输入密码',
            editable: true,
            placeholderText: '请输入密码',
            success: (res2) => {
              if (res2.confirm && res2.content) {
                this.doAccountLogin(stuNo, res2.content);
              }
            }
          });
        }
      }
    });
  },

  async doAccountLogin(username, password) {
    this.setData({ loading: true, errorMsg: '' });
    try {
      const res = await wx.request({
        url: app.globalData.baseUrl + '/auth/login',
        method: 'POST',
        data: { username, password, role: 'student' }
      });
      if (res.data.code === 200) {
        app.saveLoginState(res.data.data.token, res.data.data);
        wx.reLaunch({ url: '/pages/home/home' });
      } else {
        this.setData({ errorMsg: res.data.msg });
      }
    } catch (err) {
      this.setData({ errorMsg: '网络错误，请重试' });
    } finally {
      this.setData({ loading: false });
    }
  }
});
