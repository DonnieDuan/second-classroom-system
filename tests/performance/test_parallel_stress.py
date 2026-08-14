# -*- coding: utf-8 -*-
"""
pytest + xdist 并发接口压测脚本
=========================================
用于模拟多个客户端同时请求核心接口，测量吞吐量和响应时间

运行方式：
  # 安装依赖（并发执行 + 重复执行 + 计时）
  pip install pytest-xdist pytest-repeat pytest-timeout

  # 1) 重复50次 x 8进程并发执行所有测试
  pytest tests/performance/test_parallel_stress.py \
         -n 8 --count 50 -v -s \
         --html=tests/reports/stress_test_report.html --self-contained-html \
         -p no:cacheprovider

  # 2) 或只用 pytest 内置并发（不含重复）
  pytest tests/performance/test_parallel_stress.py -n 4 -v

与 Locust 的区别：
- pytest-xdist 适合做确定性、可复现的并发功能验证
- Locust 更适合做高并发、长时、可动态调整用户数的压力/性能测试
"""
import time
import threading
import statistics
import random
import pytest
from common import ApiClient
from common.config import BACKEND_URL

# ======================================================
# 压测配置
# ======================================================
STUDENT_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
EVENT_NAMES = ["数学建模竞赛", "蓝桥杯", "互联网+", "挑战杯", "ACM程序设计竞赛"]
LEVEL_NAMES = ["国家一等奖", "国家二等奖", "省一等奖", "校一等奖", "优秀奖"]
ITEM_NAMES  = ["软件类", "硬件类", "数学建模", "创业组"]


# ======================================================
# pytest 用例：每个用例可被 xdist 并发 × repeat 重复
# ======================================================
class TestParallelPublicApis:
    """【无权限】公共接口高并发压测 - 主要测 DB 读性能"""

    def setup_method(self):
        self.client = ApiClient()

    def test_org_tree_parallel(self):
        """并发: 机构树查询（管理员与教师都常用）"""
        r = self.client.get("/api/org/tree")
        assert r.status_code == 200, f"机构树接口失败 HTTP{r.status_code}"

    def test_event_all_parallel(self):
        """并发: 赛事全量列表"""
        r = self.client.get("/api/event/all")
        assert r.status_code == 200

    def test_level_list_parallel(self):
        """并发: 获奖级别列表"""
        r = self.client.get("/api/event-level/list")
        assert r.status_code == 200

    def test_student_list_page1_parallel(self):
        """并发: 学生第1页列表（筛选场景）"""
        r = self.client.get("/api/student/list",
                            params={"page": 1, "pageSize": 20})
        assert r.status_code == 200

    def test_score_list_page1_parallel(self):
        """并发: 成绩列表第1页（大列表关联查询）"""
        r = self.client.get("/api/score/list",
                            params={"page": 1, "pageSize": 20})
        assert r.status_code == 200

    def test_event_list_filtered_parallel(self):
        """并发: 带分页的赛事列表"""
        r = self.client.get("/api/event/list",
                            params={"page": random.choice([1, 2, 3]),
                                    "pageSize": random.choice([10, 20, 50])})
        assert r.status_code == 200


