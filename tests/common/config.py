# -*- coding: utf-8 -*-
"""
测试配置文件
"""
import os

# ==================== 基础配置 ====================
# 后端服务地址（注意：context-path 为 /second-class）
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080/second-class")
# 前端服务地址
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# 超时时间（秒）
REQUEST_TIMEOUT = 30

# ==================== 测试账号 ====================
TEST_STUDENT = {
    "username": "20231012023",
    "password": "123456"
}

TEST_TEACHER = {
    "username": "teacher",
    "password": "123456"
}

TEST_ADMIN = {
    "username": "admin",
    "password": "123456"
}

# ==================== 测试数据 ====================
# 测试用成绩数据
TEST_SCORE_DATA = {
    "stuId": 1,
    "eventId": 1,
    "eventName": "蓝桥杯",
    "itemId": 1,
    "itemName": "软件类",
    "levelId": 1,
    "levelName": "一等奖",
    "baseScore": 100,
    "levelIndex": 1.0,
    "finalScore": 100,
    "certDate": "2026-01-01",
    "certPath": "/uploads/test_cert.pdf"
}

# 测试用赛事数据
TEST_EVENT_DATA = {
    "eventName": "自动化测试赛事",
    "eventLevel": "校级",
    "eventStatus": 1
}

# 测试用学生数据
TEST_STUDENT_DATA = {
    "stuNo": "20231012999",
    "stuName": "测试学生",
    "gender": "男",
    "classOrgId": 1,
    "enrollYear": "2023",
    "trainLevel": "本科"
}

# 测试用机构数据
TEST_ORG_DATA = {
    "orgName": "自动化测试学院",
    "parentOrgCode": "ROOT",
    "orgLevel": 1
}
