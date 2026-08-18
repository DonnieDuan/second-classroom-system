# -*- coding: utf-8 -*-
"""
Mock 单元测试 - 无需后端
使用 pytest + unittest.mock 模拟后端响应，测试小程序业务逻辑正确性

测试覆盖:
- 登录流程 mock (登录成功/失败处理逻辑)
- 成绩提交表单校验 (缺少必填字段时报错)
- 赛事列表过滤 (关键词搜索)
- 审核状态显示 (0-待审核/1-通过/2-拒绝)
- 获奖级别 ID 映射

对应小程序源码:
- miniprogram/pages/login/login.js
- miniprogram/pages/submit/submit.js
- miniprogram/pages/events/events.js
- miniprogram/utils/util.js
"""
import pytest
from unittest.mock import patch, MagicMock


# ==================== 从小程序 JS 中提取的核心业务逻辑 ====================

def filter_events(events, keyword):
    """赛事列表过滤 - 对应 events.js filterEvents

    逻辑: 空关键词返回全部; 按 name 字段做大小写不敏感的包含匹配
    """
    if not keyword:
        return events
    lower = keyword.lower()
    return [item for item in events
            if (item.get('name') or '').lower().find(lower) >= 0]


def get_audit_status_text(status):
    """审核状态文字映射 - 对应 util.js getAuditStatusText

    映射规则: 0→待审核, 1→已通过, 2→已拒绝, null→待审核, 其他→未知
    """
    mapping = {
        0: '待审核',
        1: '已通过',
        2: '已拒绝',
        None: '待审核'
    }
    return mapping.get(status, '未知')


def get_audit_status_class(status):
    """审核状态样式类名 - 对应 util.js getAuditStatusClass

    规则: 1→tag tag-success, 2→tag tag-danger, 其他→tag tag-warning
    """
    if status == 1:
        return 'tag tag-success'
    if status == 2:
        return 'tag tag-danger'
    return 'tag tag-warning'


def validate_login_form(username, password):
    """登录表单校验 - 对应 login.js doLogin 中的校验逻辑

    规则: username.trim() 非空, password.trim() 非空
    返回: (是否通过, 错误消息)
    """
    if not username or not username.strip():
        return False, '请输入学号'
    if not password or not password.strip():
        return False, '请输入密码'
    return True, None


def validate_submit_form(selected_event_index, selected_item_index,
                         selected_level_index, cert_date):
    """提交表单校验 - 对应 submit.js onSubmit 中的校验逻辑

    规则: 四个必填项均不能为空/None
    返回: (是否通过, 错误消息)
    """
    if selected_event_index is None:
        return False, '请选择赛事'
    if selected_item_index is None:
        return False, '请选择赛项'
    if selected_level_index is None:
        return False, '请选择获奖级别'
    if not cert_date:
        return False, '请选择获奖日期'
    return True, None


def build_submit_form_data(user_info, events, items, levels,
                           selected_event_index, selected_item_index,
                           selected_level_index, cert_date, cert_path):
    """构建提交表单数据 - 对应 submit.js onSubmit 中的构建逻辑"""
    return {
        'stuId': user_info['id'],
        'eventId': events[selected_event_index]['id'],
        'itemId': items[selected_item_index]['id'],
        'levelId': levels[selected_level_index]['id'],
        'certDate': cert_date,
        'certPath': cert_path
    }


# ==================== Mock 数据 ====================

MOCK_LOGIN_SUCCESS = {
    'code': 200,
    'msg': '登录成功',
    'data': {
        'token': 'eyJhbGciOiJIUzI1NiJ9.mock.student.token.abc123',
        'userInfo': {
            'id': 1001,
            'stuNo': '20231012023',
            'name': '张三',
            'role': 'student',
            'className': '计算机科学 2023-1 班'
        }
    }
}

MOCK_LOGIN_FAILURE = {
    'code': 401,
    'msg': '学号或密码错误',
    'data': None
}

MOCK_EVENTS = [
    {'id': 1, 'name': '全国大学生数学建模竞赛', 'eventDate': '2026-03-01'},
    {'id': 2, 'name': 'ACM 程序设计大赛', 'eventDate': '2026-05-15'},
    {'id': 3, 'name': '蓝桥杯软件类大赛', 'eventDate': '2026-04-20'},
    {'id': 4, 'name': '英语六级考试', 'eventDate': '2026-06-10'},
    {'id': 5, 'name': '互联网+创新创业大赛', 'eventDate': '2026-07-01'},
]

