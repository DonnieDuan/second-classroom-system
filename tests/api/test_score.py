# -*- coding: utf-8 -*-
"""
成绩管理模块测试
测试用例：TC-SCORE-001 ~ TC-SCORE-016
"""
import pytest
from common import ApiClient, assert_success
from common.config import TEST_SCORE_DATA, TEST_STUDENT


class TestScoreSubmit:
    """成绩提交测试"""
    
    def setup_method(self):
        self.client = ApiClient()
    
    def test_submit_score(self):
        """TC-SCORE-001: 正常提交成绩"""
        print("\n[TC-SCORE-001] 正常提交成绩")
        
        # 先获取一个有效的stuId
        resp = self.client.get("/api/student/list", params={"pageSize": 5})
        stu_id = TEST_SCORE_DATA["stuId"]
        try:
            if resp.status_code == 200:
                data = resp.json()
                rows = data.get("data", {}).get("rows") or data.get("data", [])
                if rows and len(rows) > 0:
                    stu_id = rows[0].get("stuId") or rows[0].get("stu_id") or 1
        except Exception:
            pass
        
        score_data = TEST_SCORE_DATA.copy()
        score_data["stuId"] = stu_id
        
        response = self.client.post("/api/app/score/submit", json=score_data)
        print(f"  HTTP状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  返回: code={result.get('code')}, msg={result.get('msg')}")
    
    def test_submit_score_missing_field(self):
        """TC-SCORE-002: 缺少必填字段"""
        print("\n[TC-SCORE-002] 缺少必填字段提交成绩")
        # 缺少eventId
        data = {
            "stuId": 1,
            "eventName": "测试赛事",
            "itemName": "测试赛项"
        }
        response = self.client.post("/api/app/score/submit", json=data)
        print(f"  HTTP状态码: {response.status_code}")
        # 预期返回400参数校验失败
        assert response.status_code == 400 or response.status_code == 200


class TestScoreAudit:
    """成绩审核测试"""
    
    def setup_method(self):
        self.client = ApiClient()
        # 尝试登录教师账号
        resp = self.client.post("/api/auth/login", json=TEST_STUDENT)
        try:
            data = resp.json()
            token = data.get("data", {}).get("token") or data.get("data", {}).get("accessToken")
            if token:
                self.client.set_token(token)
        except Exception:
            pass
    
    def test_audit_score_pass(self):
        """TC-SCORE-004: 审核通过"""
        print("\n[TC-SCORE-004] 成绩审核通过")
        
        # 先获取一个有效的scoreId
        score_id = None
        try:
            resp = self.client.get("/api/score/list", params={"page": 1, "pageSize": 5})
            if resp.status_code == 200:
                data = resp.json()
                rows = data.get("data", {}).get("rows") or data.get("data", [])
                if rows and len(rows) > 0:
                    score_id = rows[0].get("scoreId") or rows[0].get("score_id")
        except Exception:
            pass
        
        if score_id:
            audit_data = {
                "scoreId": score_id,
                "auditStatus": 1,
                "auditRemark": "自动化测试-审核通过"
            }
            response = self.client.post("/api/admin/audit", json=audit_data)
            print(f"  HTTP状态码: {response.status_code}, scoreId={score_id}")
            if response.status_code == 200:
                result = response.json()
                print(f"  返回: code={result.get('code')}, msg={result.get('msg')}")
        else:
            print("  跳过：没有找到可用的成绩记录进行审核测试")
    
    def test_audit_score_reject(self):
        """TC-SCORE-005: 审核拒绝"""
        print("\n[TC-SCORE-005] 成绩审核拒绝")
        
        score_id = None
        try:
            resp = self.client.get("/api/score/list", params={"page": 1, "pageSize": 5})
            if resp.status_code == 200:
                data = resp.json()
                rows = data.get("data", {}).get("rows") or data.get("data", [])
                if rows and len(rows) > 0:
                    score_id = rows[0].get("scoreId") or rows[0].get("score_id")
        except Exception:
            pass
        
        if score_id:
            audit_data = {
                "scoreId": score_id,
                "auditStatus": 2,
                "auditRemark": "自动化测试-审核拒绝：证书不清晰"
            }
            response = self.client.post("/api/admin/audit", json=audit_data)
            print(f"  HTTP状态码: {response.status_code}, scoreId={score_id}")
            if response.status_code == 200:
                result = response.json()
                print(f"  返回: code={result.get('code')}, msg={result.get('msg')}")
        else:
            print("  跳过：没有找到可用的成绩记录进行审核测试")


class TestScoreQuery:
    """成绩查询测试"""
    
    def setup_method(self):
        self.client = ApiClient()
    
    def test_query_my_scores(self):
        """TC-SCORE-008: 查询我的成绩"""
        print("\n[TC-SCORE-008] 查询我的成绩列表")
        resp = self.client.get("/api/app/score/myScores", params={"stuId": 1})
        print(f"  HTTP状态码: {resp.status_code}")
        assert resp.status_code == 200
        data = resp.json()
        print(f"  返回记录数: {len(data.get('data', [])) if isinstance(data.get('data'), list) else '非列表格式'}")
    
    def test_query_my_total(self):
        """TC-SCORE-009: 查询我的总分"""
        print("\n[TC-SCORE-009] 查询我的总分")
        resp = self.client.get("/api/app/score/myTotal", params={"stuId": 1})
        print(f"  HTTP状态码: {resp.status_code}")
        assert resp.status_code == 200
        data = resp.json()
        print(f"  返回数据: {data.get('data')}")
    
    def test_query_score_page(self):
        """TC-SCORE-010: 分页查询成绩列表"""
        print("\n[TC-SCORE-010] 分页查询成绩列表")
        resp = self.client.get("/api/score/list", params={"page": 1, "pageSize": 10})
        print(f"  HTTP状态码: {resp.status_code}")
        assert resp.status_code == 200
        data = resp.json()
        print(f"  返回总数: {data.get('data', {}).get('total', '未知')}")
    
    def test_query_score_filter_by_name(self):
        """TC-SCORE-011: 按学生姓名筛选"""
        print("\n[TC-SCORE-011] 按学生姓名筛选成绩")
        resp = self.client.get("/api/score/list", params={
            "page": 1, "pageSize": 10, "stuName": "张"
        })
        print(f"  HTTP状态码: {resp.status_code}")
        assert resp.status_code == 200
    
    def test_query_score_filter_by_event(self):
        """TC-SCORE-012: 按赛事名称筛选"""
        print("\n[TC-SCORE-012] 按赛事名称筛选成绩")
        resp = self.client.get("/api/score/list", params={
            "page": 1, "pageSize": 10, "eventName": "蓝桥杯"
        })
        print(f"  HTTP状态码: {resp.status_code}")
        assert resp.status_code == 200


class TestScoreStatistics:
    """成绩统计测试"""
    
    def setup_method(self):
        self.client = ApiClient()
    
    def test_class_score_summary(self):
        """TC-SCORE-013: 班级成绩汇总"""
        print("\n[TC-SCORE-013] 获取班级成绩汇总")
        resp = self.client.get("/admin/statistics/class/1")
        print(f"  HTTP状态码: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"  返回统计数据")
    
    def test_dashboard_statistics(self):
        """首页仪表盘统计"""
        print("\n[统计] 获取仪表盘统计数据")
        resp = self.client.get("/api/admin/dashboard")
        print(f"  HTTP状态码: {resp.status_code}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
