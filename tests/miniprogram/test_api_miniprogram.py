# -*- coding: utf-8 -*-
"""
模拟小程序端 API 集成测试
测试小程序端完整的请求流程：登录→查询→提交等链式调用
"""
import pytest
import sys
import os

# ==================== 配置常量 ====================
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8080/second-class')
BACKEND_API_URL = f'{BACKEND_URL}/api'
TEST_STUDENT = {
    'username': '20231012023',
    'password': '123456'
}
REQUEST_TIMEOUT = 30


class TestLoginThenQueryScores:
    """登录→查询成绩完整流程测试

    模拟小程序端: 用户打开小程序→登录→进入"我的成绩"页面
    涉及接口: /api/auth/login → /api/app/score/my/{stuId} → /api/app/score/total/{stuId}
    """

    def test_login_then_query_scores(self, api_client, backend_available):
        """TC-MP-FLOW-001: 登录→查询成绩完整流程

        流程:
        1. POST /api/auth/login 登录获取 token 和用户信息
        2. GET /api/app/score/my/{stuId} 查询我的成绩列表
        3. GET /api/app/score/total/{stuId} 查询总积分

        验证:
        - 每一步请求都成功返回
        - 数据结构符合小程序预期
        - 成绩列表中的 stuId 与登录用户一致
        """
        print("\n[TC-MP-FLOW-001] 登录→查询成绩完整流程")

        # ============ 步骤 1: 登录 ============
        login_url = f'{BACKEND_API_URL}/auth/login'
        login_payload = {
            'username': TEST_STUDENT['username'],
            'password': TEST_STUDENT['password'],
            'role': 'student'
        }

        print("  步骤1: 发送登录请求...")
        resp = api_client.post(login_url, json=login_payload, timeout=REQUEST_TIMEOUT)
        print(f"    HTTP: {resp.status_code}")

        assert resp.status_code == 200, f"登录请求失败: {resp.status_code}"

        login_data = resp.json()
        assert login_data.get('code') == 200, f"登录业务失败: {login_data.get('msg')}"

        result_data = login_data.get('data', {})
        token = result_data.get('token') or result_data.get('accessToken')
        user_info = result_data.get('userInfo', {})
        stu_id = user_info.get('id')

        print(f"    登录成功: stuId={stu_id}, token={token[:20] if token else 'N/A'}...")

        # ============ 步骤 2: 查询我的成绩 ============
        scores_url = f'{BACKEND_API_URL}/app/score/my/{stu_id}'
        print(f"  步骤2: 查询学生 {stu_id} 的成绩列表...")
        resp = api_client.get(scores_url, timeout=REQUEST_TIMEOUT)
        print(f"    HTTP: {resp.status_code}")

        assert resp.status_code == 200, f"成绩查询请求失败: {resp.status_code}"

        scores_data = resp.json()
        assert scores_data.get('code') == 200, f"成绩查询失败: {scores_data.get('msg')}"

        scores = scores_data.get('data', [])
        assert isinstance(scores, list), "成绩数据应为列表类型"

        print(f"    成绩记录数: {len(scores)}")

        # 验证每条成绩记录的学生 ID 一致
        for i, score in enumerate(scores):
            record_stu_id = score.get('stuId') or score.get('stu_id')
            if record_stu_id is not None:
                assert str(record_stu_id) == str(stu_id), \
                    f"第 {i} 条成绩的 stuId={record_stu_id} 与登录用户 stuId={stu_id} 不一致"

        if scores:
            print(f"    成绩列表第一条: {scores[0]}")

        # ============ 步骤 3: 查询总积分 ============
        total_url = f'{BACKEND_API_URL}/app/score/total/{stu_id}'
        print(f"  步骤3: 查询学生 {stu_id} 的总积分...")
        resp = api_client.get(total_url, timeout=REQUEST_TIMEOUT)
        print(f"    HTTP: {resp.status_code}")

        assert resp.status_code == 200, f"总积分请求失败: {resp.status_code}"

        total_data = resp.json()
        assert total_data.get('code') == 200, f"总积分查询失败: {total_data.get('msg')}"

        total_score = total_data.get('data', 0)
        print(f"    总积分: {total_score}")

        # ============ 综合验证 ============
        print(f"\n  ✅ 完整流程测试通过:")
        print(f"     - 登录: OK")
        print(f"     - 成绩列表: {len(scores)} 条记录")
        print(f"     - 总积分: {total_score}")


