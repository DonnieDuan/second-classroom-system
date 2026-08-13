 package edu.ynjgy.Service.impl;

import edu.ynjgy.Service.AdminService;
import edu.ynjgy.dto.BatchScoreImportDTO;
import edu.ynjgy.dto.ScoreAuditDTO;
import edu.ynjgy.entity.*;
import edu.ynjgy.exception.BusinessException;
import edu.ynjgy.mapper.*;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.*;

@Slf4j
@Service
@RequiredArgsConstructor
public class AdminServiceImpl implements AdminService {

    private final StuScoreRecordMapper scoreRecordMapper;
    private final StudentInfoMapper studentInfoMapper;
    private final EventInfoMapper eventInfoMapper;
    private final ItemInfoMapper itemInfoMapper;
    private final EventLevelInfoMapper levelInfoMapper;
    private final OrgInfoMapper orgInfoMapper;

    @Override
    @Transactional
    @CacheEvict(value = {"studentTotalScore", "classScoreStats", "majorScoreStats"}, allEntries = true)
    public Result<?> auditScore(ScoreAuditDTO auditDTO) {
        StuScoreRecord record = scoreRecordMapper.selectById(auditDTO.getScoreId());
        if (record == null) {
            throw new BusinessException("成绩记录不存在");
        }

        record.setAuditStatus(auditDTO.getAuditStatus());
        record.setAuditRemark(auditDTO.getAuditRemark());

        int rows = scoreRecordMapper.update(record);
        if (rows > 0) {
            String statusText = auditDTO.getAuditStatus() == 1 ? "审核通过" : "审核拒绝";
            return Result.success("成绩" + statusText);
        }
        return Result.error("审核失败");
    }

    @Override
    @Transactional
    @CacheEvict(value = {"studentTotalScore", "classScoreStats", "majorScoreStats"}, allEntries = true)
    public Result<?> batchImportScores(BatchScoreImportDTO importDTO) {
        EventInfo event = eventInfoMapper.selectById(importDTO.getEventId());
        if (event == null) {
            throw new BusinessException("赛事不存在");
        }

        ItemInfo item = itemInfoMapper.selectById(importDTO.getItemId());
        if (item == null) {
            throw new BusinessException("赛项不存在");
        }

        EventLevelInfo level = levelInfoMapper.selectById(importDTO.getLevelId());
        if (level == null) {
            throw new BusinessException("获奖级别不存在");
        }

        BigDecimal finalScore = event.getBaseScore().multiply(level.getLevelIndex());
        int successCount = 0;
        int failCount = 0;
        List<String> errors = new ArrayList<>();

        for (BatchScoreImportDTO.ScoreItem scoreItem : importDTO.getScores()) {
            StudentInfo student = studentInfoMapper.selectById(scoreItem.getStuId());
            if (student == null) {
                errors.add("学生ID " + scoreItem.getStuId() + " 不存在");
                failCount++;
                continue;
            }

            StuScoreRecord record = new StuScoreRecord();
            record.setStuId(scoreItem.getStuId());
            record.setEventId(event.getEventId());
            record.setEventName(event.getEventName());
            record.setItemId(item.getItemId());
            record.setItemName(item.getItemName());
            record.setLevelId(level.getLevelId());
            record.setLevelName(level.getLevelName());
            record.setBaseScore(event.getBaseScore());
            record.setLevelIndex(level.getLevelIndex());
            record.setFinalScore(finalScore);
            record.setCertDate(importDTO.getCertDate());
            record.setCertPath(scoreItem.getCertPath());

            scoreRecordMapper.insert(record);
            successCount++;
        }

        Map<String, Object> result = new HashMap<>();
        result.put("successCount", successCount);
        result.put("failCount", failCount);
        result.put("errors", errors);

        return Result.success(result);
    }

    @Override
    public Result<Map<String, Object>> getDashboardStatistics() {
        Map<String, Object> dashboard = new HashMap<>();

        dashboard.put("totalStudents", studentInfoMapper.countAll());
        dashboard.put("totalEvents", eventInfoMapper.countAll());
        dashboard.put("totalScoreRecords", scoreRecordMapper.countAll());
        dashboard.put("avgScore", scoreRecordMapper.getGlobalAvgScore());

        List<Map<String, Object>> topStudents = scoreRecordMapper.getTopStudents(10);
        dashboard.put("topStudents", topStudents);

        // Event trend for bar chart
        List<Map<String, Object>> eventTrend = scoreRecordMapper.getEventTrend();
        List<Map<String, Object>> trendList = new ArrayList<>();
        for (Map<String, Object> row : eventTrend) {
            Map<String, Object> item = new HashMap<>();
            item.put("eventName", row.get("event_name"));
            item.put("count", row.get("participant_count"));
            trendList.add(item);
        }
        dashboard.put("eventTrend", trendList);

        // Level distribution for pie chart
        List<Map<String, Object>> levelDist = scoreRecordMapper.getLevelDistribution();
        List<Map<String, Object>> distList = new ArrayList<>();
        for (Map<String, Object> row : levelDist) {
            Map<String, Object> item = new HashMap<>();
            item.put("levelName", row.get("level_name"));
            item.put("count", row.get("cnt"));
            distList.add(item);
        }
        dashboard.put("levelDistribution", distList);

        return Result.success(dashboard);
    }

    @Override
    public Result<?> generateClassReport(Integer classOrgId) {
        OrgInfo org = orgInfoMapper.selectById(classOrgId);
        if (org == null) {
            throw new BusinessException("班级不存在");
        }

        List<StudentInfo> students = studentInfoMapper.selectByClassId(classOrgId);
        List<Integer> stuIds = students.stream()
                .map(StudentInfo::getStuId)
                .collect(java.util.stream.Collectors.toList());

        // Batch-load scores and totals
        Map<Integer, List<StuScoreRecord>> recordsByStu = new HashMap<>();
        Map<Integer, BigDecimal> totalByStu = new HashMap<>();
        if (!stuIds.isEmpty()) {
            List<StuScoreRecord> allRecords = scoreRecordMapper.selectByStuIds(stuIds);
            for (StuScoreRecord r : allRecords) {
                recordsByStu.computeIfAbsent(r.getStuId(), k -> new ArrayList<>()).add(r);
            }
            List<Map<String, Object>> sumResults = scoreRecordMapper.sumScoresByStuIds(stuIds);
            for (Map<String, Object> row : sumResults) {
                Integer stuId = (Integer) row.get("stu_id");
                BigDecimal total = (BigDecimal) row.get("total_score");
                totalByStu.put(stuId, total != null ? total : BigDecimal.ZERO);
            }
        }

        List<Map<String, Object>> studentReports = new ArrayList<>();
        for (StudentInfo student : students) {
            Map<String, Object> studentReport = new HashMap<>();
            studentReport.put("studentInfo", student);

            List<StuScoreRecord> records = recordsByStu.getOrDefault(student.getStuId(), Collections.emptyList());
            studentReport.put("scoreRecords", records);
            studentReport.put("totalScore", totalByStu.getOrDefault(student.getStuId(), BigDecimal.ZERO));
            studentReport.put("recordCount", records.size());

            studentReports.add(studentReport);
        }

        Map<String, Object> classReport = new HashMap<>();
        classReport.put("classInfo", org);
        classReport.put("studentReports", studentReports);
        classReport.put("totalStudents", students.size());
        classReport.put("generateTime", LocalDate.now());

        return Result.success(classReport);
    }
}
