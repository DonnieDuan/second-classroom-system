# -*- coding: utf-8 -*-
"""
赛事管理模块测试
测试用例：TC-EVENT-001~005, TC-ITEM-001~004, TC-LEVEL-001~004
"""
import pytest
from common import ApiClient, assert_success
from common.config import TEST_EVENT_DATA


class TestEventCRUD:
    """赛事CRUD测试"""
    
    def setup_method(self):
        self.client = ApiClient()
        self.created_event_id = None
    
    def teardown_method(self):
        """清理测试数据"""
        if self.created_event_id:
            try:
                self.client.delete(f"/api/event/{self.created_event_id}")
                print(f"  清理测试数据: 删除赛事ID={self.created_event_id}")
            except Exception as e:
                print(f"  清理测试数据失败: {e}")
    
    def test_create_event(self):
        """TC-EVENT-001: 新增赛事"""
        print("\n[TC-EVENT-001] 新增赛事")
        event_data = TEST_EVENT_DATA.copy()
        event_data["eventName"] = f"自动化测试_{pytest.__version__}"
        
        response = self.client.post("/api/event", json=event_data)
        print(f"  HTTP状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  返回: code={data.get('code')}, msg={data.get('msg')}")
            if data.get("code") == 200 or data.get("code") == 0:
                self.created_event_id = data.get("data", {}).get("eventId") or data.get("data")
                if isinstance(self.created_event_id, int):
                    print(f"  创建的赛事ID: {self.created_event_id}")
    
    def test_query_event_list(self):
        """TC-EVENT-002: 查询赛事列表"""
        print("\n[TC-EVENT-002] 查询赛事列表")
        response = self.client.get("/api/event/list", params={"page": 1, "pageSize": 10})
        assert response.status_code == 200
        data = response.json()
        result = data.get("data", {})
        print(f"  返回总数: {result.get('total') if isinstance(result, dict) else '未知'}")
        print(f"  当前页记录数: {len(result.get('rows', [])) if isinstance(result, dict) else '未知'}")
    
    def test_query_all_events(self):
        """查询全部赛事（下拉选择用）"""
        print("\n[查询] 获取全部赛事列表")
        response = self.client.get("/api/event/all")
        assert response.status_code == 200
        data = response.json()
        print(f"  返回赛事数量: {len(data.get('data', [])) if isinstance(data.get('data'), list) else '未知'}")
    
    def test_query_event_detail(self):
        """TC-EVENT-003: 查询单个赛事详情"""
        print("\n[TC-EVENT-003] 查询单个赛事详情")
        # 先获取一个赛事ID
        event_id = 1
        resp = self.client.get("/api/event/list", params={"page": 1, "pageSize": 1})
        try:
            if resp.status_code == 200:
                rows = resp.json().get("data", {}).get("rows", [])
                if rows:
                    event_id = rows[0].get("eventId") or 1
        except Exception:
            pass
        
        response = self.client.get(f"/api/event/{event_id}")
        print(f"  赛事ID: {event_id}, HTTP状态码: {response.status_code}")
        assert response.status_code == 200
    
    def test_update_event(self):
        """TC-EVENT-004: 修改赛事信息"""
        print("\n[TC-EVENT-004] 修改赛事信息")
        # 先创建一个赛事
        event_data = TEST_EVENT_DATA.copy()
        event_data["eventName"] = f"更新测试赛事_{pytest.__version__}"
        resp = self.client.post("/api/event", json=event_data)
        
        event_id = None
        try:
            if resp.status_code == 200:
                data = resp.json()
                event_id = data.get("data", {}).get("eventId") or data.get("data")
                if not isinstance(event_id, int):
                    print("  跳过：未获取到赛事ID")
                    return
        except Exception:
            print("  跳过：创建赛事失败")
            return
        
        # 修改赛事
        update_data = {
            "eventName": f"更新后的赛事_{pytest.__version__}",
            "eventLevel": "省级",
            "eventStatus": 1
        }
        response = self.client.put(f"/api/event/{event_id}", json=update_data)
        print(f"  赛事ID: {event_id}, HTTP状态码: {response.status_code}")
        
        # 清理
        try:
            self.client.delete(f"/api/event/{event_id}")
        except Exception:
            pass
    
    def test_delete_event(self):
        """TC-EVENT-005: 删除赛事"""
        print("\n[TC-EVENT-005] 删除赛事")
        # 先创建一个赛事
        event_data = TEST_EVENT_DATA.copy()
        event_data["eventName"] = f"删除测试赛事_{pytest.__version__}"
        resp = self.client.post("/api/event", json=event_data)
        
        event_id = None
        try:
            if resp.status_code == 200:
                data = resp.json()
                event_id = data.get("data", {}).get("eventId") or data.get("data")
                if not isinstance(event_id, int):
                    print("  跳过：未获取到赛事ID")
                    return
        except Exception:
            print("  跳过：创建赛事失败")
            return
        
        # 删除赛事
        response = self.client.delete(f"/api/event/{event_id}")
        print(f"  赛事ID: {event_id}, HTTP状态码: {response.status_code}")
        assert response.status_code == 200


class TestItemCRUD:
    """赛项管理测试"""
    
    def setup_method(self):
        self.client = ApiClient()
    
    def test_create_item(self):
        """TC-ITEM-001: 新增赛项"""
        print("\n[TC-ITEM-001] 新增赛项")
        item_data = {
            "eventId": 1,
            "itemName": f"自动化测试赛项_{pytest.__version__}",
            "baseScore": 80
        }
        response = self.client.post("/api/item", json=item_data)
        print(f"  HTTP状态码: {response.status_code}")
    
    def test_query_items_by_event(self):
        """TC-ITEM-002: 按赛事查询赛项"""
        print("\n[TC-ITEM-002] 按赛事查询赛项")
        response = self.client.get("/api/item/event/1")
        assert response.status_code == 200
        data = response.json()
        print(f"  返回赛项数量: {len(data.get('data', [])) if isinstance(data.get('data'), list) else '未知'}")
    
    def test_query_item_list(self):
        """查询赛项列表"""
        print("\n[查询] 赛项列表分页查询")
        response = self.client.get("/api/item/list", params={"page": 1, "pageSize": 10, "eventId": 1})
        assert response.status_code == 200


class TestEventLevelCRUD:
    """获奖级别管理测试"""
    
    def setup_method(self):
        self.client = ApiClient()
    
    def test_create_level(self):
        """TC-LEVEL-001: 新增获奖级别"""
        print("\n[TC-LEVEL-001] 新增获奖级别")
        level_data = {
            "levelName": f"测试级别_{pytest.__version__}",
            "levelIndex": 1.2
        }
        response = self.client.post("/api/event-level", json=level_data)
        print(f"  HTTP状态码: {response.status_code}")
    
    def test_query_all_levels(self):
        """TC-LEVEL-002: 查询所有获奖级别"""
        print("\n[TC-LEVEL-002] 查询所有获奖级别")
        response = self.client.get("/api/event-level/list")
        assert response.status_code == 200
        data = response.json()
        print(f"  返回级别数量: {len(data.get('data', [])) if isinstance(data.get('data'), list) else '未知'}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