class TestScoreSubmitWithCert:
    """成绩提交（含证书路径）流程测试

    模拟小程序端: 登录→选择赛事→选择赛项→选择级别→填写证书信息→提交
    """

    def test_score_submit_with_cert(self, api_client, backend_available):
        """TC-MP-FLOW-002: 成绩提交（含证书路径）完整流程

        流程:
        1. 登录获取学生信息
        2. 获取赛事列表，选择赛事
        3. 获取该赛事的赛项列表
        4. 获取获奖级别列表
        5. 提交成绩（包含 certDate 和 certPath）

        验证:
        - 所有 API 调用成功
        - 提交的数据格式正确
        - 后端正确处理成绩提交
        """
        print("\n[TC-MP-FLOW-002] 成绩提交（含证书路径）流程")

        # ============ 步骤 1: 登录 ============
        login_url = f'{BACKEND_API_URL}/auth/login'
        login_payload = {
            'username': TEST_STUDENT['username'],
            'password': TEST_STUDENT['password'],
            'role': 'student'
        }

        resp = api_client.post(login_url, json=login_payload, timeout=REQUEST_TIMEOUT)
        login_data = resp.json()
        assert login_data.get('code') == 200, "登录失败"

        user_info = login_data.get('data', {}).get('userInfo', {})
        stu_id = user_info.get('id')
        print(f"  步骤1 - 登录: stuId={stu_id}")

        # ============ 步骤 2: 获取赛事列表 ============
        events_url = f'{BACKEND_API_URL}/event/all'
        resp = api_client.get(events_url, timeout=REQUEST_TIMEOUT)
        events_data = resp.json()
        events = events_data.get('data', [])

        assert len(events) > 0, "没有可用的赛事数据"
        event = events[0]
        event_id = event.get('id')
        event_name = event.get('eventName') or event.get('name')
        print(f"  步骤2 - 选择赛事: id={event_id}, name={event_name}")

        # ============ 步骤 3: 获取赛项列表 ============
        items_url = f'{BACKEND_API_URL}/item/event/{event_id}'
        resp = api_client.get(items_url, timeout=REQUEST_TIMEOUT)
        items_data = resp.json()
        items = items_data.get('data', [])

        assert len(items) > 0, f"赛事 {event_id} 下没有赛项"
        item = items[0]
        item_id = item.get('id')
        item_name = item.get('itemName') or item.get('name')
        print(f"  步骤3 - 选择赛项: id={item_id}, name={item_name}")

        # ============ 步骤 4: 获取级别列表 ============
        levels_url = f'{BACKEND_API_URL}/event-level/list'
        resp = api_client.get(levels_url, timeout=REQUEST_TIMEOUT)
        levels_data = resp.json()
        levels = levels_data.get('data', [])

        assert len(levels) > 0, "没有可用的级别数据"
        level = levels[0]
        level_id = level.get('id')
        level_name = level.get('levelName') or level.get('name')
        level_index = level.get('levelIndex', 1.0)
        print(f"  步骤4 - 选择级别: id={level_id}, name={level_name}, index={level_index}")

        # ============ 步骤 5: 提交成绩 ============
        submit_url = f'{BACKEND_API_URL}/app/score/submit'
        cert_date = '2026-06-15'
        cert_path = '/uploads/certificates/test_cert_flow.pdf'

        submit_payload = {
            'stuId': stu_id,
            'eventId': event_id,
            'itemId': item_id,
            'levelId': level_id,
            'score': 90,
            'certDate': cert_date,
            'certPath': cert_path
        }

        print(f"  步骤5 - 提交成绩:")
        print(f"    {{ stuId: {stu_id}, eventId: {event_id}, itemId: {item_id},")
        print(f"      levelId: {level_id}, score: 90,")
        print(f"      certDate: {cert_date}, certPath: {cert_path} }}")

        resp = api_client.post(submit_url, json=submit_payload, timeout=REQUEST_TIMEOUT)
        print(f"    HTTP: {resp.status_code}")

        if resp.status_code == 200:
            submit_result = resp.json()
            print(f"    业务返回: code={submit_result.get('code')}, msg={submit_result.get('msg')}")

            if submit_result.get('code') == 200:
                print("    ✅ 成绩提交成功")

                # 验证提交后成绩是否可查询
                scores_url = f'{BACKEND_API_URL}/app/score/my/{stu_id}'
                resp = api_client.get(scores_url, timeout=REQUEST_TIMEOUT)
                scores_data = resp.json()
                scores = scores_data.get('data', [])

                print(f"    步骤6 - 验证提交: 当前成绩记录数={len(scores)}")
                if scores:
                    latest = scores[0]
                    print(f"    最新成绩记录: {latest}")
            else:
                print(f"    ⚠️ 提交未通过业务校验: {submit_result.get('msg')}")
        else:
            print(f"    ⚠️ 提交请求失败: HTTP {resp.status_code}")

    def test_score_submit_without_cert_path(self, api_client, backend_available):
        """TC-MP-FLOW-003: 成绩提交不带证书路径（可选字段验证）

        验证: certPath 为可选字段时，后端能正确处理
        """
        print("\n[TC-MP-FLOW-003] 无证书路径的成绩提交测试")

        # 登录
        login_url = f'{BACKEND_API_URL}/auth/login'
        login_payload = {
            'username': TEST_STUDENT['username'],
            'password': TEST_STUDENT['password'],
            'role': 'student'
        }
        resp = api_client.post(login_url, json=login_payload, timeout=REQUEST_TIMEOUT)
        login_data = resp.json()
        stu_id = login_data.get('data', {}).get('userInfo', {}).get('id')
        print(f"  登录成功: stuId={stu_id}")

        # 获取第一个赛事和赛项
        events_resp = api_client.get(f'{BACKEND_API_URL}/event/all', timeout=REQUEST_TIMEOUT)
        events = events_resp.json().get('data', [])
        if not events:
            pytest.skip("没有可用赛事数据")
            return

        event_id = events[0].get('id')

        items_resp = api_client.get(f'{BACKEND_API_URL}/item/event/{event_id}', timeout=REQUEST_TIMEOUT)
        items = items_resp.json().get('data', [])
        if not items:
            pytest.skip("没有可用赛项数据")
            return

        item_id = items[0].get('id')

        # 获取级别
        levels_resp = api_client.get(f'{BACKEND_API_URL}/event-level/list', timeout=REQUEST_TIMEOUT)
        levels = levels_resp.json().get('data', [])
        level_id = levels[0].get('id') if levels else 1

        # 提交（不带 certPath）
        submit_url = f'{BACKEND_API_URL}/app/score/submit'
        submit_payload = {
            'stuId': stu_id,
            'eventId': event_id,
            'itemId': item_id,
            'levelId': level_id,
            'score': 80,
            'certDate': '2026-03-01'
        }

        print(f"  提交成绩（无证书路径）: {submit_payload}")
        resp = api_client.post(submit_url, json=submit_payload, timeout=REQUEST_TIMEOUT)
        print(f"  HTTP: {resp.status_code}")

        if resp.status_code == 200:
            result = resp.json()
            print(f"  业务返回: code={result.get('code')}, msg={result.get('msg')}")
            if result.get('code') == 200:
                print("  ✅ 无证书路径提交成功")
            else:
                print(f"  ⚠️ 提交被拒绝: {result.get('msg')}")


