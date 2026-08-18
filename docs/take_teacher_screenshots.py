"""
教师端页面截图脚本 - 重新生成正确的页面截图
截图保存到 docs/screenshots/ 目录
"""
import os
import time
from playwright.sync_api import sync_playwright

FRONTEND_URL = "http://localhost:5173"
BACKEND_URL = "http://localhost:8080/second-class"
SCREENSHOT_DIR = r"d:\java\1\docs\screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# 教师账号
TEACHER_USER = "teacher001_screenshot"
TEACHER_PASS = "Test123456"


def save(page, name: str):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    page.screenshot(path=path, full_page=True)
    size_kb = os.path.getsize(path) // 1024
    print(f"  📸 {name}.png  ({size_kb} KB)")


def teacher_login(page, username, password):
    """执行教师登录流程"""
    page.goto(f"{FRONTEND_URL}/login/teacher", wait_until="networkidle")
    time.sleep(1.5)

    # 填写表单
    username_input = page.locator("input[placeholder='请输入教师工号']")
    password_input = page.locator("input[placeholder='请输入密码']")

    username_input.fill(username)
    password_input.fill(password)
    time.sleep(0.5)

    # 点击登录
    login_btn = page.locator("button:has-text('登 录')")
    login_btn.click()
    time.sleep(3)

    # 等待跳转到 dashboard
    page.wait_for_url("**/dashboard", timeout=10000)
    time.sleep(1)
    print(f"  ✅ 登录成功: {username}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1.25,
        )
        page = ctx.new_page()
        page.set_default_timeout(30000)

        # ==========================================================
        # [1] 角色选择页
        # ==========================================================
        print("[1/9] 角色选择页...")
        page.goto(f"{FRONTEND_URL}/login", wait_until="networkidle")
        time.sleep(2)
        save(page, "01-role-select")

        # ==========================================================
        # [2] 教师登录页（填好表单）
        # ==========================================================
        print("[2/9] 教师登录页...")
        page.goto(f"{FRONTEND_URL}/login/teacher", wait_until="networkidle")
        time.sleep(1.5)
        page.locator("input[placeholder='请输入教师工号']").fill(TEACHER_USER)
        page.locator("input[placeholder='请输入密码']").fill(TEACHER_PASS)
        time.sleep(0.8)
        save(page, "02-teacher-login")

        # ==========================================================
        # [3] 登录并跳转到仪表盘
        # ==========================================================
        print("[3/9] 教师仪表盘首页...")
        teacher_login(page, TEACHER_USER, TEACHER_PASS)
        # 保存仪表盘
        save(page, "03-teacher-dashboard")

        # ==========================================================
        # [4] 成绩审核页 - 核心功能
        # ==========================================================
        print("[4/9] 成绩审核页 (核心)...")
        page.goto(f"{FRONTEND_URL}/scores", wait_until="networkidle")
        time.sleep(2.5)
        # 等待数据加载
        page.wait_for_timeout(1500)
        save(page, "04-score-audit")

        # ==========================================================
        # [5] 成绩汇总页
        # ==========================================================
        print("[5/9] 成绩汇总页...")
        page.goto(f"{FRONTEND_URL}/scores/summary", wait_until="networkidle")
        time.sleep(2.5)
        page.wait_for_timeout(1500)
        save(page, "05-score-summary")

        # ==========================================================
        # [6] 班级统计分析页
        # ==========================================================
        print("[6/9] 班级统计分析页...")
        page.goto(f"{FRONTEND_URL}/teacher/class-stats", wait_until="networkidle")
        time.sleep(2.5)
        page.wait_for_timeout(1500)
        save(page, "06-class-stats")

        # ==========================================================
        # [7] 预警通知页
        # ==========================================================
        print("[7/9] 预警通知页...")
        page.goto(f"{FRONTEND_URL}/teacher/warnings", wait_until="networkidle")
        time.sleep(2.5)
        page.wait_for_timeout(1500)
        save(page, "07-teacher-warnings")

        # ==========================================================
        # [8] 管理员-机构管理（树形）
        # ==========================================================
        print("[8/9] 管理员-机构管理...")
        # 需要管理员登录
        page2 = ctx.new_page()
        page2.set_default_timeout(30000)
        page2.goto(f"{FRONTEND_URL}/login/admin", wait_until="networkidle")
        time.sleep(1.5)

        # 先通过API获取token
        import requests
        try:
            resp = requests.post(f"{BACKEND_URL}/api/auth/login", json={
                "username": "admin",
                "password": "admin123",
                "role": "admin"
            }, timeout=5)
            data = resp.json()
            if data.get("code") == 200:
                token = data["data"]["token"]
                # 注入token
                page2.add_init_script(f"""
                    () => {{
                        localStorage.setItem('token', '{token}');
                        localStorage.setItem('userRole', 'admin');
                        localStorage.setItem('username', '系统管理员');
                    }}
                """)
                page2.goto(f"{FRONTEND_URL}/admin/orgs", wait_until="networkidle")
                time.sleep(2.5)
                page2.wait_for_timeout(1500)
                save(page2, "13-admin-org-tree")

                # [9] 管理员-赛事管理
                print("[9/9] 管理员-赛事管理...")
                page2.goto(f"{FRONTEND_URL}/admin/events", wait_until="networkidle")
                time.sleep(2.5)
                page2.wait_for_timeout(1500)
                save(page2, "14-admin-event-manage")
        except Exception as e:
            print(f"    管理员截图跳过: {e}")
            # 用teacher账户直接导航（因为security permitAll）
            page.goto(f"{FRONTEND_URL}/admin/orgs", wait_until="networkidle")
            time.sleep(2.5)
            save(page, "13-admin-org-tree")
            page.goto(f"{FRONTEND_URL}/admin/events", wait_until="networkidle")
            time.sleep(2.5)
            save(page, "14-admin-event-manage")

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
            print(f"   {count}. {f:<34}  {sz//1024:>5} KB")
        print("-" * 55)
        print(f"   共 {count} 张截图，合计 {total_size/1024/1024:.2f} MB")
        print("=" * 55)


if __name__ == "__main__":
    main()