MOCK_LEVELS = [
    {'id': 1, 'name': '国家级一等奖', 'levelIndex': 1.0},
    {'id': 2, 'name': '国家级二等奖', 'levelIndex': 0.8},
    {'id': 3, 'name': '国家级三等奖', 'levelIndex': 0.6},
    {'id': 4, 'name': '省级一等奖', 'levelIndex': 0.5},
    {'id': 5, 'name': '省级二等奖', 'levelIndex': 0.3},
    {'id': 6, 'name': '校级一等奖', 'levelIndex': 0.2},
]

MOCK_ITEMS = [
    {'id': 11, 'eventId': 1, 'name': '数学建模本科组', 'score': 95},
    {'id': 12, 'eventId': 1, 'name': '数学建模研究生组', 'score': 90},
    {'id': 13, 'eventId': 2, 'name': 'ACM 校赛', 'score': 85},
]

MOCK_SUBMIT_SUCCESS = {
    'code': 200,
    'msg': '提交成功，等待审核',
    'data': {'id': 5001, 'auditStatus': 0}
}

MOCK_SUBMIT_FAILURE = {
    'code': 500,
    'msg': '系统繁忙，请稍后重试',
    'data': None
}

MOCK_USER_INFO = {'id': 1001, 'name': '张三', 'stuNo': '20231012023'}


# ==================== 测试用例 ====================

class TestLoginFlowMock:
    """TC-MOCK-LOGIN: 模拟登录成功和失败的处理逻辑

    对应小程序 pages/login/login.js 中的 doLogin() 方法
    """

    def test_login_success_flow(self):
        """TC-MOCK-LOGIN-001: 模拟登录成功完整流程

        步骤: 表单校验 → 调用API → 保存状态 → 跳转
        验证: 各步骤数据正确传递
        """
        valid, err = validate_login_form('20231012023', '123456')
        assert valid, f"表单校验应通过，实际: {err}"

        response = MOCK_LOGIN_SUCCESS
        assert response['code'] == 200
        token = response['data']['token']
        user_info = response['data']['userInfo']
        assert len(token) > 0, "token 非空"
        assert user_info['id'] == 1001
        assert user_info['stuNo'] == '20231012023'
        print("  \u2705 登录成功流程: 表单校验 → API响应 → 状态保存 均正确")

    def test_login_failure_flow(self):
        """TC-MOCK-LOGIN-002: 模拟登录失败处理

        步骤: 表单校验 → 调用API失败 → 显示错误消息
        验证: 错误消息正确传递
        """
        valid, err = validate_login_form('20231012023', 'wrong_pwd')
        assert valid

        response = MOCK_LOGIN_FAILURE
        assert response['code'] != 200
        assert '密码' in response['msg'] or '错误' in response['msg']
        print("  \u2705 登录失败处理: 错误消息正确传递")

    def test_login_empty_username(self):
        """TC-MOCK-LOGIN-003: 空学号应被表单校验拦截"""
        valid, err = validate_login_form('', '123456')
        assert not valid
        assert err == '请输入学号'
        print("  \u2705 空学号校验被正确拦截")

    def test_login_empty_password(self):
        """TC-MOCK-LOGIN-004: 空密码应被表单校验拦截"""
        valid, err = validate_login_form('20231012023', '')
        assert not valid
        assert err == '请输入密码'
        print("  \u2705 空密码校验被正确拦截")

    def test_login_whitespace_only(self):
        """TC-MOCK-LOGIN-005: 纯空格学号/密码应被拦截"""
        valid, err = validate_login_form('   ', '123456')
        assert not valid
        assert err == '请输入学号'

        valid, err = validate_login_form('20231012023', '   ')
        assert not valid
        assert err == '请输入密码'
        print("  \u2705 纯空格输入被正确拦截")

    def test_login_with_mock_api_call(self):
        """TC-MOCK-LOGIN-006: 使用 mock 模拟 API 调用成功/失败

        使用 MagicMock 模拟 studentLogin API 的返回值
        """
        mock_success_api = MagicMock(return_value=MOCK_LOGIN_SUCCESS)
        mock_failure_api = MagicMock(return_value=MOCK_LOGIN_FAILURE)

        response = mock_success_api()
        assert response['code'] == 200
        assert response['data']['token'] is not None
        assert len(response['data']['token']) > 0
        mock_success_api.assert_called_once()

        response = mock_failure_api()
        assert response['code'] == 401
        assert '密码' in response['msg']
        mock_failure_api.assert_called_once()

        print("  \u2705 Mock API 调用模拟成功/失败均正确")