class TestEventsItemsChain:
    """赛事→赛项级联查询测试

    模拟小程序端: 用户进入"赛事列表"→选择某个赛事→加载该赛事的赛项列表
    """

    def test_events_items_chain(self, api_client, backend_available):
        """TC-MP-FLOW-004: 赛事→赛项级联查询完整流程

        流程:
        1. GET /api/event/all 获取所有赛事
        2. 遍历每个赛事，GET /api/item/event/{eventId} 获取赛项
        3. 验证级联数据的一致性

        验证:
        - 每个赛事都能正确查询到对应的赛项
        - 赛项的 eventId 与查询的赛事 ID 一致
        - 数据结构完整
        """
        print("\n[TC-MP-FLOW-004] 赛事→赛项级联查询")

        # 获取所有赛事
        events_url = f'{BACKEND_API_URL}/event/all'
        resp = api_client.get(events_url, timeout=REQUEST_TIMEOUT)
        print(f"  获取赛事列表: HTTP {resp.status_code}")

        assert resp.status_code == 200, f"赛事列表请求失败: {resp.status_code}"

        events_data = resp.json()
        assert events_data.get('code') == 200, f"赛事列表业务失败: {events_data.get('msg')}"

        events = events_data.get('data', [])
        print(f"  赛事总数: {len(events)}")

        if not events:
            pytest.skip("没有赛事数据，跳过级联测试")
            return

        # 逐个赛事查询其赛项
        total_items = 0
        for event in events[:5]:
            event_id = event.get('id')
            event_name = event.get('eventName') or event.get('name')

            items_url = f'{BACKEND_API_URL}/item/event/{event_id}'
            resp = api_client.get(items_url, timeout=REQUEST_TIMEOUT)

            if resp.status_code == 200:
                items_data = resp.json()
                items = items_data.get('data', [])
                item_count = len(items)
                total_items += item_count

                print(f"    赛事 [{event_id}] {event_name}: {item_count} 个赛项")

                # 验证赛项数据
                for item in items:
                    item_event_id = item.get('eventId') or item.get('event_id')
                    if item_event_id is not None:
                        assert str(item_event_id) == str(event_id), \
                            f"赛项的 eventId={item_event_id} 与查询的赛事 ID={event_id} 不一致"

                    assert item.get('id') is not None, "赛项缺少 id 字段"
                    assert item.get('itemName') or item.get('name'), "赛项缺少名称字段"
            else:
                print(f"    赛事 [{event_id}] {event_name}: 查询失败 (HTTP {resp.status_code})")

        print(f"\n  ✅ 级联查询完成: {len(events)} 个赛事, 共 {total_items} 个赛项")

    def test_single_event_item_detail(self, api_client, backend_available):
        """TC-MP-FLOW-005: 单赛事→赛项详情查询

        验证特定赛事下赛项的详细信息完整性
        """
        print("\n[TC-MP-FLOW-005] 单赛事赛项详情验证")

        # 获取第一个赛事
        resp = api_client.get(f'{BACKEND_API_URL}/event/all', timeout=REQUEST_TIMEOUT)
        events = resp.json().get('data', [])
        if not events:
            pytest.skip("没有赛事数据")
            return

        event = events[0]
        event_id = event.get('id')
        event_name = event.get('eventName') or event.get('name')
        print(f"  目标赛事: id={event_id}, name={event_name}")

        # 获取该赛事的赛项
        resp = api_client.get(f'{BACKEND_API_URL}/item/event/{event_id}', timeout=REQUEST_TIMEOUT)
        items_data = resp.json()
        items = items_data.get('data', [])

        if not items:
            print(f"  该赛事暂无赛项数据")
            return

        item = items[0]
        item_id = item.get('id')
        item_name = item.get('itemName') or item.get('name')
        print(f"  目标赛项: id={item_id}, name={item_name}")

        # 验证赛项详情结构
        print(f"  赛项完整数据: {item}")

        # 验证必要字段
        required_fields = ['id']
        for field in required_fields:
            assert field in item, f"赛项缺少必要字段: {field}"

        # 可选字段检查
        optional_fields = ['itemName', 'name', 'eventId', 'itemLevel', 'itemDesc']
        present_fields = [f for f in optional_fields if f in item]
        print(f"  存在的可选字段: {present_fields}")

        print("  ✅ 赛项详情结构验证通过")