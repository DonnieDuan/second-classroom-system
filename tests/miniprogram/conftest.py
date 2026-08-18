# -*- coding: utf-8 -*-
"""
微信小程序自动化测试 - pytest 配置
使用 miniprogram-automator 框架实现小程序 UI 自动化测试
同时支持通过 requests 模拟小程序端 API 调用进行接口测试
"""
import os
import sys
import pytest

# 将当前目录和上级目录加入路径，以便导入公共模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# ==================== 路径配置 ====================
# 微信开发者工具路径
WX_DEVTOOLS_PATH = os.getenv(
    'WX_DEVTOOLS_PATH',
    r'C:\Program Files (x86)\Tencent\微信web开发者工具'
)

# 小程序项目路径
MINIPROGRAM_PATH = os.getenv(
    'MINIPROGRAM_PATH',
    r'd:\java\1\miniprogram'
)

# 后端服务基础地址（context-path 为 /second-class）
BACKEND_URL = os.getenv(
    'BACKEND_URL',
    'http://localhost:8080/second-class'
)

# 后端 API 完整地址
BACKEND_API_URL = f'{BACKEND_URL}/api'

# 测试账号
TEST_STUDENT = {
    'username': '20231012023',
    'password': '123456'
}

# 请求超时时间（秒）
REQUEST_TIMEOUT = 30


@pytest.fixture(scope="session")
def backend_available():
    """检查后端服务是否可用"""
    import urllib.request
    import urllib.error
    try:
        urllib.request.urlopen(BACKEND_URL, timeout=5)
        return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def api_client():
    """创建 API 客户端实例，模拟小程序端 HTTP 请求"""
    import requests
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json;charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36 MicroMessenger/8.0.0',
        'Referer': 'https://servicewechat.com/',
        'X-Requested-With': 'XMLHttpRequest'
    })
    return session


@pytest.fixture(scope="session")
def mini_program(backend_available):
    """启动微信小程序并获取 automator 实例

    当 miniprogram-automator 不可用或后端未启动时，
    返回 None，测试用例应检查并跳过。
    """
    if not backend_available:
        print("\n[警告] 后端服务未启动，小程序 UI 自动化测试不可用")
        yield None
        return

    try:
        from miniprogram_automator import automator
        print("\n[信息] miniprogram-automator 已加载")
        yield None
    except ImportError:
        print("\n[警告] miniprogram-automator 未安装，UI 自动化测试不可用")
        print("  安装命令: npm install miniprogram-automator")
        yield None


@pytest.fixture(scope="session")
def student_token(api_client, backend_available):
    """学生登录并获取 Token"""
    if not backend_available:
        return None

    try:
        url = f'{BACKEND_API_URL}/auth/login'
        payload = {
            'username': TEST_STUDENT['username'],
            'password': TEST_STUDENT['password'],
            'role': 'student'
        }
        resp = api_client.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        data = resp.json()

        if data.get('code') in (200, 0):
            result_data = data.get('data', {})
            token = result_data.get('token') or result_data.get('accessToken')
            if token:
                print(f"\n[信息] 学生登录成功，token 获取成功")
                return token
        print(f"\n[警告] 学生登录失败: {data.get('msg', '未知错误')}")
        return None
    except Exception as e:
        print(f"\n[警告] 学生登录异常: {e}")
        return None


@pytest.fixture(scope="session")
def student_user_info(api_client, student_token, backend_available):
    """获取学生用户信息"""
    if not backend_available or not student_token:
        return None

    try:
        url = f'{BACKEND_API_URL}/auth/login'
        payload = {
            'username': TEST_STUDENT['username'],
            'password': TEST_STUDENT['password'],
            'role': 'student'
        }
        api_client.headers.update({'Authorization': f'Bearer {student_token}'})
        resp = api_client.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        data = resp.json()

        if data.get('code') in (200, 0):
            result_data = data.get('data', {})
            user_info = result_data.get('userInfo') or {}
            return user_info
        return None
    except Exception:
        return None


@pytest.fixture(autouse=True)
def skip_if_backend_not_available(request, backend_available):
    """后端不可用时自动跳过所有测试（Mock 单元测试除外）"""
    if 'mock' in request.node.nodeid.lower():
        return
    if not backend_available:
        pytest.skip(f'后端服务 {BACKEND_URL} 未启动，跳过测试')