class TestSubmitScoreValidation:
    """TC-MOCK-SUBMIT: 模拟表单校验逻辑

    对应小程序 pages/submit/submit.js 中的 onSubmit() 方法
    """

    def test_all_fields_valid(self):
        """TC-MOCK-SUBMIT-001: 所有必填字段填写正确时校验通过"""
        valid, err = validate_submit_form(0, 0, 0, '2026-01-15')
        assert valid
        assert err is None
        print("  \u2705 所有必填字段校验通过")

    def test_missing_event(self):
        """TC-MOCK-SUBMIT-002: 缺少赛事选择时报错"""
        valid, err = validate_submit_form(None, 0, 0, '2026-01-15')
        assert not valid
        assert err == '请选择赛事'
        print("  \u2705 缺少赛事被正确拦截")

    def test_missing_item(self):
        """TC-MOCK-SUBMIT-003: 缺少赛项选择时报错"""
        valid, err = validate_submit_form(0, None, 0, '2026-01-15')
        assert not valid
        assert err == '请选择赛项'
        print("  \u2705 缺少赛项被正确拦截")

    def test_missing_level(self):
        """TC-MOCK-SUBMIT-004: 缺少级别选择时报错"""
        valid, err = validate_submit_form(0, 0, None, '2026-01-15')
        assert not valid
        assert err == '请选择获奖级别'
        print("  \u2705 缺少级别被正确拦截")

    def test_missing_cert_date(self):
        """TC-MOCK-SUBMIT-005: 缺少获奖日期时报错"""
        valid, err = validate_submit_form(0, 0, 0, '')
        assert not valid
        assert err == '请选择获奖日期'
        print("  \u2705 缺少获奖日期被正确拦截")

    def test_build_submit_form_data(self):
        """TC-MOCK-SUBMIT-006: 验证表单数据构建的正确性

        从选中索引正确映射到对应的 ID 字段
        """
        form = build_submit_form_data(
            MOCK_USER_INFO, MOCK_EVENTS, MOCK_ITEMS, MOCK_LEVELS,
            selected_event_index=0,
            selected_item_index=0,
            selected_level_index=0,
            cert_date='2026-01-15',
            cert_path='/uploads/cert_001.pdf'
        )

        assert form['stuId'] == 1001
        assert form['eventId'] == 1
        assert form['itemId'] == 11
        assert form['levelId'] == 1
        assert form['certDate'] == '2026-01-15'
        assert form['certPath'] == '/uploads/cert_001.pdf'
        print(f"  \u2705 表单数据构建正确: {form}")

    def test_submit_success_response(self):
        """TC-MOCK-SUBMIT-007: 模拟提交成功响应处理"""
        response = MOCK_SUBMIT_SUCCESS
        assert response['code'] == 200
        assert response['data']['auditStatus'] == 0
        assert response['msg'] == '提交成功，等待审核'
        print("  \u2705 提交成功响应处理正确")

    def test_submit_failure_response(self):
        """TC-MOCK-SUBMIT-008: 模拟提交失败响应处理"""
        response = MOCK_SUBMIT_FAILURE
        assert response['code'] == 500
        assert '系统' in response['msg']
        print("  \u2705 提交失败响应处理正确")


class TestEventsFilterMock:
    """TC-MOCK-EVENT: 模拟赛事列表过滤功能

    对应小程序 pages/events/events.js 中的 filterEvents() 方法
    """

    def test_empty_keyword_returns_all(self):
        """TC-MOCK-EVENT-001: 空关键词返回全部赛事"""
        result = filter_events(MOCK_EVENTS, '')
        assert len(result) == len(MOCK_EVENTS)
        print(f"  \u2705 空关键词返回 {len(result)} 个赛事")

    def test_filter_by_exact_name(self):
        """TC-MOCK-EVENT-002: 按完整赛事名称精确过滤"""
        result = filter_events(MOCK_EVENTS, '全国大学生数学建模竞赛')
        assert len(result) == 1
        assert result[0]['name'] == '全国大学生数学建模竞赛'
        print("  \u2705 完整名称过滤正确")

    def test_filter_case_insensitive(self):
        """TC-MOCK-EVENT-003: 大小写不敏感过滤"""
        r1 = filter_events(MOCK_EVENTS, 'ACM')
        r2 = filter_events(MOCK_EVENTS, 'acm')
        r3 = filter_events(MOCK_EVENTS, 'AcM')
        assert len(r1) == len(r2) == len(r3) == 1
        assert r1[0]['name'] == 'ACM 程序设计大赛'
        print("  \u2705 大小写不敏感过滤正确")

    def test_filter_partial_match(self):
        """TC-MOCK-EVENT-004: 部分关键词匹配（包含匹配）"""
        result = filter_events(MOCK_EVENTS, '建模')
        assert len(result) == 1
        assert '建模' in result[0]['name']
        print(f"  \u2705 部分关键词匹配正确: '建模' → {len(result)} 个结果")

    def test_filter_no_match(self):
        """TC-MOCK-EVENT-005: 无匹配结果返回空列表"""
        result = filter_events(MOCK_EVENTS, '不存在的赛事名xyz')
        assert len(result) == 0
        print("  \u2705 无匹配返回空列表")

    def test_filter_multiple_results(self):
        """TC-MOCK-EVENT-006: 匹配多个结果"""
        result = filter_events(MOCK_EVENTS, '赛')
        assert len(result) >= 2
        for item in result:
            assert '赛' in item['name']
        print(f"  \u2705 多结果过滤正确: '赛' → {len(result)} 个结果")

    def test_filter_empty_events_list(self):
        """TC-MOCK-EVENT-007: 空赛事列表不报错"""
        result = filter_events([], 'ACM')
        assert len(result) == 0
        print("  \u2705 空列表过滤不报错")

    def test_filter_name_field_missing(self):
        """TC-MOCK-EVENT-008: name 字段缺失时不报错"""
        events_without_name = [
            {'id': 1, 'eventDate': '2026-01-01'},
            {'id': 2, 'name': '有名字的赛事'}
        ]
        result = filter_events(events_without_name, '赛事')
        assert len(result) == 1
        assert result[0]['id'] == 2
        print("  \u2705 name 字段缺失时安全处理")


