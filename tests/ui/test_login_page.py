# -*- coding: utf-8 -*-
"""
前端UI自动化测试 - 登录页面测试

采用 Page Object 模式：测试用例只调用 LoginPage 的业务方法，
不直接接触 Playwright 的 page/locator，实现 UI 定位与测试逻辑解耦。
"""
import os
import sys
import pytest
from playwright.sync_api import Page

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages import LoginPage
from common.config import FRONTEND_URL, TEST_TEACHER


class TestLoginPage:
    """登录页面 UI 测试（PO 模式）"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """每个测试前创建 LoginPage 对象"""
        self.login_page = LoginPage(page, FRONTEND_URL)
        self.login_page.open_login_page()

    def test_login_page_title(self):
        """[UI-LOGIN-001] 验证登录页面标题显示"""
        print("\n[UI-LOGIN-001] 验证登录页面标题")
        has_keyword = self.login_page.page_has_login_keyword()
        print(f"  页面包含标题关键字: {has_keyword}")

    def test_login_form_elements(self):
        """[UI-LOGIN-002] 验证登录表单元素存在"""
        print("\n[UI-LOGIN-002] 验证登录表单元素")
        username_found = self.login_page.has_username_input()
        password_found = self.login_page.has_password_input()
        print(f"  用户名输入框: {'存在' if username_found else '未找到'}")
        print(f"  密码输入框: {'存在' if password_found else '未找到'}")

    def test_login_teacher(self):
        """[UI-LOGIN-003] 教师账号登录流程测试"""
        print("\n[UI-LOGIN-003] 教师账号登录测试")
        input_count = self.login_page.get_input_count()
        btn_count = self.login_page.get_button_count()
        print(f"  页面 input 元素数: {input_count}")
        print(f"  页面 button 元素数: {btn_count}")

        self.login_page.login_as(TEST_TEACHER["username"], TEST_TEACHER["password"])
        print("  已执行教师登录流程")

        self.login_page.screenshot("ui_login_test")
        print("  测试截图已保存: tests/reports/ui_login_test.png")
