# 自动化测试体系与压测报告

> 基于 **学生第二课堂成绩管理系统** 的真实落地实践

---

## 一、自动化测试体系架构图

```
┌────────────────────────────────────────────────────────────────────────┐
│                        自动化测试体系总览                                │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌──────────────────────────┐   ┌──────────────────────────────────┐   │
│  │   1. 接口功能测试         │   │   2. UI 回归测试                 │   │
│  │      Python + Pytest     │   │      Python + Playwright        │   │
│  │      ApiClient 封装      │   │      登录/审核/统计截图对比      │   │
│  │      49+ 用例覆盖 5模块  │   │      失败自动截图+Trace         │   │
│  │      HTML+JUnit 报告    │   │      三端（教师/学生/管理员）   │   │
│  └──────────────────────────┘   └──────────────────────────────────┘   │
│               │                                     │                  │
│               └──────────────────┬──────────────────┘                  │
│                                  ▼                                     │
│                   ┌──────────────────────────────┐                     │
│                   │   3. 性能 / 并发压测         │                     │
│                   │   ├── Locust (动态用户数)     │                     │
│                   │   ├── pytest-xdist (并发)     │                     │
│                   │   └── Python threading 基准   │                     │
│                   │   输出 QPS / P50 / P95       │                     │
│                   └──────────────────────────────┘                     │
│                                  │                                     │
│                                  ▼                                     │
│                   ┌──────────────────────────────┐                     │
│                   │  4. CI/CD (GitHub Actions)   │                     │
│                   │   ├── Job1: 接口自动化       │                     │
│                   │   ├── Job2: UI自动化         │                     │
│                   │   └── Job3: 结果汇总 + 存档  │                     │
│                   │   Artifacts下载HTML/XML报告  │                     │
│                   └──────────────────────────────┘                     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 二、功能测试：Pytest + Requests（接口层）

### 测试框架设计模式

```
tests/
├── common/
│   ├── __init__.py        # ApiClient 通用请求类 (requests.Session 复用连接)
│   ├── config.py          # 环境变量可覆盖的 BACKEND_URL / 测试账号 / 数据
│   └── 断言工具
├── api/                   # 功能接口用例
│   ├── test_auth.py       # 登录/注册 9用例
│   ├── test_score.py      # 成绩提交/审核/查询 16用例
│   ├── test_event.py      # 赛事/赛项/级别 CRUD 13用例
│   └── test_student_org.py# 学生/机构 11用例
└── conftest.py            # pytest fixture 注入 teacher_client / student_client
```

### ApiClient 封装关键代码（摘录）
```python
class ApiClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or BACKEND_URL
        self.session = requests.Session()   # 连接池，压测提升吞吐
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "SecondClass-AutoTest/1.0"
        })
    def _request(self, method, endpoint, **kwargs):
        kwargs.setdefault("timeout", REQUEST_TIMEOUT)
        url = f"{self.base_url}{endpoint}"
        try:
            return self.session.request(method, url, **kwargs)
        except requests.exceptions.ConnectionError:
            raise AssertionError(f"连接失败: {method} {url} - 请检查服务是否启动")
```

### 用例覆盖率

| 模块 | 用例数 | 关键场景 |
|------|--------|----------|
| 用户认证 | 9 | 学生/教师正常登录、用户名不存在、密码错误、空值校验 |
| 成绩管理 | 16 | 成绩提交、缺失字段校验、审核通过/拒绝、分页+筛选、班级汇总、仪表盘 |
| 赛事管理 | 13 | 赛事增/删/改/查、赛项按赛事分组、获奖级别CRUD |
| 学生+机构 | 11 | 学生列表/详情/班级查询、机构树结构、新增/删除/详情 |
| **合计** | **49** | |

---

## 三、并发 / 性能压测实现

### ✅ 方案 A：Python Threading 基准测试（快速可复现）

`tests/performance/test_parallel_stress.py::test_thread_benchmark`

**实际执行结果（本机实测）：**

```
======================================================================
  🚀 Python 多线程并发基准测试  |  100 线程 × 4接口 = 400 请求
======================================================================
  总耗时:            0.59 秒
  总请求数:          400
  ✅ 成功:           400
  ❌ 失败:           0        ← 100% 成功率
  整体 QPS:          674.72 req/s
----------------------------------------------------------------------
  · org_tree  (机构树)         avg= 139.46ms  P95= 243.87ms  n=100
  · score_list(成绩列表分页)   avg= 316.74ms  P95= 410.40ms  n=100
  · my_scores (学生我的成绩)   avg=  10.61ms  P95=  28.33ms  n=100
  · event_all (赛事全量)       avg=   9.57ms  P95=  24.27ms  n=100
