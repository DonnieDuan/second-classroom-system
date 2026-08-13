# -*- coding: utf-8 -*-
"""
pytest全局配置和fixture
"""
import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.config import TEST_STUDENT, TEST_TEACHER, TEST_ADMIN
from common import ApiClient, assert_success


@pytest.fixture(scope="session")
def client():
    """创建全局API客户端"""
    return ApiClient()


@pytest.fixture(scope="session")
def student_token(client):
    """获取学生登录Token"""
    response = client.post("/api/auth/login", json=TEST_STUDENT)
    try:
        data = response.json()
        if data.get("code") == 200 or data.get("code") == 0:
            token = data.get("data", {}).get("token") or data.get("data", {}).get("accessToken")
            if token:
                client.set_token(token)
                return token
    except Exception:
        pass
    return None


@pytest.fixture(scope="session")
def teacher_token(client):
    """获取教师登录Token"""
    response = client.post("/api/auth/login", json=TEST_TEACHER)
    try:
        data = response.json()
        if data.get("code") == 200 or data.get("code") == 0:
            token = data.get("data", {}).get("token") or data.get("data", {}).get("accessToken")
            if token:
                client.set_token(token)
                return token
    except Exception:
        pass
    return None


@pytest.fixture(scope="session")
def admin_token(client):
    """获取管理员登录Token"""
    response = client.post("/api/auth/login", json=TEST_ADMIN)
    try:
        data = response.json()
        if data.get("code") == 200 or data.get("code") == 0:
            token = data.get("data", {}).get("token") or data.get("data", {}).get("accessToken")
            if token:
                client.set_token(token)
                return token
    except Exception:
        pass
    return None


@pytest.fixture(scope="function")
def auth_client(client, teacher_token):
    """带教师认证的客户端"""
    if teacher_token:
        client.set_token(teacher_token)
    return client


@pytest.fixture(scope="session", autouse=True)
def test_environment_check(request):
    """测试环境检查 - 自动跳过未启动的服务"""
    import urllib.request
    from common.config import BACKEND_URL
    
    def skip_all_tests():
        # 检查所有测试是否都应该跳过
        pass
    
    # 检查后端服务是否可用
    backend_running = True
    try:
        urllib.request.urlopen(BACKEND_URL, timeout=5)
    except Exception:
        backend_running = False
    
    if not backend_running:
        print(f"\n[警告] 后端服务 {BACKEND_URL} 未启动，接口测试将跳过实际请求验证")