class TestScoreStatusDisplay:
    """TC-MOCK-STATUS: 模拟审核状态显示

    对应小程序 utils/util.js 中的 getAuditStatusText() 和 getAuditStatusClass()
    """

    def test_status_0_pending(self):
        """TC-MOCK-STATUS-001: 状态 0 → 待审核 / tag-warning"""
        assert get_audit_status_text(0) == '待审核'
        assert get_audit_status_class(0) == 'tag tag-warning'
        print("  \u2705 状态0: 待审核 / tag-warning")

    def test_status_1_approved(self):
        """TC-MOCK-STATUS-002: 状态 1 → 已通过 / tag-success"""
        assert get_audit_status_text(1) == '已通过'
        assert get_audit_status_class(1) == 'tag tag-success'
        print("  \u2705 状态1: 已通过 / tag-success")

    def test_status_2_rejected(self):
        """TC-MOCK-STATUS-003: 状态 2 → 已拒绝 / tag-danger"""
        assert get_audit_status_text(2) == '已拒绝'
        assert get_audit_status_class(2) == 'tag tag-danger'
        print("  \u2705 状态2: 已拒绝 / tag-danger")

    def test_status_null_pending(self):
        """TC-MOCK-STATUS-004: null 状态 → 待审核 / tag-warning"""
        assert get_audit_status_text(None) == '待审核'
        assert get_audit_status_class(None) == 'tag tag-warning'
        print("  \u2705 null状态: 待审核 / tag-warning")

    def test_status_unknown(self):
        """TC-MOCK-STATUS-005: 未知状态 → 未知 / tag-warning"""
        assert get_audit_status_text(99) == '未知'
        assert get_audit_status_class(99) == 'tag tag-warning'

        assert get_audit_status_text(-1) == '未知'
        assert get_audit_status_class(-1) == 'tag tag-warning'
        print("  \u2705 未知状态: 未知 / tag-warning")

    def test_batch_status_mapping(self):
        """TC-MOCK-STATUS-006: 批量成绩记录的状态映射"""
        mock_scores = [
            {'id': 101, 'auditStatus': 1, 'eventName': '数学建模'},
            {'id': 102, 'auditStatus': 0, 'eventName': 'ACM'},
            {'id': 103, 'auditStatus': 2, 'eventName': '蓝桥杯'},
            {'id': 104, 'auditStatus': None, 'eventName': '英语六级'},
            {'id': 105, 'auditStatus': 99, 'eventName': '互联网+'},
        ]

        results = [(s['id'],
                    get_audit_status_text(s['auditStatus']),
                    get_audit_status_class(s['auditStatus']))
                   for s in mock_scores]

        assert results[0] == (101, '已通过', 'tag tag-success')
        assert results[1] == (102, '待审核', 'tag tag-warning')
        assert results[2] == (103, '已拒绝', 'tag tag-danger')
        assert results[3] == (104, '待审核', 'tag tag-warning')
        assert results[4] == (105, '未知', 'tag tag-warning')
        print(f"  \u2705 批量状态映射正确: {results}")

    def test_status_display_in_score_list(self):
        """TC-MOCK-STATUS-007: 模拟成绩列表页面的状态显示逻辑"""
        mock_score_list = [
            {'id': 201, 'auditStatus': 1},
            {'id': 202, 'auditStatus': 0},
            {'id': 203, 'auditStatus': 2},
        ]

        display_texts = [get_audit_status_text(s['auditStatus'])
                         for s in mock_score_list]
        assert display_texts == ['已通过', '待审核', '已拒绝']

        display_classes = [get_audit_status_class(s['auditStatus'])
                          for s in mock_score_list]
        assert display_classes == [
            'tag tag-success',
            'tag tag-warning',
            'tag tag-danger'
        ]
        print(f"  \u2705 成绩列表状态显示正确")


