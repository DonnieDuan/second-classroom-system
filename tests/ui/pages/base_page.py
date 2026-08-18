# -*- coding: utf-8 -*-
"""
BasePage - 页面对象基类

PO 模式核心：将页面交互细节封装在 Page 对象中，测试用例只调用业务方法。
所有具体页面对象（LoginPage / ScorePage 等）继承此类，复用通用操作。
"""
import os
from playwright.sync_api import Page, expect, Locator


class BasePage:
    """所有页面对象的基类，封装 Playwright 通用操作"""

    def __init__(self, page: Page, base_url: str = ""):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str = ""):
        """打开页面，path 为相对路径（如 /#/login）"""
        url = f"{self.base_url}{path}" if path else self.base_url
        self.page.goto(url, wait_until="domcontentloaded", timeout=15000)
        self.page.wait_for_load_state("networkidle")

    def find(self, selector: str) -> Locator:
        """根据 CSS 选择器查找单个元素"""
        return self.page.locator(selector)

    def find_all(self, selector: str) -> Locator:
        """查找匹配某选择器的全部元素"""
        return self.page.locator(selector)

    def input(self, selector: str, text: str):
        """向输入框填入文本"""
        el = self.find(selector)
        el.wait_for(state="visible", timeout=5000)
        el.fill(text)

    def click(self, selector: str):
        """点击元素"""
        el = self.find(selector)
        el.wait_for(state="visible", timeout=5000)
        el.click()

    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        el = self.find(selector)
        el.wait_for(state="visible", timeout=5000)
        return el.inner_text()

    def is_visible(self, selector: str) -> bool:
        """判断元素是否可见"""
        try:
            return self.find(selector).is_visible(timeout=3000)
        except Exception:
            return False

    def wait_for(self, selector: str, timeout: int = 5000):
        """等待元素出现"""
        self.find(selector).wait_for(state="visible", timeout=timeout)

    def screenshot(self, name: str = "screenshot"):
        """截图并保存到 reports 目录"""
        reports_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "..", "reports"
        )
        os.makedirs(reports_dir, exist_ok=True)
        path = os.path.join(reports_dir, f"{name}.png")
        self.page.screenshot(path=path, full_page=True)
        return path

    def get_button_by_text(self, *keywords: str) -> Locator:
        """根据按钮文本关键字查找按钮，支持多关键字匹配"""
        buttons = self.find_all("button, .el-button")
        count = buttons.count()
        for i in range(count):
            try:
                text = buttons.nth(i).inner_text().strip()
                for kw in keywords:
                    if kw in text:
                        return buttons.nth(i)
            except Exception:
                continue
        return self.page.locator(".__not_found__")
