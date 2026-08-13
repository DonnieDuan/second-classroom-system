# 学生第二课堂成绩管理系统 - 自动化测试套件

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/pytest-7.4%2B-green" alt="Pytest Version">
  <img src="https://img.shields.io/badge/Playwright-1.40%2B-purple" alt="Playwright Version">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-orange" alt="Platform">
  <img src="https://img.shields.io/badge/CI-GitHub%20Actions-blue" alt="CI Status">
</p>

## 📁 项目结构

```
tests/
├── api/                          # 后端接口自动化测试
│   ├── test_auth.py              # 用户认证模块测试（9个用例）
│   ├── test_score.py             # 成绩管理模块测试（16个用例）
│   ├── test_event.py             # 赛事管理模块测试（13个用例）
│   └── test_student_org.py       # 学生与机构管理测试（11个用例）
│
├── ui/                           # 前端UI自动化测试
│   ├── test_login_page.py        # 登录页面UI测试
│   └── test_score_page.py        # 成绩审核页面UI测试
│
├── common/                       # 公共工具模块
│   ├── config.py                 # 测试配置（服务地址、测试账号）
│   └── __init__.py               # API请求封装类和断言工具
│
├── reports/                      # 测试报告输出目录
│
├── conftest.py                   # pytest全局配置和fixture
├── pytest.ini                    # pytest配置文件
├── requirements-api.txt          # 接口测试依赖
├── requirements-ui.txt           # UI测试依赖
└── README.md                     # 本文档

.github/
└── workflows/
    └── automated-tests.yml       # GitHub Actions CI/CD 配置
```

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- 后端服务已启动（默认 http://localhost:8080）
- （可选）前端服务已启动（默认 http://localhost:5173）
- （可选）MySQL 数据库已配置

### 1. 安装依赖

```bash
# 进入测试目录
cd tests

# 安装接口测试依赖
pip install -r requirements-api.txt

# 安装UI测试依赖（如果需要运行UI测试）
pip install -r requirements-ui.txt
playwright install chromium    # 安装浏览器
```

### 2. 配置测试环境

编辑 [common/config.py](tests/common/config.py) 修改配置：

```python
# 服务地址
BACKEND_URL = "http://localhost:8080"
FRONTEND_URL = "http://localhost:5173"

# 测试账号（修改为你自己的）
TEST_STUDENT = {"username": "20231012023", "password": "123456"}
TEST_TEACHER = {"username": "teacher", "password": "123456"}
TEST_ADMIN = {"username": "admin", "password": "123456"}
```

也可以通过环境变量配置：

```bash
# Windows PowerShell
$env:BACKEND_URL = "http://your-server:8080"
$env:FRONTEND_URL = "http://your-server:5173"

# Linux/Mac
export BACKEND_URL="http://your-server:8080"
export FRONTEND_URL="http://your-server:5173"
```

---

## 📋 运行测试

### 方式一：运行接口测试

```bash
cd tests

# 运行所有接口测试
pytest api/ -v -s

# 运行单个模块
pytest api/test_auth.py -v -s
pytest api/test_score.py -v -s

# 运行带测试报告
pytest api/ -v --html=reports/api_report.html --self-contained-html

# 生成Junit XML报告（兼容CI/CD）
pytest api/ -v --junitxml=reports/api_results.xml
```

### 方式二：运行UI测试

```bash
cd tests

# 运行所有UI测试（需要前端服务启动）
pytest ui/ -v -s

# 运行截图+录屏
pytest ui/ -v --screenshot=only-on-failure --video=retain-on-failure

# 生成报告
pytest ui/ -v --html=reports/ui_report.html --self-contained-html
```

### 方式三：运行全部测试

```bash
cd tests
pytest -v -s \
  --html=reports/full_report.html \
  --self-contained-html \
  --junitxml=reports/results.xml
```

### 常用pytest参数

| 参数 | 说明 |
|------|------|
| `-v` | 详细输出每个用例执行结果 |
| `-s` | 显示print输出内容 |
| `-k "keyword"` | 只运行名称包含keyword的用例 |
| `-m "mark"` | 运行带特定标记的用例 |
| `--html=path` | 生成HTML格式报告 |
| `--junitxml=path` | 生成JUnit XML报告 |
| `--tb=short` | 简化错误堆栈信息 |
| `-n 4` | 4线程并行执行（需安装pytest-xdist） |

---

## 🔬 测试用例清单

### 接口测试用例（共49+个）

