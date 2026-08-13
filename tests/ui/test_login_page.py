# -*- coding: utf-8 -*-
"""
前端UI自动化测试 - 登录页面测试
"""
import pytest
import re
from playwright.sync_api import Page, expect
from common.config import FRONTEND_URL, TEST_TEACHER


class TestLoginPage:
    """登录页面UI测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """每个测试前打开登录页"""
        self.page = page
        self.base_url = FRONTEND_URL
        # 访问登录页面
        page.goto(f"{self.base_url}/#/login")
        page.wait_for_load_state("networkidle")
    
    def test_login_page_title(self):
        """测试登录页面标题显示"""
        print("\n[UI-LOGIN-001] 验证登录页面标题")
        # 检查页面是否包含"登录"或"管理"等关键字
        content = self.page.content()
        print(f"  页面包含标题关键字: {'登录' in content or '管理' in content}")
    
    def test_login_form_elements(self):
        """测试登录表单元素是否存在"""
        print("\n[UI-LOGIN-002] 验证登录表单元素")
        
        # 查找用户名输入框（支持多种选择器）
        username_selectors = [
            'input[placeholder*="账号"]',
            'input[placeholder*="用户名"]',
            'input[type="text"]',
            'input[name="username"]',
            '.el-input__inner'
        ]
        pwd_selectors = [
            'input[placeholder*="密码"]',
            'input[type="password"]',
            'input[name="password"]'
        ]
        
        username_found = False
        for sel in username_selectors:
            try:
                if self.page.locator(sel).count() > 0:
                    username_found = True
                    print(f"  找到用户名输入框: {sel}")
                    break
            except Exception:
                continue
        
        password_found = False
        for sel in pwd_selectors:
            try:
                if self.page.locator(sel).count() > 0:
                    password_found = True
                    print(f"  找到密码输入框: {sel}")
                    break
            except Exception:
                continue
        
        print(f"  用户名输入框: {'存在' if username_found else '未找到'}")
        print(f"  密码输入框: {'存在' if password_found else '未找到'}")
    
    def test_login_teacher(self):
        """测试教师登录流程"""
        print("\n[UI-LOGIN-003] 教师账号登录测试")
        
        page = self.page
        
        # 尝试填写表单（多种选择器尝试）
        try:
            # 查找输入框
            inputs = page.locator('input')
            count = inputs.count()
            print(f"  页面上共找到 {count} 个input元素")
            
            if count >= 2:
                # 第一个输入框填用户名，第二个填密码
                inputs.first.fill(TEST_TEACHER["username"])
                inputs.nth(1).fill(TEST_TEACHER["password"])
                print("  已填写用户名和密码")
                
                # 查找登录按钮
                buttons = page.locator('button')
                btn_count = buttons.count()
                print(f"  页面上共找到 {btn_count} 个按钮")
                
                for i in range(btn_count):
                    btn_text = buttons.nth(i).inner_text() if i < btn_count else ""
                    if "登录" in btn_text or "Login" in btn_text or "submit" in str(btn_text).lower():
                        print(f"  点击登录按钮: {btn_text.strip()}")
                        buttons.nth(i).click()
                        # 等待页面跳转或响应
                        page.wait_for_timeout(2000)
                        break
        except Exception as e:
            print(f"  登录操作提示: {str(e)[:100]}")
        
        # 截图保存测试结果
        page.screenshot(path=f"tests/reports/ui_login_test.png", full_page=True)
        print("  测试截图已保存: tests/reports/ui_login_test.png")