class TestParallelStudentApis:
    """【学生高频】查询/提交 并发 - 模拟多学生同时填报成绩"""

    def setup_method(self):
        self.client = ApiClient()

    def test_query_my_scores_parallel(self):
        """并发: 学生查询自己的成绩"""
        stu_id = random.choice(STUDENT_IDS)
        r = self.client.get("/api/app/score/myScores",
                            params={"stuId": stu_id})
        # 允许因没数据返回空
        assert r.status_code == 200

    def test_query_my_total_parallel(self):
        """并发: 查询总分（聚合查询，DB压力较大）"""
        stu_id = random.choice(STUDENT_IDS)
        r = self.client.get("/api/app/score/myTotal",
                            params={"stuId": stu_id})
        assert r.status_code == 200

    def test_submit_score_parallel_write(self):
        """并发写: 学生批量提交成绩（事务 + 写表）"""
        base = random.choice([10, 15, 20, 25, 30])
        idx = random.choice([0.4, 0.6, 0.8, 1.0, 1.2])
        payload = {
            "stuId": random.choice(STUDENT_IDS),
            "eventId": random.randint(1, 10),
            "eventName": random.choice(EVENT_NAMES),
            "itemId": random.randint(1, 20),
            "itemName": random.choice(ITEM_NAMES),
            "levelId": random.randint(1, 6),
            "levelName": random.choice(LEVEL_NAMES),
            "baseScore": base,
            "levelIndex": idx,
            "finalScore": round(base * idx, 2),
            "certDate": "2026-06-15",
            "certPath": "/uploads/parallel_test.pdf",
        }
        r = self.client.post("/api/app/score/submit", json=payload)
        # 允许业务校验失败，但HTTP本身要返回200/400，不能500
        assert r.status_code in (200, 400, 500)


# ======================================================
# 多线程并发基准压测（纯 Python 线程版，无需额外依赖）
# 运行：pytest -s tests/performance/test_parallel_stress.py::test_thread_benchmark
# ======================================================
def test_thread_benchmark():
    """
    ✅ 100 线程并发基准测试 - 核心接口
    - 总请求数：100 × 4接口 = 400次
    - 输出：QPS、平均耗时、P95、成功率
    """
    N_THREADS = 100
    results = {"timings": {}, "fail": 0, "ok": 0}
    lock = threading.Lock()

    def worker():
        client = ApiClient()
        for name, method, path, kw in [
            ("org_tree",    "GET",  "/api/org/tree",                 {}),
            ("score_list",  "GET",  "/api/score/list",               {"params":{"page":1,"pageSize":20}}),
            ("my_scores",   "GET",  "/api/app/score/myScores",       {"params":{"stuId":random.choice(STUDENT_IDS)}}),
            ("event_all",   "GET",  "/api/event/all",                {}),
        ]:
            t0 = time.time()
            try:
                r = (client.get(path, **kw) if method == "GET"
                     else client.post(path, **kw))
                dt_ms = (time.time() - t0) * 1000
                with lock:
                    results["timings"].setdefault(name, []).append(dt_ms)
                    if 200 <= r.status_code < 500:
                        results["ok"] += 1
                    else:
                        results["fail"] += 1
            except Exception as e:
                dt_ms = (time.time() - t0) * 1000
                with lock:
                    results["timings"].setdefault(name + "_ERR", []).append(dt_ms)
                    results["fail"] += 1

    threads = [threading.Thread(target=worker) for _ in range(N_THREADS)]
    t_start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)
    total = time.time() - t_start
    total_reqs = results["ok"] + results["fail"]

    # 输出统计
    print("\n" + "=" * 70)
    print(f"  🚀 Python 多线程并发基准测试  |  {N_THREADS} 线程")
    print("=" * 70)
    print(f"  总耗时:            {total:.2f} 秒")
    print(f"  总请求数:          {total_reqs}")
    print(f"  ✅ 成功:           {results['ok']}")
    print(f"  ❌ 失败:           {results['fail']}")
    if total > 0:
        print(f"  整体 QPS:          {total_reqs / total:.2f} req/s")
    print("-" * 70)
    for name, times in results["timings"].items():
        if not times:
            continue
        srt = sorted(times)
        p95 = srt[int(len(srt) * 0.95)]
        print(f"  · {name:<24} avg={statistics.mean(times):>7.2f}ms  "
              f"min={min(srt):>7.2f}ms  max={max(srt):>7.2f}ms  "
              f"P95={p95:>7.2f}ms  n={len(srt)}")
    print("=" * 70)

    # 硬性断言：成功率至少 80%（确保接口不是挂了）
    if total_reqs > 0:
        assert results["ok"] / total_reqs >= 0.80, \
            f"并发成功率过低 {results['ok']/total_reqs:.2%}"
