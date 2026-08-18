// pages/submit/submit.js
const {
  getAllEvents,
  getItemsByEvent,
  getAllLevels,
  submitScore
} = require('../../utils/api.js');
const {
  showLoading,
  hideLoading,
  showSuccess,
  showError
} = require('../../utils/util.js');
const app = getApp();

Page({
  data: {
    events: [],
    items: [],
    levels: [],
    selectedEventIndex: null,
    selectedItemIndex: null,
    selectedLevelIndex: null,
    certDate: '',
    certPath: '',
    submitting: false
  },

  onLoad() {
    this.loadFormData();
  },

  // 加载表单所需的基础数据
  async loadFormData() {
    showLoading('加载中...');
    try {
      const [eventsRes, levelsRes] = await Promise.all([
        getAllEvents(),
        getAllLevels()
      ]);
      this.setData({
        events: eventsRes.data || [],
        levels: levelsRes.data || []
      });
    } catch (err) {
      showError(err.message || '加载数据失败');
    } finally {
      hideLoading();
    }
  },

  // 选择赛事
  async onEventChange(e) {
    const index = e.detail.value;
    const event = this.data.events[index];
    this.setData({
      selectedEventIndex: index,
      selectedItemIndex: null,
      items: []
    });

    // 加载该赛事下的赛项
    if (event && event.id) {
      try {
        const res = await getItemsByEvent(event.id);
        this.setData({ items: res.data || [] });
      } catch (err) {
        showError(err.message || '加载赛项失败');
      }
    }
  },

  // 选择赛项
  onItemChange(e) {
    this.setData({ selectedItemIndex: e.detail.value });
  },

  // 选择级别
  onLevelChange(e) {
    this.setData({ selectedLevelIndex: e.detail.value });
  },

  // 选择日期
  onDateChange(e) {
    this.setData({ certDate: e.detail.value });
  },

  // 选择图片
  chooseImage() {
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        this.setData({ certPath: res.tempFilePaths[0] });
      }
    });
  },

  // 提交成绩
  async onSubmit() {
    const {
      events,
      items,
      levels,
      selectedEventIndex,
      selectedItemIndex,
      selectedLevelIndex,
      certDate,
      certPath
    } = this.data;

    // 表单校验
    if (selectedEventIndex === null) {
      showError('请选择赛事');
      return;
    }
    if (selectedItemIndex === null) {
      showError('请选择赛项');
      return;
    }
    if (selectedLevelIndex === null) {
      showError('请选择获奖级别');
      return;
    }
    if (!certDate) {
      showError('请选择获奖日期');
      return;
    }

    const userInfo = app.getUserInfo() || wx.getStorageSync('userInfo');

    const formData = {
      stuId: userInfo.id,
      eventId: events[selectedEventIndex].id,
      itemId: items[selectedItemIndex].id,
      levelId: levels[selectedLevelIndex].id,
      certDate,
      certPath
    };

    this.setData({ submitting: true });
    showLoading('提交中...');

    try {
      await submitScore(formData);
      showSuccess('提交成功，等待审核');
      // 重置表单
      this.setData({
        selectedEventIndex: null,
        selectedItemIndex: null,
        selectedLevelIndex: null,
        certDate: '',
        certPath: ''
      });
      // 跳转到成绩列表
      setTimeout(() => {
        wx.switchTab({ url: '/pages/scores/scores' });
      }, 1500);
    } catch (err) {
      showError(err.message || '提交失败');
    } finally {
      this.setData({ submitting: false });
      hideLoading();
    }
  }
});