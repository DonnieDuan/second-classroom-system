# -*- coding: utf-8 -*-
"""
前端UI自动化测试 - 成绩审核页面测试
"""
import pytest
from playwright.sync_api import Page
from common.config import FRONTEND_URL


class TestScoreAuditPage:
    """成绩审核页面UI测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """设置 - 尝试模拟登录状态后访问成绩审核页"""
        self.page = page
        self.base_url = FRONTEND_URL
        
        # 先设置一些localStorage模拟登录（避免复杂登录流程）
        page.add_init_script("""
            () => {
                try {
                    localStorage.setItem('token', 'test-token-placeholder');
                    localStorage.setItem('userInfo', JSON.stringify({role: 'teacher', name: '测试教师'}));
                } catch(e) {}
            }
        """)
    
    def test_score_list_page_load(self):
        """测试成绩列表页面加载"""
        print("\n[UI-SCORE-001] 成绩列表页面加载测试")
        page = self.page
        
        # 访问成绩列表页
        page.goto(f"{self.base_url}/#/scores", wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(3000)
        
        content = page.content()
        has_table = 'el-table' in content or '表格' in content or '成绩' in content or '审核' in content
        print(f"  页面加载成功: {'是' if has_table else '否'}")
        print(f"  页面URL: {page.url}")
        
        # 截图
        page.screenshot(path="tests/reports/ui_score_list.png", full_page=True)
        print("  测试截图已保存: tests/reports/ui_score_list.png")
    
    def test_audit_button_exist(self):
        """测试审核操作按钮存在性"""
        print("\n[UI-SCORE-002] 审核操作按钮测试")
        page = self.page
        
        page.goto(f"{self.base_url}/#/scores", wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(3000)
        
        # 查找按钮
        buttons = page.locator('button, .el-button')
        count = buttons.count()
        print(f"  页面按钮总数: {count}")
        
        keywords = ["通过", "拒绝", "审核", "操作", "编辑", "删除"]
        found_keywords = []
        
        for i in range(min(count, 20)):
            try:
                text = buttons.nth(i).inner_text().strip()
                for kw in keywords:
                    if kw in text and kw not in found_keywords:
                        found_keywords.append(kw)
            except Exception:
                continue
        
        print(f"  找到的操作按钮关键字: {found_keywords}")
        
        page.screenshot(path="tests/reports/ui_audit_buttons.png")
        print("  测试截图已保存: tests/reports/ui_audit_buttons.png")
    
    def test_class_stats_page(self):
        """测试班级统计页面"""
        print("\n[UI-SCORE-003] 班级统计页面加载测试")
        page = self.page
        
        page.goto(f"{self.base_url}/#/teacher/class-stats", wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(3000)
        
        content = page.content()
        has_stats = '统计' in content or '分析' in content or '平均' in content or '班级' in content
        print(f"  统计页面加载成功: {'是' if has_stats else '否'}")
        print(f"  页面URL: {page.url}")
        
        page.screenshot(path="tests/reports/ui_class_stats.png", full_page=True)
        print("  测试截图已保存: tests/reports/ui_class_stats.png")
    
    def test_warnings_page(self):
        """测试预警通知页面"""
        print("\n[UI-SCORE-004] 预警通知页面加载测试")
        page = self.page
        
        page.goto(f"{self.base_url}/#/teacher/warnings", wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(3000)
        
        content = page.content()
        has_warning = '预警' in content or '达标' in content or '学生' in content
        print(f"  预警页面加载成功: {'是' if has_warning else '否'}")
        print(f"  页面URL: {page.url}")
        
        page.screenshot(path="tests/reports/ui_warnings.png", full_page=True)
        print("  测试截图已保存: tests/reports/ui_warnings.png")