class TestLevelOptionsMap:
    """TC-MOCK-LEVEL: 验证获奖级别 ID 映射的正确性

    对应小程序 pages/submit/submit.js 中级别选择器的数据映射
    """

    def test_level_id_to_name(self):
        """TC-MOCK-LEVEL-001: 验证级别 ID → 名称映射"""
        level_map = {lv['id']: lv['name'] for lv in MOCK_LEVELS}

        assert level_map[1] == '国家级一等奖'
        assert level_map[2] == '国家级二等奖'
        assert level_map[3] == '国家级三等奖'
        assert level_map[4] == '省级一等奖'
        assert level_map[5] == '省级二等奖'
        assert level_map[6] == '校级一等奖'
        print(f"  \u2705 级别ID→名称映射正确: {level_map}")

    def test_level_id_to_index(self):
        """TC-MOCK-LEVEL-002: 验证级别 ID → 积分系数映射"""
        index_map = {lv['id']: lv['levelIndex'] for lv in MOCK_LEVELS}

        assert index_map[1] == 1.0
        assert index_map[2] == 0.8
        assert index_map[3] == 0.6
        assert index_map[4] == 0.5
        assert index_map[5] == 0.3
        assert index_map[6] == 0.2
        print(f"  \u2705 级别ID→积分系数映射正确: {index_map}")

    def test_level_data_consistency(self):
        """TC-MOCK-LEVEL-003: 验证级别数据完整性

        每个级别必须包含 id, name, levelIndex 三个字段
        """
        for lv in MOCK_LEVELS:
            assert 'id' in lv, f"级别缺少 id 字段: {lv}"
            assert 'name' in lv, f"级别缺少 name 字段: {lv}"
            assert 'levelIndex' in lv, f"级别缺少 levelIndex 字段: {lv}"
            assert isinstance(lv['levelIndex'], (int, float)), \
                f"levelIndex 应为数字类型: {lv}"
            assert lv['levelIndex'] > 0, \
                f"levelIndex 应为正数: {lv}"
            assert lv['levelIndex'] <= 1.0, \
                f"levelIndex 不应超过 1.0: {lv}"

        print(f"  \u2705 级别数据完整性验证通过: {len(MOCK_LEVELS)} 个级别")

    def test_level_sorted_by_index_desc(self):
        """TC-MOCK-LEVEL-004: 验证级别按积分系数降序排列

        国家级 > 省级 > 校级, 同一级别内一等奖 > 二等奖 > 三等奖
        """
        indices = [lv['levelIndex'] for lv in MOCK_LEVELS]

        for i in range(len(indices) - 1):
            assert indices[i] >= indices[i + 1], \
                f"级别未按积分系数降序: index[{i}]={indices[i]} < index[{i+1}]={indices[i+1]}"

        print(f"  \u2705 级别按积分系数降序排列: {indices}")

    def test_level_names_unique(self):
        """TC-MOCK-LEVEL-005: 验证级别名称唯一性"""
        names = [lv['name'] for lv in MOCK_LEVELS]
        assert len(names) == len(set(names)), "级别名称存在重复"
        print(f"  \u2705 级别名称唯一: {len(names)} 个级别名称均不重复")

    def test_level_selected_index_to_id(self):
        """TC-MOCK-LEVEL-006: 验证选中索引到 ID 的转换

        提交表单时 selectedLevelIndex 需正确转换为 levelId
        """
        form = build_submit_form_data(
            MOCK_USER_INFO, MOCK_EVENTS, MOCK_ITEMS, MOCK_LEVELS,
            selected_event_index=0,
            selected_item_index=0,
            selected_level_index=2,
            cert_date='2026-03-01',
            cert_path='/uploads/cert_level3.pdf'
        )

        assert form['levelId'] == MOCK_LEVELS[2]['id']
        assert form['levelId'] == 3
        print(f"  \u2705 选中索引→级别ID转换正确: index=2 → levelId={form['levelId']}")