======================================================================
```

**关键代码思路：**
```python
import threading, time, statistics
def test_thread_benchmark():
    def worker():
        client = ApiClient()                # 每个线程独立Session
        for path in ["/api/org/tree", "/api/score/list",
                     "/api/app/score/myScores", "/api/event/all"]:
            t0 = time.time()
            r = client.get(path)            # requests.Session 走HTTP连接池
            record_resp_time_ms(time.time()-t0, r.status_code)

    threads = [Thread(target=worker) for _ in range(100)]
    t = time.time()
    for th in threads: th.start()
    for th in threads: th.join(timeout=60)
    # 打印 QPS、Avg、P50、P95、P99
```

---

### ✅ 方案 B：Locust 专业动态压测（模拟真实用户）

`tests/performance/locustfile.py`

**三种场景加权模拟真实流量：**

| 角色场景类 | 用户占比(weight) | 高频操作 |
|---|---|---|
| TeacherUserBehavior | 3 (≈ 60%) | 成绩审核列表×8、班级统计×3、Dashboard×2、审核通过×1 |
| StudentUserBehavior | 2 (≈ 25%) | 查成绩×5、查总分×3、成绩提交×2、赛事列表×1 |
| PublicApiBehavior | 1 (≈ 15%) | 机构树×5、赛事列表×3、获奖级别×3、学生列表×2 |

**启动命令：**
```bash
# Web UI：浏览器实时观察 RPS / 响应时间图表
locust -f tests/performance/locustfile.py --host=http://localhost:8080/second-class

# 无UI：50用户、持续2分钟、直接产出CSV+HTML报告
locust -f tests/performance/locustfile.py \
       --host=http://localhost:8080/second-class \
       --headless -u 50 -r 2 -t 2m \
       --csv=tests/reports/locust_result \
       --html=tests/reports/locust_report.html
```

**Locust 与 pytest 方案的取舍：**
- **功能/回归 CI** 常用 pytest（断言严格、和JUnit报告互通）
- **性能/压测** 常用 Locust（支持百万级用户、实时图表、多种权重用户）

---

### ✅ 方案 C：pytest-xdist 多进程并发用例

```bash
# 8 进程并行执行，重复 50 轮 ≈ 压力测试
pip install pytest-xdist pytest-repeat

pytest tests/performance/test_parallel_stress.py \
       -n 8 --count 50 -v \
       --html=tests/reports/stress_test_report.html \
       --self-contained-html
```

适合**并发功能正确性验证**（比如同时提交成绩事务不丢数据、唯一索引是否真的拦了重复数据）。

---

## 四、CI/CD：GitHub Actions 全自动集成

`.github/workflows/automated-tests.yml`（已配置，推送到 main 或 PR 自动跑）

```
  ┌─ Job 1: 接口自动化测试 ─────────────────────────────┐
  │ services: mysql:8.0 (端口3306，建库+导入secscore.sql)│
  │ steps: Maven 编译 → 后台启动 Spring Boot            │
  │        → 安装 pytest + requests                      │
  │        → 运行 tests/api/ 全部 49+ 用例              │
  │        → 上传 reports/ (HTML + JUnit XML) Artifacts │
  └──────────────────────────────────────────────────────┘
  ┌─ Job 2: UI 自动化测试 ──────────────────────────────┐
  │ steps: npm ci → Playwright 安装 Chromium            │
  │        → npm run dev 启动前端                        │
  │        → pytest tests/ui/ --screenshot=only-on-fail │
  │        → 上传 UI 报告 + 失败截图                     │
  └──────────────────────────────────────────────────────┘
  ┌─ Job 3: 测试结果汇总 ───────────────────────────────┐
  │ 解析 JUnit XML → 输出 用例数 / 失败数 / 断言文本     │
  └──────────────────────────────────────────────────────┘
```

---

## 五、怎么运行（快速复刻）

```bash
# ===== 环境准备 =====
cd tests
pip install -r requirements-api.txt    # pytest + requests + locust + playwright
playwright install chromium             # UI测试浏览器

# ===== 接口功能测试 =====
pytest api/ -v -s --html=reports/api_report.html --self-contained-html

# ===== 并发基准压测（100线程）=====
pytest performance/test_parallel_stress.py::test_thread_benchmark -v -s

# ===== Locust Web UI 压测 =====
locust -f performance/locustfile.py --host=http://localhost:8080/second-class
# 浏览器打开 http://localhost:8089 输入用户数，Start Swarming

# ===== Locust 无UI脚本模式 =====
locust -f performance/locustfile.py --host=http://localhost:8080/second-class \
       --headless -u 100 -r 5 -t 3m \
       --csv=reports/locust --html=reports/locust_report.html
```

---

> 💡 **本测试体系 GitHub 源码位置：**
> - 接口测试：[`tests/api/`](tests/api/)
> - UI 测试：[`tests/ui/`](tests/ui/)
> - 压测脚本：[`tests/performance/`](tests/performance/)
> - CI/CD：[`.github/workflows/automated-tests.yml`](.github/workflows/automated-tests.yml)
