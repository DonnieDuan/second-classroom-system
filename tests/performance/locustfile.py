# -*- coding: utf-8 -*-
"""
Locust 并发压测脚本 - 学生第二课堂系统
=============================================
覆盖核心接口：登录 / 成绩查询 / 成绩提交 / 成绩审核 / 机构树 / 仪表盘统计

使用方法：
  # 安装
  pip install locust

  # 1) Web UI 模式（常用：手动调整并发数，实时看图表）
  locust -f tests/performance/locustfile.py --host=http://localhost:8080/second-class

  # 2) 无UI模式（直接跑，输出 CSV/HTML 报告）- 例：50用户，30秒爬升，持续120秒
  locust -f tests/performance/locustfile.py --host=http://localhost:8080/second-class \
         --headless -u 50 -r 2 -t 120s \
         --csv=tests/reports/locust_result --html=tests/reports/locust_report.html

GitHub Actions 中可通过 headless 模式生成报告并上传 Artifacts
"""
from locust import HttpUser, task, between, events, TaskSet
import random
import json
import statistics

# ============================================================
# 测试数据
# ============================================================
TEACHER_LOGIN_PAYLOADS = [
    {"username": "张老师",  "password": "123456", "role": "teacher"},
    {"username": "李老师",  "password": "123456", "role": "teacher"},
    {"username": "admin",   "password": "admin123", "role": "admin"},
]

STUDENT_LOGIN_PAYLOADS = [
    {"username": "20231012023", "password": "123456", "role": "student"},
    {"username": "20231012024", "password": "123456", "role": "student"},
    {"username": "20231012025", "password": "123456", "role": "student"},
    {"username": "20231012026", "password": "123456", "role": "student"},
]

EVENT_NAMES = [
    "全国大学生数学建模竞赛", "蓝桥杯全国软件大赛",
    "中国大学生计算机设计大赛", "互联网+大学生创新创业大赛",
    "ACM-ICPC程序设计竞赛", "挑战杯课外学术科技作品竞赛",
]
LEVEL_NAMES = ["一等奖", "二等奖", "三等奖", "优秀奖", "省级一等奖", "校级一等奖"]
ITEM_NAMES  = ["软件类本科组", "硬件类", "数学组", "创业计划组", "Web应用开发"]

# ============================================================
# 全局统计
# ============================================================
response_times = []
fail_count = 0
success_count = 0


@events.quitting.add_listener
def _(environment, **kw):
    """压测结束时输出汇总（headless模式下会自动触发）"""
    global response_times, fail_count, success_count
    if not response_times:
        return
    environment.runner.stats.total.log_request(
        "CUSTOM_SUMMARY", "",
        response_time=sum(response_times) / len(response_times),
        length=0,
    )
    print("\n" + "=" * 70)
    print("  📊 压测自定义汇总")
    print("=" * 70)
    print(f"  请求总数:       {success_count + fail_count}")
    print(f"  成功数:         {success_count}")
    print(f"  失败数:         {fail_count}")
    print(f"  成功率:         {success_count/(success_count+fail_count)*100:.2f}%")
    print(f"  平均响应时间:   {statistics.mean(response_times):.2f} ms")
    print(f"  P50 响应时间:   {statistics.median(response_times):.2f} ms")
    try:
        rt_sorted = sorted(response_times)
        p95_idx = int(len(rt_sorted) * 0.95)
        p99_idx = int(len(rt_sorted) * 0.99)
        print(f"  P95 响应时间:   {rt_sorted[p95_idx]:.2f} ms")
        print(f"  P99 响应时间:   {rt_sorted[p99_idx]:.2f} ms")
    except Exception:
        pass
    print("=" * 70)


def _record(resp):
    """统一记录每次请求"""
    global response_times, fail_count, success_count
    ms = resp.elapsed.total_seconds() * 1000
    response_times.append(ms)
    if 200 <= resp.status_code < 500:
        try:
            j = resp.json()
            code = j.get("code", -1)
            if code == 200 or code == 0:
                success_count += 1
            else:
                fail_count += 1
        except Exception:
            # 非JSON返回（如登录成功）也算成功
            success_count += 1
    else:
        fail_count += 1


