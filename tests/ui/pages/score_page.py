# -*- coding: utf-8 -*-
"""
ScorePage - 成绩审核页面对象

封装教师端成绩审核、班级统计、预警通知等页面的元素定位与操作。
继承 BasePage，复用通用交互方法，测试用例只调用业务方法。
"""
from playwright.sync_api import Page
from base_page import BasePage


class ScorePage(BasePage):
    """成绩审核相关页面 PO"""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

    def open_score_list(self):
        """打开成绩列表页"""
        self.open("/#/scores")
        self.page.wait_for_timeout(2000)

    def open_class_stats(self):
        """打开班级统计页"""
        self.open("/#/teacher/class-stats")
        self.page.wait_for_timeout(2000)

    def open_warnings(self):
        """打开预警通知页"""
        self.open("/#/teacher/warnings")
        self.page.wait_for_timeout(2000)

    def set_teacher_login_state(self):
        """模拟教师登录态（通过 localStorage 注入 token）"""
        self.page.add_init_script("""
            () => {
                try {
                    localStorage.setItem('token', 'test-token-placeholder');
                    localStorage.setItem('userInfo', JSON.stringify({role: 'teacher', name: '测试教师'}));
                } catch(e) {}
            }
        """)

    def has_score_table(self) -> bool:
        """检查成绩表格是否存在"""
        content = self.page.content()
        return any(kw in content for kw in ["el-table", "表格", "成绩", "审核"])

    def get_audit_button_keywords(self) -> list:
        """查找审核操作按钮的关键字"""
        buttons = self.find_all("button, .el-button")
        count = buttons.count()
        keywords = ["通过", "拒绝", "审核", "操作", "编辑", "删除"]
        found = []
        for i in range(min(count, 20)):
            try:
                text = buttons.nth(i).inner_text().strip()
                for kw in keywords:
                    if kw in text and kw not in found:
                        found.append(kw)
            except Exception:
                continue
        return found

    def has_stats_content(self) -> bool:
        """检查统计页面是否加载"""
        content = self.page.content()
        return any(kw in content for kw in ["统计", "分析", "平均", "班级"])

    def has_warning_content(self) -> bool:
        """检查预警页面是否加载"""
        content = self.page.content()
        return any(kw in content for kw in ["预警", "达标", "学生"])

    def get_page_url(self) -> str:
        """获取当前页面 URL"""
        return self.page.url
