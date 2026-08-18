# -*- coding: utf-8 -*-
"""
LoginPage - 登录页面对象

封装登录页的元素定位与操作，测试用例只调用业务方法，
不直接接触 Playwright 的 page/locator，实现 UI 与测试逻辑解耦。
"""
from playwright.sync_api import Page
from base_page import BasePage


class LoginPage(BasePage):
    """登录页面 PO，封装登录页所有元素定位和业务操作"""

    # 元素定位器集中管理，便于前端 UI 变动后一处修改
    USERNAME_SELECTORS = [
        'input[placeholder*="账号"]',
        'input[placeholder*="用户名"]',
        'input[name="username"]',
        'input[type="text"]',
    ]
    PASSWORD_SELECTORS = [
        'input[placeholder*="密码"]',
        'input[name="password"]',
        'input[type="password"]',
    ]

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.path = "/#/login"

    def open_login_page(self):
        """打开登录页"""
        self.open(self.path)

    def _find_input(self, selectors: list) -> str:
        """从候选选择器中找到首个可见输入框的选择器"""
        for sel in selectors:
            if self.is_visible(sel):
                return sel
        return selectors[0]

    def input_username(self, username: str):
        """输入用户名"""
        sel = self._find_input(self.USERNAME_SELECTORS)
        self.input(sel, username)

    def input_password(self, password: str):
        """输入密码"""
        sel = self._find_input(self.PASSWORD_SELECTORS)
        self.input(sel, password)

    def click_login_button(self):
        """点击登录按钮"""
        btn = self.get_button_by_text("登录", "Login", "登 录")
        btn.click()
        self.page.wait_for_timeout(2000)

    def login_as(self, username: str, password: str):
        """业务方法：执行完整登录流程"""
        self.open_login_page()
        self.input_username(username)
        self.input_password(password)
        self.click_login_button()

    def has_username_input(self) -> bool:
        """检查用户名输入框是否存在"""
        return any(self.is_visible(sel) for sel in self.USERNAME_SELECTORS)

    def has_password_input(self) -> bool:
        """检查密码输入框是否存在"""
        return any(self.is_visible(sel) for sel in self.PASSWORD_SELECTORS)

    def get_input_count(self) -> int:
        """获取页面 input 元素总数（用于断言表单结构）"""
        return self.find_all("input").count()

    def get_button_count(self) -> int:
        """获取页面 button 元素总数"""
        return self.find_all("button").count()

    def page_has_login_keyword(self) -> bool:
        """页面内容是否包含登录相关关键字"""
        content = self.page.content()
        return "登录" in content or "管理" in content