# ============================================================
# 1. 教师端场景：登录 → 审核列表 → 班级统计 → 预警 → Dashboard
# ============================================================
class TeacherUserBehavior(HttpUser):
    """教师/管理员 常规操作（约80%流量：审核与查询为主）"""

    wait_time = between(0.5, 2.0)  # 用户思考时间 0.5~2 秒
    weight = 3  # 教师场景占比更高（日常审核为主）
    token = None

    def on_start(self):
        """用户首次启动时：执行教师登录并保存 token"""
        payload = random.choice(TEACHER_LOGIN_PAYLOADS)
        with self.client.post("/api/auth/login",
                              json=payload,
                              catch_response=True) as resp:
            _record(resp)
            if resp.status_code == 200:
                try:
                    data = resp.json().get("data") or {}
                    tk = data.get("token")
                    if tk:
                        self.token = tk
                except Exception:
                    pass

    def _headers(self):
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    # --------- 核心高频接口 ---------
    @task(8)  # 权重最高：80% 时间都在刷成绩审核列表
    def task_score_list(self):
        """成绩审核列表（分页 + 筛选）"""
        params = {
            "page": random.choice([1, 1, 1, 2, 3]),
            "pageSize": random.choice([10, 15, 20, 50]),
            "auditStatus": random.choice([None, None, 0, 1, 2]),
        }
        params = {k: v for k, v in params.items() if v is not None}
        with self.client.get("/api/score/list", params=params,
                             headers=self._headers(), catch_response=True) as r:
            _record(r)

    @task(3)
    def task_class_stats(self):
        """班级统计接口"""
        class_id = random.choice([1, 2, 3, 4, 5])
        with self.client.get(f"/admin/statistics/class/{class_id}",
                             headers=self._headers(), catch_response=True) as r:
            _record(r)

    @task(2)
    def task_dashboard(self):
        """管理端仪表盘（首页高频访问）"""
        with self.client.get("/api/admin/dashboard",
                             headers=self._headers(), catch_response=True) as r:
            _record(r)

    @task(2)
    def task_warnings(self):
        """预警通知接口"""
        with self.client.get("/api/admin/dashboard",
                             headers=self._headers(), catch_response=True) as r:
            _record(r)

    @task(1)
    def task_audit_pass(self):
        """成绩审核通过（1/15 的写操作比例）"""
        audit_payload = {
            "scoreId": random.randint(1, 30),
            "auditStatus": random.choice([1, 2]),
            "auditRemark": random.choice(["审核通过", "信息真实有效", "材料不全请重新上传", "证书不清晰"]),
        }
        with self.client.post("/api/admin/audit",
                              json=audit_payload,
                              headers=self._headers(), catch_response=True) as r:
            _record(r)


# ============================================================
# 2. 学生端场景：登录 → 成绩列表 → 成绩提交 → 学习计划
# ============================================================
class StudentUserBehavior(HttpUser):
    """学生 常规操作（大量学生并发提交成绩）"""

    wait_time = between(1, 3)
    weight = 2
    token = None

    def on_start(self):
        payload = random.choice(STUDENT_LOGIN_PAYLOADS)
        with self.client.post("/api/auth/login",
                              json=payload,
                              catch_response=True) as resp:
            _record(resp)
            if resp.status_code == 200:
                try:
                    data = resp.json().get("data") or {}
                    tk = data.get("token")
                    if tk:
                        self.token = tk
                except Exception:
                    pass

    def _headers(self):
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    @task(5)
    def task_query_my_scores(self):
        """学生查询我的成绩（高频）"""
        stu_id = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        with self.client.get("/api/app/score/myScores",
                             params={"stuId": stu_id},
                             headers=self._headers(), catch_response=True) as r:
            _record(r)

    @task(3)
    def task_query_total(self):
        """学生总积分（首页展示）"""
        stu_id = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        with self.client.get("/api/app/score/myTotal",
                             params={"stuId": stu_id},
                             headers=self._headers(), catch_response=True) as r:
            _record(r)

    @task(2)  # 提交成绩的并发写操作
    def task_submit_score(self):
        """学生提交成绩（写操作）"""
        base = random.choice([10, 15, 20, 25, 30])
        lvl_idx = random.choice([0.4, 0.6, 0.8, 1.0, 1.2, 1.5])
        payload = {
            "stuId": random.randint(1, 20),
            "eventId": random.randint(1, 10),
            "eventName": random.choice(EVENT_NAMES),
            "itemId": random.randint(1, 20),
            "itemName": random.choice(ITEM_NAMES),
            "levelId": random.randint(1, 6),
            "levelName": random.choice(LEVEL_NAMES),
            "baseScore": base,
            "levelIndex": lvl_idx,
            "finalScore": round(base * lvl_idx, 2),
            "certDate": f"2026-0{random.randint(1,7)}-{random.randint(1,28):02d}",
            "certPath": "/uploads/stu_" + str(random.randint(1000, 9999)) + ".pdf",
        }
        with self.client.post("/api/app/score/submit",
                              json=payload,
                              headers=self._headers(), catch_response=True) as r:
            _record(r)

    @task(1)
    def task_event_all(self):
        """赛事信息列表（学习计划页加载）"""
        with self.client.get("/api/event/all",
                             headers=self._headers(), catch_response=True) as r:
            _record(r)


# ============================================================
# 3. 公共读接口：机构树/赛事列表（无权限、低资源消耗）
# ============================================================
class PublicApiBehavior(HttpUser):
    """公共接口并发（机构树、赛事、级别），可承受更高并发"""

    wait_time = between(0.2, 1)
    weight = 1

    @task(5)
    def task_org_tree(self):
        with self.client.get("/api/org/tree", catch_response=True) as r:
            _record(r)

    @task(3)
    def task_event_list(self):
        with self.client.get("/api/event/list",
                             params={"page": 1, "pageSize": 20},
                             catch_response=True) as r:
            _record(r)

    @task(3)
    def task_level_list(self):
        with self.client.get("/api/event-level/list", catch_response=True) as r:
            _record(r)

    @task(2)
    def task_student_list(self):
        with self.client.get("/api/student/list",
                             params={"page": 1, "pageSize": 15},
                             catch_response=True) as r:
            _record(r)
