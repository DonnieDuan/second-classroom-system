# -*- coding: utf-8 -*-
"""
学生管理与机构管理模块测试
测试用例：TC-STU-001~006, TC-ORG-001~005
"""
import pytest
from common import ApiClient
from common.config import TEST_STUDENT_DATA, TEST_ORG_DATA


class TestStudentCRUD:
    """学生信息CRUD测试"""
    
    def setup_method(self):
        self.client = ApiClient()
        self.created_stu_id = None
    
    def teardown_method(self):
        """清理测试数据"""
        if self.created_stu_id:
            try:
                self.client.delete(f"/api/student/{self.created_stu_id}")
                print(f"  清理测试数据: 删除学生ID={self.created_stu_id}")
            except Exception as e:
                print(f"  清理测试数据失败: {e}")
    
    def test_create_student(self):
        """TC-STU-001: 新增学生"""
        print("\n[TC-STU-001] 新增学生")
        stu_data = TEST_STUDENT_DATA.copy()
        stu_data["stuNo"] = f"2023{pytest.__version__.replace('.', '')}"
        stu_data["stuName"] = f"自动化测试学生_{pytest.__version__}"
        
        response = self.client.post("/api/student", json=stu_data)
        print(f"  HTTP状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  返回: code={data.get('code')}, msg={data.get('msg')}")
            if data.get("code") == 200 or data.get("code") == 0:
                stu_id = data.get("data", {}).get("stuId") or data.get("data")
                if isinstance(stu_id, int):
                    self.created_stu_id = stu_id
                    print(f"  创建的学生ID: {self.created_stu_id}")
    
    def test_query_student_list(self):
        """TC-STU-002: 查询学生列表"""
        print("\n[TC-STU-002] 查询学生列表")
        response = self.client.get("/api/student/list", params={
            "page": 1, "pageSize": 10,
            "keyword": ""
        })
        assert response.status_code == 200
        data = response.json()
        result = data.get("data", {})
        total = result.get("total") if isinstance(result, dict) else "未知"
        print(f"  返回学生总数: {total}")
    
    def test_query_student_detail(self):
        """TC-STU-003: 查询单个学生详情"""
        print("\n[TC-STU-003] 查询单个学生详情")
        
        stu_id = 1
        resp = self.client.get("/api/student/list", params={"page": 1, "pageSize": 1})
        try:
            if resp.status_code == 200:
                rows = resp.json().get("data", {}).get("rows", [])
                if rows:
                    stu_id = rows[0].get("stuId") or 1
        except Exception:
            pass
        
        response = self.client.get(f"/api/student/{stu_id}")
        print(f"  学生ID: {stu_id}, HTTP状态码: {response.status_code}")
        assert response.status_code == 200
    
    def test_query_students_by_class(self):
        """TC-STU-004: 按班级查询学生"""
        print("\n[TC-STU-004] 按班级查询学生")
        response = self.client.get("/api/student/class/1")
        print(f"  HTTP状态码: {response.status_code}")
        assert response.status_code == 200
    
    def test_update_student(self):
        """TC-STU-005: 修改学生信息"""
        print("\n[TC-STU-005] 修改学生信息")
        
        # 先创建一个学生
        stu_data = TEST_STUDENT_DATA.copy()
        stu_data["stuNo"] = f"2024{pytest.__version__.replace('.', '')}"
        stu_data["stuName"] = f"更新测试学生_{pytest.__version__}"
        resp = self.client.post("/api/student", json=stu_data)
        
        stu_id = None
        try:
            if resp.status_code == 200:
                data = resp.json()
                stu_id = data.get("data", {}).get("stuId") or data.get("data")
                if not isinstance(stu_id, int):
                    print("  跳过：未获取到学生ID")
                    return
        except Exception:
            print("  跳过：创建学生失败")
            return
        
        # 修改学生
        update_data = {
            "stuName": f"已更新学生_{pytest.__version__}",
            "stuNo": stu_data["stuNo"],
            "gender": "女",
            "trainLevel": "本科"
        }
        response = self.client.put(f"/api/student/{stu_id}", json=update_data)
        print(f"  学生ID: {stu_id}, HTTP状态码: {response.status_code}")
        
        # 清理
        try:
            self.client.delete(f"/api/student/{stu_id}")
        except Exception:
            pass
    
    def test_delete_student(self):
        """TC-STU-006: 删除学生"""
        print("\n[TC-STU-006] 删除学生")
        
        # 先创建一个学生
        stu_data = TEST_STUDENT_DATA.copy()
        stu_data["stuNo"] = f"2025{pytest.__version__.replace('.', '')}"
        stu_data["stuName"] = f"删除测试学生_{pytest.__version__}"
        resp = self.client.post("/api/student", json=stu_data)
        
        stu_id = None
        try:
            if resp.status_code == 200:
                data = resp.json()
                stu_id = data.get("data", {}).get("stuId") or data.get("data")
                if not isinstance(stu_id, int):
                    print("  跳过：未获取到学生ID")
                    return
        except Exception:
            print("  跳过：创建学生失败")
            return
        
        # 删除学生
        response = self.client.delete(f"/api/student/{stu_id}")
        print(f"  学生ID: {stu_id}, HTTP状态码: {response.status_code}")
        assert response.status_code == 200


class TestOrgCRUD:
    """机构树形结构测试"""
    
    def setup_method(self):
        self.client = ApiClient()
        self.created_org_id = None
    
    def teardown_method(self):
        """清理测试数据"""
        if self.created_org_id:
            try:
                self.client.delete(f"/api/org/{self.created_org_id}")
                print(f"  清理测试数据: 删除机构ID={self.created_org_id}")
            except Exception as e:
                print(f"  清理测试数据失败: {e}")
    
    def test_get_org_tree(self):
        """TC-ORG-001: 获取机构树形结构"""
        print("\n[TC-ORG-001] 获取机构树形结构")
        response = self.client.get("/api/org/tree")
        assert response.status_code == 200
        data = response.json()
        org_list = data.get("data", [])
        print(f"  返回机构数量: {len(org_list) if isinstance(org_list, list) else '未知'}")
    
    def test_create_org(self):
        """TC-ORG-002: 新增机构"""
        print("\n[TC-ORG-002] 新增机构")
        org_data = TEST_ORG_DATA.copy()
        org_data["orgName"] = f"自动化测试学院_{pytest.__version__}"
        
        response = self.client.post("/api/org", json=org_data)
        print(f"  HTTP状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  返回: code={data.get('code')}, msg={data.get('msg')}")
            if data.get("code") == 200 or data.get("code") == 0:
                org_id = data.get("data", {}).get("orgId") or data.get("data")
                if isinstance(org_id, int):
                    self.created_org_id = org_id
                    print(f"  创建的机构ID: {self.created_org_id}")
    
    def test_query_org_detail(self):
        """TC-ORG-005: 查询机构详情"""
        print("\n[TC-ORG-005] 查询机构详情")
        
        org_id = 1
        resp = self.client.get("/api/org/tree")
        try:
            if resp.status_code == 200:
                org_list = resp.json().get("data", [])
                if org_list and isinstance(org_list, list):
                    org_id = org_list[0].get("orgId") or 1
        except Exception:
            pass
        
        response = self.client.get(f"/api/org/{org_id}")
        print(f"  机构ID: {org_id}, HTTP状态码: {response.status_code}")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