| 模块 | 文件 | 用例数 | 说明 |
|------|------|--------|------|
| 用户认证 | test_auth.py | 9 | 登录/注册、异常场景校验 |
| 成绩管理 | test_score.py | 16 | 提交/审核/查询/统计 |
| 赛事管理 | test_event.py | 13 | 赛事/赛项/获奖级别 CRUD |
| 学生机构 | test_student_org.py | 11 | 学生信息/机构树 CRUD |

### UI测试用例

| 模块 | 文件 | 说明 |
|------|------|------|
| 登录页面 | test_login_page.py | 页面标题、表单元素、登录流程 |
| 成绩页面 | test_score_page.py | 列表加载、审核按钮、统计页面、预警页面 |

---

## ⚙️ GitHub Actions CI/CD

### 功能特性

项目已内置完整的 GitHub Actions 自动化流程，代码提交后自动执行：

1. **接口测试Job**：
   - 自动启动 MySQL 8.0 容器
   - 编译启动后端 Spring Boot 服务
   - 运行全部接口自动化用例
   - 上传测试报告到 Artifacts

2. **UI测试Job**：
   - 安装 Playwright + Chromium 浏览器
   - npm 安装依赖并启动前端 Vite 服务
   - 运行全部 UI 自动化测试
   - 自动截图+录屏（失败时保留）
   - 上传测试报告

3. **结果汇总Job**：
   - 汇总两个Job的测试结果
   - 解析JUnit XML统计用例数/失败数

### 手动触发

在 GitHub 仓库页面：
1. 进入 **Actions** 标签
2. 左侧选择 **"自动化测试 CI"**
3. 点击 **"Run workflow"** → 选择分支 → 确认运行

### 触发条件

```yaml
on:
  push:                      # 代码push时
    branches: [main, master]
  pull_request:              # 创建/更新PR时
    branches: [main, master]
  workflow_dispatch:         # 手动点击触发
```

---

## 📊 查看测试报告

### 本地运行后

```
tests/reports/
├── api_test_report.html        # 接口测试HTML报告（直接浏览器打开）
├── ui_test_report.html         # UI测试HTML报告
├── api_test_results.xml        # JUnit XML格式（CI用）
├── ui_login_test.png           # UI测试截图
├── ui_score_list.png           # 成绩页截图
└── ...
```

### GitHub Actions 下载

1. 进入 Actions 页面，点击某次运行
2. 滚动到 **Artifacts** 区域
3. 下载 **"API测试报告"** 或 **"UI测试报告"** 压缩包

---

## 🛠️ 自定义扩展

### 添加新的接口测试用例

1. 在 `tests/api/` 下创建 `test_xxx.py` 文件
2. 编写测试类：

```python
# tests/api/test_xxx.py
import pytest
from common import ApiClient, assert_success

class TestYourModule:
    
    def setup_method(self):
        self.client = ApiClient()
    
    def test_your_case(self):
        """TC-XXX-001: 用例说明"""
        print("\n[TC-XXX-001] 用例名称")
        response = self.client.get("/api/your-endpoint")
        data = assert_success(response, "用例名")
        # 你的断言
        assert data.get("data") is not None
```

### 添加新的UI测试用例

```python
# tests/ui/test_xxx_page.py
from playwright.sync_api import Page

class TestYourPage:
    
    def test_page_load(self, page: Page):
        """UI-XXX-001: 页面加载"""
        page.goto("http://localhost:5173/#/your-page")
        page.wait_for_timeout(2000)
        # 你的断言或操作
        page.screenshot(path="reports/xxx.png")
```

---

## ❓ 常见问题

**Q1: 接口测试全部失败？**
> 检查后端服务是否启动：浏览器访问 http://localhost:8080/api/auth/login 看是否能响应。
> 检查 common/config.py 中的 BACKEND_URL 是否正确。

**Q2: UI测试页面打不开？**
> 检查前端服务是否启动：先 cd frontend-admin && npm run dev
> 或修改 FRONTEND_URL 为你的部署地址。

**Q3: pytest 找不到模块？**
> 确保 cd 到 tests 目录下运行，或者用 pytest tests/api/ 路径方式运行。
> conftest.py 已自动将 tests 目录加入 sys.path。

**Q4: Playwright 浏览器报错？**
> 重新安装浏览器：`playwright install chromium`
> Linux环境还需要：`playwright install-deps`

---

## 📝 License

MIT License - 仅供学习和测试使用。
