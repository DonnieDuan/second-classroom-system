"""
学生第二课堂系统 - 关键页面截图脚本
截图保存到 docs/screenshots/ 目录
"""
import os
import time
from playwright.sync_api import sync_playwright

FRONTEND_URL = "http://localhost:5173"
SCREENSHOT_DIR = r"d:\java\1\docs\screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def save(page, name: str):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    page.screenshot(path=path, full_page=True)
    size_kb = os.path.getsize(path) // 1024
    print(f"  📸 {name}.png  ({size_kb} KB)")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1.25,
        )
        page = ctx.new_page()
        page.set_default_timeout(25000)

        # ==========================================================
        # [1] 角色选择页
        # ==========================================================
        print("[1/14] 角色选择页...")
        page.goto(FRONTEND_URL + "/login", wait_until="domcontentloaded")
        time.sleep(2.5)
        save(page, "01-role-select")

        # ==========================================================
        # [2] 教师登录页（填好表单效果）
        # ==========================================================
        print("[2/14] 教师登录页...")
        page.goto(FRONTEND_URL + "/login/teacher", wait_until="domcontentloaded")
        time.sleep(2)
        page.locator("input[placeholder='请输入教师工号']").fill("张老师")
        page.locator("input[placeholder='请输入密码']").fill("123456")
        time.sleep(0.8)
        save(page, "02-teacher-login")

        # ==========================================================
        # [3] 教师登录 → 仪表盘
        # ==========================================================
        print("[3/14] 教师登录 → 仪表盘...")
        page.goto(FRONTEND_URL + "/login/teacher", wait_until="domcontentloaded")
        time.sleep(2)
        page.locator("input[placeholder='请输入教师工号']").fill("张老师")
        page.locator("input[placeholder='请输入密码']").fill("123456")
        page.locator("button:has-text('登 录')").click()
        time.sleep(3.5)
        save(page, "03-teacher-dashboard")

        # ==========================================================
        # [4] 成绩审核页（核心功能！）
        # ==========================================================
        print("[4/14] 成绩审核页 (核心)...")
        page.goto(FRONTEND_URL + "/scores", wait_until="domcontentloaded")
        time.sleep(3.5)
        save(page, "04-score-audit")

        # ==========================================================
        # [5] 成绩汇总页
        # ==========================================================
        print("[5/14] 成绩汇总页...")
        page.goto(FRONTEND_URL + "/scores/summary", wait_until="domcontentloaded")
        time.sleep(3)
        save(page, "05-score-summary")

        # ==========================================================
        # [6] 班级统计分析页
        # ==========================================================
        print("[6/14] 班级统计分析页...")
        page.goto(FRONTEND_URL + "/teacher/class-stats", wait_until="domcontentloaded")
        time.sleep(3)
        save(page, "06-class-stats")

        # ==========================================================
        # [7] 预警通知页
        # ==========================================================
        print("[7/14] 预警通知页...")
        page.goto(FRONTEND_URL + "/teacher/warnings", wait_until="domcontentloaded")
        time.sleep(3)
        save(page, "07-teacher-warnings")

        # ==========================================================
        # [8] 学生登录页（移动端尺寸）
        # ==========================================================
        print("[8/14] 学生登录页（手机尺寸）...")
        ctx_mobile = browser.new_context(
            viewport={"width": 420, "height": 900},
            device_scale_factor=2,
        )
        mp = ctx_mobile.new_page()
        mp.set_default_timeout(20000)
        mp.goto(FRONTEND_URL + "/login/student", wait_until="domcontentloaded")
        time.sleep(2)
        mp.locator("input[placeholder*='学号'], input[placeholder*='账号']").first.fill("20231012023")
        mp.locator("input[type='password']").fill("123456")
        time.sleep(0.8)
        save(mp, "08-student-login-mobile")

        # ==========================================================
        # [9] 学生端 → 登录后首页/仪表盘
        # ==========================================================
        print("[9/14] 学生端首页（仪表盘）...")
        mp.locator("button:has-text('登 录'), button:has-text('登录')").first.click()
        time.sleep(3.5)
        save(mp, "09-student-home")

        # ==========================================================
        # [10] 学生 → 学习计划
        # ==========================================================
        print("[10/14] 学生-学习计划页...")
        try:
            mp.goto(FRONTEND_URL + "/student/plan", wait_until="domcontentloaded")
            time.sleep(3)
            save(mp, "10-student-study-plan")
        except Exception as e:
            print(f"    跳过: {e}")

        # ==========================================================
        # [11] 学生 → 成绩填报
        # ==========================================================
        print("[11/14] 学生-成绩填报页...")
        try:
            mp.goto(FRONTEND_URL + "/student/submit", wait_until="domcontentloaded")
            time.sleep(3)
            save(mp, "11-student-score-submit")
        except Exception as e:
            print(f"    跳过: {e}")

        # ==========================================================
        # [12] 学生 → 我的成绩
        # ==========================================================
        print("[12/14] 学生-我的成绩页...")
        try:
            mp.goto(FRONTEND_URL + "/student/my-scores", wait_until="domcontentloaded")
            time.sleep(3)
            save(mp, "12-student-my-scores")
        except Exception as e:
            print(f"    跳过: {e}")

        # ==========================================================
        # [13] 管理员端 → 机构管理（树形结构）
        # ==========================================================
        print("[13/14] 管理员-机构管理（树形）...")
        page2 = ctx.new_page()
        page2.set_default_timeout(20000)
        page2.goto(FRONTEND_URL + "/login/admin", wait_until="domcontentloaded")
        time.sleep(2)
        inputs_admin = page2.locator("input").all()
        if len(inputs_admin) >= 2:
            inputs_admin[0].fill("admin")
            inputs_admin[1].fill("admin123")
        admin_btn = page2.locator("button:has-text('登 录'), button:has-text('登录')").first
        if admin_btn.count() > 0:
            admin_btn.click()
            time.sleep(3.5)
        try:
            page2.goto(FRONTEND_URL + "/admin/orgs", wait_until="domcontentloaded")
            time.sleep(3)
            save(page2, "13-admin-org-tree")
        except Exception as e:
            print(f"    跳过: {e}")

        # ==========================================================
        # [14] 管理员端 → 赛事管理
        # ==========================================================
        print("[14/14] 管理员-赛事管理页...")
        try:
            page2.goto(FRONTEND_URL + "/admin/events", wait_until="domcontentloaded")
            time.sleep(3)
            save(page2, "14-admin-event-manage")
        except Exception as e:
            print(f"    跳过: {e}")

        browser.close()

        # 输出汇总
        print("\n" + "=" * 55)
        print("✅ 截图流程完成！保存在:", SCREENSHOT_DIR)
        total_size = 0
        count = 0
        for f in sorted(os.listdir(SCREENSHOT_DIR)):
            if not f.endswith(".png"):
                continue
            sz = os.path.getsize(os.path.join(SCREENSHOT_DIR, f))
            total_size += sz
            count += 1
            print(f"   {count:2}. {f:<34}  {sz//1024:>5} KB")
        print("-" * 55)
        print(f"   共 {count} 张截图，合计 {total_size/1024/1024:.2f} MB")
        print("=" * 55)


if __name__ == "__main__":
    main()
