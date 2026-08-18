// utils/util.js - 通用工具函数

/**
 * 格式化日期为 YYYY-MM-DD
 */
function formatDate(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * 格式化日期时间为 YYYY-MM-DD HH:mm:ss
 */
function formatDateTime(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hour = String(d.getHours()).padStart(2, '0');
  const minute = String(d.getMinutes()).padStart(2, '0');
  const second = String(d.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}

/**
 * 获取审核状态文字
 */
function getAuditStatusText(status) {
  const map = {
    0: '待审核',
    1: '已通过',
    2: '已拒绝',
    null: '待审核'
  };
  return map[status] || '未知';
}

/**
 * 获取审核状态样式类名
 */
function getAuditStatusClass(status) {
  if (status === 1) return 'tag tag-success';
  if (status === 2) return 'tag tag-danger';
  return 'tag tag-warning';
}

/**
 * 显示加载提示
 */
function showLoading(title = '加载中...') {
  wx.showLoading({ title, mask: true });
}

/**
 * 隐藏加载提示
 */
function hideLoading() {
  wx.hideLoading();
}

/**
 * 显示成功提示
 */
function showSuccess(title = '操作成功') {
  wx.showToast({ title, icon: 'success', duration: 2000 });
}

/**
 * 显示错误提示
 */
function showError(title = '操作失败') {
  wx.showToast({ title, icon: 'none', duration: 2000 });
}

module.exports = {
  formatDate,
  formatDateTime,
  getAuditStatusText,
  getAuditStatusClass,
  showLoading,
  hideLoading,
  showSuccess,
  showError
};
