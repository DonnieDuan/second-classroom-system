/*
 Navicat Premium Dump SQL

 Source Server         : localhost_3307
 Source Server Type    : MySQL
 Source Server Version : 80406 (8.4.6)
 Source Host           : localhost:3307
 Source Schema         : secscore

 Target Server Type    : MySQL
 Target Server Version : 80406 (8.4.6)
 File Encoding         : 65001

 Date: 26/05/2026 20:42:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for event_info
-- ----------------------------
DROP TABLE IF EXISTS `event_info`;
CREATE TABLE `event_info`  (
  `event_id` int NOT NULL AUTO_INCREMENT COMMENT '赛事主键',
  `event_no` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '赛事编号',
  `event_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '赛事名称',
  `host_unit` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '主办单位',
  `event_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '赛事等级',
  `event_desc` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '赛事说明',
  `charter_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '赛事章程（文件地址）',
  `event_status` int NOT NULL COMMENT '赛事状态：0-未开始，1-进行中，2-已结束',
  `base_score` decimal(5, 2) NOT NULL COMMENT '赛事成绩基准分',
  `back_str1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_str2` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_str3` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_int1` int NULL DEFAULT NULL COMMENT '备用字段-数字',
  `back_int2` int NULL DEFAULT NULL COMMENT '备用字段-数字',
  PRIMARY KEY (`event_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '赛事（证书）信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of event_info
-- ----------------------------
INSERT INTO `event_info` VALUES (1, 'EVT-2024-001', 'ACM国际大学生程序设计竞赛', 'ACM/ICPC基金会', '国家级', '国际顶级程序设计赛事', NULL, 2, 20.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `event_info` VALUES (2, 'EVT-2024-002', '蓝桥杯全国软件和信息技术专业人才大赛', '工业和信息化部人才交流中心', '国家级', '全国性IT类专业赛事', NULL, 2, 15.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `event_info` VALUES (3, 'EVT-2024-003', '全国大学生数学建模竞赛', '中国工业与应用数学学会', '国家级', '数学建模类赛事', NULL, 2, 15.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `event_info` VALUES (4, 'EVT-2024-004', '中国大学生计算机设计大赛', '教育部高等学校计算机类专业教指委', '国家级', '计算机综合设计赛事', NULL, 2, 12.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `event_info` VALUES (5, 'EVT-2024-005', '全国大学生信息安全竞赛', '教育部高等学校信息安全专业教指委', '国家级', '网络安全类赛事', NULL, 2, 12.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `event_info` VALUES (6, 'EVT-2024-006', '互联网+大学生创新创业大赛', '教育部', '国家级', '创新创业类综合赛事', NULL, 1, 18.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `event_info` VALUES (7, 'EVT-2024-007', '全国英语四级考试（CET-4）', '教育部考试中心', '国家级', '英语能力等级证书考试', NULL, 2, 10.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `event_info` VALUES (8, 'EVT-2024-008', '全国计算机等级考试（NCRE）', '教育部考试中心', '国家级', '计算机能力等级证书考试', NULL, 2, 8.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `event_info` VALUES (9, 'EVT-2024-009', '挑战杯全国大学生课外学术科技作品竞赛', '共青团中央、中国科协', '国家级', '学术科技创新赛事', NULL, 1, 16.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `event_info` VALUES (10, 'EVT-2024-010', '省级大学生程序设计竞赛', '省教育厅', '省级', '省级程序设计赛事', NULL, 2, 10.00, NULL, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for event_level_info
-- ----------------------------
DROP TABLE IF EXISTS `event_level_info`;
CREATE TABLE `event_level_info`  (
  `level_id` int NOT NULL AUTO_INCREMENT COMMENT '赛事级别主键',
  `level_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '赛事级别编码',
  `level_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '赛事级别名称',
  `level_index` decimal(4, 2) NOT NULL COMMENT '赛事级别指数（乘数）',
  `back_str1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_str2` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_int1` int NULL DEFAULT NULL COMMENT '备用字段-数字',
  `back_int2` int NULL DEFAULT NULL COMMENT '备用字段-数字',
  PRIMARY KEY (`level_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '赛事级别信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of event_level_info
-- ----------------------------
INSERT INTO `event_level_info` VALUES (1, 'LVL-001', '国家级-特等奖', 1.50, NULL, NULL, NULL, NULL);
INSERT INTO `event_level_info` VALUES (2, 'LVL-002', '国家级-一等奖', 1.20, NULL, NULL, NULL, NULL);
INSERT INTO `event_level_info` VALUES (3, 'LVL-003', '国家级-二等奖', 1.00, NULL, NULL, NULL, NULL);
INSERT INTO `event_level_info` VALUES (4, 'LVL-004', '国家级-三等奖', 0.80, NULL, NULL, NULL, NULL);
INSERT INTO `event_level_info` VALUES (5, 'LVL-005', '省级-特等奖', 1.00, NULL, NULL, NULL, NULL);
INSERT INTO `event_level_info` VALUES (6, 'LVL-006', '省级-一等奖', 0.80, NULL, NULL, NULL, NULL);
INSERT INTO `event_level_info` VALUES (7, 'LVL-007', '省级-二等奖', 0.60, NULL, NULL, NULL, NULL);
INSERT INTO `event_level_info` VALUES (8, 'LVL-008', '省级-三等奖', 0.50, NULL, NULL, NULL, NULL);
INSERT INTO `event_level_info` VALUES (9, 'LVL-009', '校级-一等奖', 0.50, NULL, NULL, NULL, NULL);
INSERT INTO `event_level_info` VALUES (10, 'LVL-010', '校级-二等奖', 0.30, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for item_info
-- ----------------------------
DROP TABLE IF EXISTS `item_info`;
CREATE TABLE `item_info`  (
  `item_id` int NOT NULL AUTO_INCREMENT COMMENT '赛项主键',
  `event_id` int NOT NULL COMMENT '赛事主键',
  `item_no` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '赛项编号',
  `item_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '赛项名称',
  `track_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '赛道',
  `major_desc` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '适用专业说明',
  `team_type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '组队方式（个人/团体）',
  `open_cond` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '开赛条件（校验条件）',
  `dept_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '赛项管理部门',
  `back_str1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_str2` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_str3` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_int1` int NULL DEFAULT NULL COMMENT '备用字段-数字',
  `back_int2` int NULL DEFAULT NULL COMMENT '备用字段-数字',
  PRIMARY KEY (`item_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '赛项信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of item_info
-- ----------------------------
INSERT INTO `item_info` VALUES (1, 1, 'ITM-001-01', 'ACM程序设计赛项', '算法赛道', '计算机类相关专业', '团体(3人)', '需通过校内选拔赛', '计算机学院', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `item_info` VALUES (2, 2, 'ITM-002-01', '蓝桥杯软件类赛项', '软件赛道', '软件工程、计算机科学', '个人', '无特殊限制', '软件学院', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `item_info` VALUES (3, 2, 'ITM-002-02', '蓝桥杯Web应用开发赛项', 'Web赛道', '计算机类、软件类专业', '个人', '需掌握HTML/CSS/JS', '软件学院', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `item_info` VALUES (4, 3, 'ITM-003-01', '数学建模本科组赛项', '本科组', '理工科专业', '团体(3人)', '需具备高等数学基础', '教务处', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `item_info` VALUES (5, 4, 'ITM-004-01', '计算机设计-软件开发赛项', '软件开发赛道', '计算机类、软件类专业', '团体(3人)', '需提交完整软件作品', '计算机学院', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `item_info` VALUES (6, 4, 'ITM-004-02', '计算机设计-数字媒体赛项', '数媒赛道', '数字媒体技术专业', '团体(3人)', '需提交多媒体作品', '信息学院', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `item_info` VALUES (7, 5, 'ITM-005-01', '信息安全-攻防赛项', '攻防赛道', '信息安全、网络安全专业', '团体(4人)', '需具备网络安全基础', '信息学院', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `item_info` VALUES (8, 6, 'ITM-006-01', '互联网+高教主赛道', '主赛道', '所有专业', '团体(5人)', '需有完整的商业计划书', '创新创业学院', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `item_info` VALUES (9, 7, 'ITM-007-01', '英语四级笔试赛项', '笔试', '所有专业', '个人', '在校本科生均可报名', '外国语学院', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `item_info` VALUES (10, 8, 'ITM-008-01', '计算机二级-C语言赛项', 'C语言赛道', '所有专业', '个人', '需具备C语言编程基础', '计算机学院', NULL, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for org_info
-- ----------------------------
DROP TABLE IF EXISTS `org_info`;
CREATE TABLE `org_info`  (
  `org_id` int NOT NULL AUTO_INCREMENT COMMENT '机构主键',
  `org_code` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '机构编码，按主键生成10位，前补0',
  `org_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '机构名称',
  `org_level` int NULL DEFAULT NULL COMMENT '第几级机构',
  `parent_org_code` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '上级机构编码',
  `remark` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `back_str1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_str2` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_str3` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  PRIMARY KEY (`org_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '机构信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of org_info
-- ----------------------------
INSERT INTO `org_info` VALUES (1, '0000000001', '某某大学', 1, NULL, '学校顶级机构', NULL, NULL, NULL);
INSERT INTO `org_info` VALUES (2, '0000000002', '计算机科学与技术学院', 2, '0000000001', NULL, NULL, NULL, NULL);
INSERT INTO `org_info` VALUES (3, '0000000003', '软件工程学院', 2, '0000000001', NULL, NULL, NULL, NULL);
INSERT INTO `org_info` VALUES (4, '0000000004', '信息工程学院', 2, '0000000001', NULL, NULL, NULL, NULL);
INSERT INTO `org_info` VALUES (5, '0000000005', '计科2301班', 3, '0000000002', NULL, NULL, NULL, NULL);
INSERT INTO `org_info` VALUES (6, '0000000006', '计科2302班', 3, '0000000002', NULL, NULL, NULL, NULL);
INSERT INTO `org_info` VALUES (7, '0000000007', '软工2301班', 3, '0000000003', NULL, NULL, NULL, NULL);
INSERT INTO `org_info` VALUES (8, '0000000008', '软工2302班', 3, '0000000003', NULL, NULL, NULL, NULL);
INSERT INTO `org_info` VALUES (9, '0000000009', '信工2301班', 3, '0000000004', NULL, NULL, NULL, NULL);
INSERT INTO `org_info` VALUES (10, '0000000010', '信工2302班', 3, '0000000004', NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for score_require
-- ----------------------------
DROP TABLE IF EXISTS `score_require`;
CREATE TABLE `score_require`  (
  `req_id` int NOT NULL AUTO_INCREMENT COMMENT '要求主键',
  `level_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分级名称',
  `min_score` decimal(5, 2) NULL DEFAULT NULL COMMENT '分级分数-最低',
  `max_score` decimal(5, 2) NULL DEFAULT NULL COMMENT '分级分数-最高',
  `back_str1` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_str2` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_int1` int NULL DEFAULT NULL COMMENT '备用字段-数字',
  `back_int2` int NULL DEFAULT NULL COMMENT '备用字段-数字',
  PRIMARY KEY (`req_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '二课成绩要求表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of score_require
-- ----------------------------
INSERT INTO `score_require` VALUES (1, 'S级-卓越', 95.00, 100.00, NULL, NULL, NULL, NULL);
INSERT INTO `score_require` VALUES (2, 'A级-优秀', 85.00, 94.99, NULL, NULL, NULL, NULL);
INSERT INTO `score_require` VALUES (3, 'B级-良好', 75.00, 84.99, NULL, NULL, NULL, NULL);
INSERT INTO `score_require` VALUES (4, 'C级-合格', 60.00, 74.99, NULL, NULL, NULL, NULL);
INSERT INTO `score_require` VALUES (5, 'D级-不合格', 0.00, 59.99, NULL, NULL, NULL, NULL);
INSERT INTO `score_require` VALUES (6, 'A+级-特优', 90.00, 100.00, NULL, NULL, NULL, NULL);
INSERT INTO `score_require` VALUES (7, 'B+级-优良', 80.00, 89.99, NULL, NULL, NULL, NULL);
INSERT INTO `score_require` VALUES (8, 'C+级-尚可', 65.00, 79.99, NULL, NULL, NULL, NULL);
INSERT INTO `score_require` VALUES (9, 'D+级-及格', 50.00, 64.99, NULL, NULL, NULL, NULL);
INSERT INTO `score_require` VALUES (10, 'E级-不及格', 0.00, 49.99, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for stu_score_record
-- ----------------------------
DROP TABLE IF EXISTS `stu_score_record`;
CREATE TABLE `stu_score_record`  (
  `score_id` int NOT NULL AUTO_INCREMENT COMMENT '成绩主键',
  `stu_id` int NOT NULL COMMENT '学生主键',
  `event_id` int NOT NULL COMMENT '赛事主键',
  `event_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '赛事名称（冗余字段，提高查询效率）',
  `item_id` int NOT NULL COMMENT '赛项主键',
  `item_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '赛项名称（冗余字段，提高查询效率）',
  `level_id` int NOT NULL COMMENT '赛事级别主键',
  `level_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '赛事级别名称（冗余字段，提高查询效率）',
  `base_score` decimal(5, 2) NOT NULL COMMENT '赛事成绩基准分（获奖时的快照）',
  `level_index` decimal(4, 2) NOT NULL COMMENT '赛事级别指数（获奖时的快照）',
  `final_score` decimal(5, 2) NOT NULL COMMENT '成绩得分 = base_score × level_index',
  `schedule_id` int NULL DEFAULT NULL COMMENT '赛程主键（扩展用，暂不关联）',
  `cert_date` date NULL DEFAULT NULL COMMENT '获得证书日期',
  `cert_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '证书（文件地址）',
  `audit_status` int NULL DEFAULT 0 COMMENT '审核状态：0-待审核，1-已通过，2-未通过',
  `audit_remark` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '审核备注（未通过原因）',
  `back_str1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_str2` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_str3` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_int1` int NULL DEFAULT NULL COMMENT '备用字段-数字',
  `back_int2` int NULL DEFAULT NULL COMMENT '备用字段-数字',
  PRIMARY KEY (`score_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '学生成绩表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of stu_score_record
-- ----------------------------
INSERT INTO `stu_score_record` VALUES (1, 1, 1, 'ACM国际大学生程序设计竞赛', 1, 'ACM程序设计赛项', 2, '国家级-一等奖', 20.00, 1.20, 24.00, NULL, '2024-06-15', '/certs/acm_1st.pdf', 1, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `stu_score_record` VALUES (2, 1, 2, '蓝桥杯全国软件和信息技术专业人才大赛', 2, '蓝桥杯软件类赛项', 3, '国家级-二等奖', 15.00, 1.00, 15.00, NULL, '2024-05-20', '/certs/lanqiao_2nd.pdf', 1, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `stu_score_record` VALUES (3, 2, 3, '全国大学生数学建模竞赛', 4, '数学建模本科组赛项', 3, '国家级-二等奖', 15.00, 1.00, 15.00, NULL, '2024-09-18', '/certs/mathmodel_2nd.pdf', 0, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `stu_score_record` VALUES (4, 2, 7, '全国英语四级考试（CET-4）', 9, '英语四级笔试赛项', 3, '国家级-二等奖', 10.00, 1.00, 10.00, NULL, '2024-06-15', '/certs/cet4_pass.pdf', 1, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `stu_score_record` VALUES (5, 3, 8, '全国计算机等级考试（NCRE）', 10, '计算机二级-C语言赛项', 2, '国家级-一等奖', 8.00, 1.20, 9.60, NULL, '2024-03-25', '/certs/ncre2_1st.pdf', 2, '证书信息不完整，请重新上传', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `stu_score_record` VALUES (6, 4, 4, '中国大学生计算机设计大赛', 5, '计算机设计-软件开发赛项', 4, '国家级-三等奖', 12.00, 0.80, 9.60, NULL, '2024-07-20', '/certs/compdesign_3rd.pdf', 1, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `stu_score_record` VALUES (7, 5, 5, '全国大学生信息安全竞赛', 7, '信息安全-攻防赛项', 2, '国家级-一等奖', 12.00, 1.20, 14.40, NULL, '2024-08-10', '/certs/infosec_1st.pdf', 0, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `stu_score_record` VALUES (8, 6, 6, '互联网+大学生创新创业大赛', 8, '互联网+高教主赛道', 3, '国家级-二等奖', 18.00, 1.00, 18.00, NULL, '2024-10-15', '/certs/internetplus_2nd.pdf', 2, '项目材料不完整，请补充', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `stu_score_record` VALUES (9, 7, 10, '省级大学生程序设计竞赛', 1, 'ACM程序设计赛项', 6, '省级-一等奖', 10.00, 0.80, 8.00, NULL, '2024-04-20', '/certs/prov_1st.pdf', 1, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `stu_score_record` VALUES (10, 8, 9, '挑战杯全国大学生课外学术科技作品竞赛', 5, '计算机设计-软件开发赛项', 5, '省级-特等奖', 16.00, 1.00, 16.00, NULL, '2024-11-05', '/certs/challenge_prov.pdf', 0, NULL, NULL, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for student_info
-- ----------------------------
DROP TABLE IF EXISTS `student_info`;
CREATE TABLE `student_info`  (
  `stu_id` int NOT NULL AUTO_INCREMENT COMMENT '学生主键',
  `stu_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '学号',
  `stu_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '姓名',
  `gender` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '性别',
  `phone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '电话号码',
  `class_org_id` int NOT NULL COMMENT '所述班级（机构主键）',
  `enroll_year` char(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '入学年份（第几届）',
  `id_card` char(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '身份证号',
  `birth_date` date NULL DEFAULT NULL COMMENT '出生日期',
  `train_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '培养层次：本科、专科、硕士等',
  `back_str1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_str2` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_str3` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备用字段-字符',
  `back_int1` int NULL DEFAULT NULL COMMENT '备用字段-数字',
  `back_int2` int NULL DEFAULT NULL COMMENT '备用字段-数字',
  PRIMARY KEY (`stu_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '学生信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student_info
-- ----------------------------
INSERT INTO `student_info` VALUES (1, '2023010101', '张三', '男', '13800001001', 5, '2023', '320102200401011234', '2004-01-01', '本科', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student_info` VALUES (2, '2023010102', '李四', '女', '13800001002', 5, '2023', '320102200402021234', '2004-02-02', '本科', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student_info` VALUES (3, '2023010103', '王五', '男', '13800001003', 5, '2023', '320102200403031234', '2004-03-03', '本科', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student_info` VALUES (4, '2023010201', '赵六', '男', '13800001004', 6, '2023', '320102200404041234', '2004-04-04', '本科', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student_info` VALUES (5, '2023010202', '孙七', '女', '13800001005', 6, '2023', '320102200405051234', '2004-05-05', '本科', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student_info` VALUES (6, '2023020101', '周八', '男', '13800001006', 7, '2023', '320102200406061234', '2004-06-06', '本科', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student_info` VALUES (7, '2023020102', '吴九', '女', '13800001007', 7, '2023', '320102200407071234', '2004-07-07', '本科', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student_info` VALUES (8, '2023020201', '郑十', '男', '13800001008', 8, '2023', '320102200408081234', '2004-08-08', '本科', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student_info` VALUES (9, '2023030101', '陈十一', '男', '13800001009', 9, '2023', '320102200409091234', '2004-09-09', '本科', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `student_info` VALUES (10, '2023030201', '林十二', '女', '13800001010', 10, '2023', '320102200410101234', '2004-10-10', '本科', NULL, NULL, NULL, NULL, NULL);

SET FOREIGN_KEY_CHECKS = 1;
