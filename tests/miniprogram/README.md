# 微信小程序测试套件

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/pytest-7.4%2B-green" alt="Pytest Version">
  <img src="https://img.shields.io/badge/Mock-U nit%20Tests-orange" alt="Mock Tests">
  <img src="https://img.shields.io/badge/Integration-Tests-purple" alt="Integration Tests">
</p>

本目录包含微信小程序（`miniprogram/`）的自动化测试，分为 **Mock 单元测试** 和 **集成测试** 两大类。

---

## 📁 目录结构

```
tests/miniprogram/
├── test_mock_unit.py        # Mock 单元测试（无需后端，35 个用例）
├── test_miniprogram.py      # 小程序业务流程集成测试（需后端）
├── test_api_miniprogram.py  # 小程序 API 集成测试（需后端）
├── conftest.py              # pytest 配置和公共 fixture
├── requirements.txt         # 依赖清单
└── __init__.py              # 包初始化
```

---

## 🔧 测试框架和依赖

### 核心框架

| 框架 | 版本 | 用途 |
|------|------|------|
| [pytest](https://docs.pytest.org/) | >= 7.0.0 | 测试运行器，支持 fixtures、参数化、标记 |
| [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) | 内置 | Mock 对象模拟，用于单元测试 |
| [requests](https://requests.readthedocs.io/) | >= 2.28.0 | HTTP 客户端，用于集成测试调用后端 API |

### 安装依赖

```bash
cd tests/miniprogram
pip install -r requirements.txt
```

或单独安装：

```bash
pip install pytest>=7.0.0 requests>=2.28.0
```

---

## 🚀 如何运行单元测试（无需后端）

Mock 单元测试直接测试从小程序 JS 中提取的纯业务逻辑函数，**不需要启动后端服务**。

### 运行全部单元测试

```bash
cd tests/miniprogram
python -m pytest test_mock_unit.py -v --tb=short
```

### 运行指定测试类或用例

```bash
# 只运行登录流程测试
python -m pytest test_mock_unit.py::TestLoginFlowMock -v

# 只运行表单校验测试
python -m pytest test_mock_unit.py::TestSubmitScoreValidation -v

# 只运行某个具体用例
python -m pytest test_mock_unit.py::TestScoreStatusDisplay::test_status_0_pending -v

# 按关键字过滤
python -m pytest test_mock_unit.py -v -k "filter"
python -m pytest test_mock_unit.py -v -k "status or level"
```

### 生成测试报告

```bash
# 文本报告（保存到文件）
python -m pytest test_mock_unit.py -v --tb=short 2>&1 | tee reports/miniprogram_unit_test_report.txt

# JUnit XML 报告（兼容 CI/CD）
python -m pytest test_mock_unit.py -v --junitxml=reports/miniprogram_unit_test_report.xml

# HTML 报告
python -m pytest test_mock_unit.py -v --html=reports/miniprogram_unit_test_report.html --self-contained-html
```

---

## 🔗 如何运行集成测试（需要启动后端）

集成测试模拟小程序端完整的 HTTP 请求流程，**需要后端服务运行**。

### 前置条件

1. 启动后端 Spring Boot 服务（默认 `http://localhost:8080/second-class`）
2. 测试数据库中有可用的学生账号（默认：`20231012023` / `123456`）
3. 赛事、赛项、级别等基础数据已初始化

### 运行集成测试

```bash
cd tests/miniprogram

# 运行业务流程集成测试
python -m pytest test_miniprogram.py -v --tb=short

# 运行 API 集成测试
python -m pytest test_api_miniprogram.py -v --tb=short

# 运行所有集成测试
python -m pytest test_miniprogram.py test_api_miniprogram.py -v --tb=short
```

### 后端不可用时的行为

- Mock 单元测试：**正常运行**，不依赖后端
- 集成测试：自动跳过所有用例，并输出提示信息：

```
SKIPPED ... 后端服务 http://localhost:8080/second-class 未启动，跳过测试
```

---

## 📋 测试用例列表

### Mock 单元测试（test_mock_unit.py，共 35 个用例）

| 测试类 | 用例 ID | 用例名称 | 测试内容 |
|--------|---------|----------|----------|
| **TestLoginFlowMock** | TC-MOCK-LOGIN-001 | test_login_success_flow | 模拟登录成功完整流程（表单校验→API→状态保存） |
| | TC-MOCK-LOGIN-002 | test_login_failure_flow | 模拟登录失败处理（错误消息传递） |
| | TC-MOCK-LOGIN-003 | test_login_empty_username | 空学号被表单校验拦截 |
| | TC-MOCK-LOGIN-004 | test_login_empty_password | 空密码被表单校验拦截 |
| | TC-MOCK-LOGIN-005 | test_login_whitespace_only | 纯空格输入被正确拦截 |
| | TC-MOCK-LOGIN-006 | test_login_with_mock_api_call | 使用 MagicMock 模拟 API 成功/失败调用 |
| **TestSubmitScoreValidation** | TC-MOCK-SUBMIT-001 | test_all_fields_valid | 所有必填字段填写正确时校验通过 |
| | TC-MOCK-SUBMIT-002 | test_missing_event | 缺少赛事选择时报错 |
| | TC-MOCK-SUBMIT-003 | test_missing_item | 缺少赛项选择时报错 |
| | TC-MOCK-SUBMIT-004 | test_missing_level | 缺少级别选择时报错 |
| | TC-MOCK-SUBMIT-005 | test_missing_cert_date | 缺少获奖日期时报错 |
| | TC-MOCK-SUBMIT-006 | test_build_submit_form_data | 表单数据构建正确性（索引→ID 映射） |
| | TC-MOCK-SUBMIT-007 | test_submit_success_response | 提交成功响应处理 |
| | TC-MOCK-SUBMIT-008 | test_submit_failure_response | 提交失败响应处理 |
| **TestEventsFilterMock** | TC-MOCK-EVENT-001 | test_empty_keyword_returns_all | 空关键词返回全部赛事 |
| | TC-MOCK-EVENT-002 | test_filter_by_exact_name | 完整名称精确过滤 |
| | TC-MOCK-EVENT-003 | test_filter_case_insensitive | 大小写不敏感过滤 |
| | TC-MOCK-EVENT-004 | test_filter_partial_match | 部分关键词包含匹配 |
| | TC-MOCK-EVENT-005 | test_filter_no_match | 无匹配返回空列表 |
| | TC-MOCK-EVENT-006 | test_filter_multiple_results | 多结果过滤正确 |
| | TC-MOCK-EVENT-007 | test_filter_empty_events_list | 空赛事列表不报错 |
| | TC-MOCK-EVENT-008 | test_filter_name_field_missing | name 字段缺失时安全处理 |
| **TestScoreStatusDisplay** | TC-MOCK-STATUS-001 | test_status_0_pending | 状态 0 → 待审核 / tag-warning |
| | TC-MOCK-STATUS-002 | test_status_1_approved | 状态 1 → 已通过 / tag-success |
| | TC-MOCK-STATUS-003 | test_status_2_rejected | 状态 2 → 已拒绝 / tag-danger |
| | TC-MOCK-STATUS-004 | test_status_null_pending | null 状态 → 待审核 / tag-warning |
| | TC-MOCK-STATUS-005 | test_status_unknown | 未知状态 → 未知 / tag-warning |
| | TC-MOCK-STATUS-006 | test_batch_status_mapping | 批量成绩记录状态映射 |
| | TC-MOCK-STATUS-007 | test_status_display_in_score_list | 成绩列表页面状态显示 |
| **TestLevelOptionsMap** | TC-MOCK-LEVEL-001 | test_level_id_to_name | 级别 ID → 名称映射 |
| | TC-MOCK-LEVEL-002 | test_level_id_to_index | 级别 ID → 积分系数映射 |
| | TC-MOCK-LEVEL-003 | test_level_data_consistency | 级别数据完整性验证 |
| | TC-MOCK-LEVEL-004 | test_level_sorted_by_index_desc | 级别按积分系数降序排列 |
| | TC-MOCK-LEVEL-005 | test_level_names_unique | 级别名称唯一性验证 |
| | TC-MOCK-LEVEL-006 | test_level_selected_index_to_id | 选中索引→级别 ID 转换 |

### 集成测试用例

#### test_miniprogram.py（业务流程集成）

| 测试类 | 用例 ID | 用例名称 | 测试内容 |
|--------|---------|----------|----------|
| **TestStudentLogin** | TC-MP-LOGIN-001 | test_student_login | 学生正常登录流程 |
| | TC-MP-LOGIN-002 | test_login_with_invalid_password | 错误密码登录被拒绝 |
| | TC-MP-LOGIN-003 | test_login_with_empty_username | 空用户名参数校验 |
| **TestEventsList** | TC-MP-EVENT-001 | test_events_list | 赛事列表加载 |
| | TC-MP-EVENT-002 | test_event_items_chain | 赛事→赛项级联查询 |
| | TC-MP-EVENT-003 | test_all_levels | 获奖级别列表获取 |
| **TestSubmitScoreFlow** | TC-MP-SUBMIT-001 | test_submit_score_flow | 完整成绩提交流程 |
| | TC-MP-SUBMIT-002 | test_submit_score_missing_fields | 缺少必填字段提交 |
| **TestMyScoresDisplay** | TC-MP-SCORES-001 | test_my_scores_display | 我的成绩列表获取 |
| | TC-MP-SCORES-002 | test_my_scores_with_query_param | query 参数方式查询 |
| **TestTotalScore** | TC-MP-TOTAL-001 | test_total_score | 总积分获取 |
| | TC-MP-TOTAL-002 | test_total_score_with_query_param | query 参数方式查询总积分 |

#### test_api_miniprogram.py（API 集成）

| 测试类 | 用例 ID | 用例名称 | 测试内容 |
|--------|---------|----------|----------|
| **TestLoginThenQueryScores** | TC-MP-FLOW-001 | test_login_then_query_scores | 登录→查询成绩完整流程 |
| **TestScoreSubmitWithCert** | TC-MP-FLOW-002 | test_score_submit_with_cert | 成绩提交（含证书路径）流程 |
| | TC-MP-FLOW-003 | test_score_submit_without_cert_path | 无证书路径成绩提交 |
| **TestEventsItemsChain** | TC-MP-FLOW-004 | test_events_items_chain | 赛事→赛项级联查询 |
| | TC-MP-FLOW-005 | test_single_event_item_detail | 单赛事赛项详情验证 |

---

## 🧩 业务函数与小程序源码映射

Mock 单元测试覆盖的业务逻辑函数来源于以下小程序源码文件：

| 业务函数 | 来源文件 | 功能说明 |
|----------|----------|----------|
| `filter_events()` | `pages/events/events.js` | 赛事列表关键词过滤 |
| `get_audit_status_text()` | `utils/util.js` | 审核状态文字映射（0→待审核/1→已通过/2→已拒绝） |
| `get_audit_status_class()` | `utils/util.js` | 审核状态 CSS 类名映射 |
| `validate_login_form()` | `pages/login/login.js` | 登录表单校验（学号/密码非空） |
| `validate_submit_form()` | `pages/submit/submit.js` | 成绩提交表单校验（四个必填项） |
| `build_submit_form_data()` | `pages/submit/submit.js` | 构建提交表单数据（索引→ID 转换） |

---

## ❓ 常见问题

**Q1: 单元测试全部跳过？**
> 检查是否通过 `conftest.py` 中的 mock 检测逻辑。确保在 `test_mock_unit.py` 中运行测试，文件名包含 "mock" 会自动跳过后端检查。

**Q2: 集成测试报错 "后端服务未启动"？**
> 需要启动后端 Spring Boot 服务：`cd Hongmeng && mvn spring-boot:run`
> 或通过环境变量 `BACKEND_URL` 指定正确的后端地址。

**Q3: 如何添加新的 Mock 单元测试？**
> 在 `test_mock_unit.py` 中添加新的测试类和方法，或创建新的 `test_mock_xxx.py` 文件。文件名包含 "mock" 即可自动跳过后端检查。

**Q4: pytest 配置警告 "Unknown config option: verbosity"？**
> 这是 `pytest.ini` 中的配置项名称变更导致的警告，不影响测试执行。可将 `verbosity` 改为 `verbosity` 或删除该行。

---

## 📊 最近测试结果

### Mock 单元测试（无需后端）

```
test_mock_unit.py .... 35 passed, 1 warning in 8.32s
```

生成的报告文件位于 `tests/reports/miniprogram_unit_test_report.txt`。

---

## 📝 License

MIT License - 仅供学习和测试使用。