# -*- coding: utf-8 -*-
"""
公共工具类
"""
import requests
from common.config import BACKEND_URL, REQUEST_TIMEOUT


class ApiClient:
    """API请求封装类"""
    
    def __init__(self):
        self.base_url = BACKEND_URL
        self.token = None
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "AutoTest/1.0"
        })
    
    def set_token(self, token):
        """设置认证Token"""
        self.token = token
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
    
    def _request(self, method, endpoint, **kwargs):
        """通用请求方法"""
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", REQUEST_TIMEOUT)
        
        try:
            response = self.session.request(method, url, **kwargs)
            return response
        except requests.exceptions.Timeout:
            raise AssertionError(f"请求超时: {method} {url}")
        except requests.exceptions.ConnectionError:
            raise AssertionError(f"连接失败: {method} {url} - 请检查服务是否启动")
    
    def get(self, endpoint, params=None, **kwargs):
        """GET请求"""
        return self._request("GET", endpoint, params=params, **kwargs)
    
    def post(self, endpoint, json=None, **kwargs):
        """POST请求"""
        return self._request("POST", endpoint, json=json, **kwargs)
    
    def put(self, endpoint, json=None, **kwargs):
        """PUT请求"""
        return self._request("PUT", endpoint, json=json, **kwargs)
    
    def delete(self, endpoint, **kwargs):
        """DELETE请求"""
        return self._request("DELETE", endpoint, **kwargs)


def assert_success(response, message=""):
    """断言接口返回成功"""
    assert response.status_code == 200, f"{message} HTTP状态码错误: {response.status_code}，响应内容: {response.text}"
    data = response.json()
    assert data.get("code") == 200 or data.get("code") == 0, f"{message} 业务状态码错误: {data.get('code')}，响应内容: {data.get('msg')}"
    return data


def assert_failed(response, expected_msg=None):
    """断言接口返回失败"""
    assert response.status_code == 200
    data = response.json()
    assert data.get("code") != 200 and data.get("code") != 0, f"预期失败但接口返回成功: {data}"
    if expected_msg:
        assert expected_msg in data.get("msg", ""), f"错误消息不匹配，预期包含: {expected_msg}，实际: {data.get('msg')}"
    return data
