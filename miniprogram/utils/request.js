// utils/request.js - 统一的网络请求封装
const app = getApp();

// 基础配置
const BASE_URL = 'http://localhost:8080/second-class/api';
const TIMEOUT = 10000;

/**
 * 发送 HTTP 请求
 * @param {Object} options - 请求配置
 * @param {string} options.url - 请求路径
 * @param {string} options.method - 请求方法 (GET/POST)
 * @param {Object} options.data - 请求体
 * @param {Object} options.params - URL 查询参数
 * @returns {Promise<Object>} 接口返回的 ApiResult 对象
 */
function request(options) {
  return new Promise((resolve, reject) => {
    const token = wx.getStorageSync('token');
    const header = {
      'Content-Type': 'application/json;charset=utf-8'
    };
    if (token) {
      header['Authorization'] = `Bearer ${token}`;
    }

    let url = BASE_URL + options.url;
    // 拼接查询参数
    if (options.params) {
      const query = Object.keys(options.params)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(options.params[key])}`)
        .join('&');
      url += (url.includes('?') ? '&' : '?') + query;
    }

    wx.request({
      url: url,
      method: options.method || 'GET',
      data: options.data,
      header: header,
      timeout: TIMEOUT,
      success(res) {
        if (res.statusCode === 200) {
          const result = res.data;
          if (result.code === 200 || result.code === 0) {
            resolve(result);
          } else if (result.code === 401) {
            // 未授权，清除登录状态并跳转登录页
            wx.removeStorageSync('token');
            wx.removeStorageSync('userInfo');
            wx.reLaunch({ url: '/pages/login/login' });
            reject(new Error('登录已过期，请重新登录'));
          } else {
            reject(new Error(result.msg || '请求失败'));
          }
        } else {
          reject(new Error(`HTTP ${res.statusCode}`));
        }
      },
      fail(err) {
        reject(new Error('网络连接失败，请检查后端服务'));
      }
    });
  });
}

// GET 请求快捷方法
function get(url, params) {
  return request({ url, method: 'GET', params });
}

// POST 请求快捷方法
function post(url, data) {
  return request({ url, method: 'POST', data });
}

// PUT 请求快捷方法
function put(url, data) {
  return request({ url, method: 'PUT', data });
}

// DELETE 请求快捷方法
function del(url, params) {
  return request({ url, method: 'DELETE', params });
}

module.exports = {
  request,
  get,
  post,
  put,
  del,
  BASE_URL
};
