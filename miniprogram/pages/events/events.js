// pages/events/events.js
const { getAllEvents } = require('../../utils/api.js');
const { showLoading, hideLoading, showError } = require('../../utils/util.js');

Page({
  data: {
    events: [],
    filteredEvents: [],
    keyword: '',
    loading: false
  },

  onShow() {
    this.loadEvents();
  },

  // 加载赛事列表
  async loadEvents() {
    this.setData({ loading: true });
    showLoading('加载中...');

    try {
      const res = await getAllEvents();
      const events = res.data || [];
      this.setData({
        events,
        filteredEvents: this.filterEvents(events, this.data.keyword)
      });
    } catch (err) {
      showError(err.message || '加载失败');
    } finally {
      this.setData({ loading: false });
      hideLoading();
    }
  },

  // 搜索过滤
  onSearch(e) {
    const keyword = e.detail.value;
    this.setData({
      keyword,
      filteredEvents: this.filterEvents(this.data.events, keyword)
    });
  },

  // 根据关键词过滤赛事
  filterEvents(events, keyword) {
    if (!keyword) return events;
    const lower = keyword.toLowerCase();
    return events.filter(item =>
      (item.name || '').toLowerCase().includes(lower)
    );
  },

  // 点击赛事跳转到填报页
  goSubmit(e) {
    const id = e.currentTarget.dataset.id;
    wx.switchTab({
      url: '/pages/submit/submit',
      success: () => {
        // 通过全局数据传递选中的赛事ID
        const app = getApp();
        app.globalData.selectedEventId = id;
      }
    });
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadEvents().then(() => {
      wx.stopPullDownRefresh();
    });
  }
});