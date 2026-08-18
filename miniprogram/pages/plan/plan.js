// pages/plan/plan.js
const { getMyTotalScore, getMyScores } = require('../../utils/api.js');
const { showLoading, hideLoading } = require('../../utils/util.js');
const app = getApp();

Page({
  data: {
    completedCredits: 0,
    remainingCredits: 0,
    targetCredits: 60,
    progressPercent: 0,
    totalScore: 0,
    scoreCount: 0,
    passedCount: 0,
    pendingCount: 0,
    ongoingPlans: [],
    completedPlans: []
  },

  onLoad() {
    this.loadPlanData();
  },

  async loadPlanData() {
    const userInfo = app.getUserInfo() || wx.getStorageSync('userInfo');
    if (!userInfo || !userInfo.id) return;

    showLoading('加载中...');

    try {
      const [totalRes, scoresRes] = await Promise.all([
        getMyTotalScore(userInfo.id),
        getMyScores(userInfo.id)
      ]);

      const totalScore = totalRes.data || 0;
      const scores = scoresRes.data || [];

      // 统计数据
      const passedCount = scores.filter(s => s.auditStatus === 1).length;
      const pendingCount = scores.filter(s => s.auditStatus !== 1 && s.auditStatus !== 2).length;
      const completedCredits = totalScore;
      const targetCredits = this.data.targetCredits;
      const remainingCredits = Math.max(0, targetCredits - completedCredits);
      const progressPercent = Math.min(100, Math.round((completedCredits / targetCredits) * 100));

      this.setData({
        totalScore,
        scoreCount: scores.length,
        passedCount,
        pendingCount,
        completedCredits,
        remainingCredits,
        progressPercent,
        // 模拟计划数据，实际项目中从接口获取
        ongoingPlans: [
          { id: 1, name: '学科竞赛计划', description: '参加至少3次学科竞赛' },
          { id: 2, name: '志愿服务计划', description: '完成20小时志愿服务' }
        ],
        completedPlans: [
          { id: 3, name: '学术讲座计划', description: ' attend 5次学术讲座' }
        ]
      });
    } catch (err) {
      console.error('加载学习计划失败:', err);
    } finally {
      hideLoading();
    }
  },

  // 返回上一页
  goBack() {
    wx.navigateBack({ delta: 1 });
  }
});