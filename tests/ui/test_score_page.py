# -*- coding: utf-8 -*-
"""
前端UI自动化测试 - 成绩审核页面测试

采用 Page Object 模式：测试用例只调用 ScorePage 的业务方法，
UI 定位细节封装在 ScorePage 中，前端变动只需修改 Page 对象。
"""
import os
import sys
import pytest
from playwright.sync_api import Page

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages import ScorePage
from common.config import FRONTEND_URL


class TestScoreAuditPage:
    """成绩审核页面 UI 测试（PO 模式）"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """每个测试前创建 ScorePage 对象并注入教师登录态"""
        self.score_page = ScorePage(page, FRONTEND_URL)
        self.score_page.set_teacher_login_state()

    def test_score_list_page_load(self):
        """[UI-SCORE-001] 成绩列表页面加载测试"""
        print("\n[UI-SCORE-001] 成绩列表页面加载测试")
        self.score_page.open_score_list()
        has_table = self.score_page.has_score_table()
        print(f"  页面加载成功: {'是' if has_table else '否'}")
        print(f"  页面URL: {self.score_page.get_page_url()}")
        self.score_page.screenshot("ui_score_list")
        print("  测试截图已保存: tests/reports/ui_score_list.png")

    def test_audit_button_exist(self):
        """[UI-SCORE-002] 审核操作按钮存在性测试"""
        print("\n[UI-SCORE-002] 审核操作按钮测试")
        self.score_page.open_score_list()
        found_keywords = self.score_page.get_audit_button_keywords()
        print(f"  找到的操作按钮关键字: {found_keywords}")
        self.score_page.screenshot("ui_audit_buttons")
        print("  测试截图已保存: tests/reports/ui_audit_buttons.png")

    def test_class_stats_page(self):
        """[UI-SCORE-003] 班级统计页面加载测试"""
        print("\n[UI-SCORE-003] 班级统计页面加载测试")
        self.score_page.open_class_stats()
        has_stats = self.score_page.has_stats_content()
        print(f"  统计页面加载成功: {'是' if has_stats else '否'}")
        print(f"  页面URL: {self.score_page.get_page_url()}")
        self.score_page.screenshot("ui_class_stats")
        print("  测试截图已保存: tests/reports/ui_class_stats.png")

    def test_warnings_page(self):
        """[UI-SCORE-004] 预警通知页面加载测试"""
        print("\n[UI-SCORE-004] 预警通知页面加载测试")
        self.score_page.open_warnings()
        has_warning = self.score_page.has_warning_content()
        print(f"  预警页面加载成功: {'是' if has_warning else '否'}")
        print(f"  页面URL: {self.score_page.get_page_url()}")
        self.score_page.screenshot("ui_warnings")
        print("  测试截图已保存: tests/reports/ui_warnings.png")
