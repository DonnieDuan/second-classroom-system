
package edu.ynjgy.Controller;

import edu.ynjgy.Service.ScoreQueryService;
import edu.ynjgy.dto.ScoreQueryDTO;
import edu.ynjgy.entity.OrgInfo;
import edu.ynjgy.entity.StudentInfo;
import edu.ynjgy.mapper.OrgInfoMapper;
import edu.ynjgy.mapper.StuScoreRecordMapper;
import edu.ynjgy.mapper.StudentInfoMapper;
import edu.ynjgy.utils.PageResult;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/score")
@RequiredArgsConstructor
@Validated
public class ScoreQueryController {

    private final ScoreQueryService scoreQueryService;
    private final StuScoreRecordMapper scoreRecordMapper;
    private final StudentInfoMapper studentInfoMapper;
    private final OrgInfoMapper orgInfoMapper;

    @GetMapping("/list")
    public Result<?> getScoreList(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer pageSize,
            @RequestParam(required = false) String stuName,
            @RequestParam(required = false) String eventName,
            @RequestParam(required = false) Integer classOrgId) {
        ScoreQueryDTO queryDTO = new ScoreQueryDTO();
        queryDTO.setPageNum(page);
        queryDTO.setPageSize(pageSize);
        queryDTO.setStuName(stuName);
        queryDTO.setEventName(eventName);
        queryDTO.setClassOrgId(classOrgId);
        return scoreQueryService.queryScores(queryDTO);
    }

    @GetMapping("/summary")
    public Result<?> getScoreSummary(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer pageSize,
            @RequestParam(required = false) Integer classOrgId,
            @RequestParam(required = false) String enrollYear,
            @RequestParam(required = false) String trainLevel) {

        int offset = (page - 1) * pageSize;
        List<StudentInfo> pageStudents = studentInfoMapper.selectSummaryPage(
                classOrgId, enrollYear, trainLevel, offset, pageSize);
        Long total = studentInfoMapper.countSummary(classOrgId, enrollYear, trainLevel);

        List<Integer> stuIds = pageStudents.stream()
                .map(StudentInfo::getStuId)
                .collect(Collectors.toList());

        // Batch load scores
        Map<Integer, BigDecimal> totalScoreMap = new HashMap<>();
        Map<Integer, Integer> recordCountMap = new HashMap<>();
        if (!stuIds.isEmpty()) {
            List<Map<String, Object>> sumResults = scoreRecordMapper.sumScoresByStuIds(stuIds);
            for (Map<String, Object> row : sumResults) {
                Integer stuId = (Integer) row.get("stu_id");
                BigDecimal totalScore = (BigDecimal) row.get("total_score");
                totalScoreMap.put(stuId, totalScore != null ? totalScore : BigDecimal.ZERO);
            }
            List<Map<String, Object>> countResults = scoreRecordMapper.countRecordsByStuIds(stuIds);
            for (Map<String, Object> row : countResults) {
                Integer stuId = (Integer) row.get("stu_id");
                Integer cnt = ((Number) row.get("cnt")).intValue();
                recordCountMap.put(stuId, cnt);
            }
        }

        // Preload class names
        Map<Integer, String> classNameMap = new HashMap<>();
        for (StudentInfo s : pageStudents) {
            if (s.getClassOrgId() != null && !classNameMap.containsKey(s.getClassOrgId())) {
                OrgInfo org = orgInfoMapper.selectById(s.getClassOrgId());
                classNameMap.put(s.getClassOrgId(), org != null ? org.getOrgName() : "未知班级");
            }
        }

        List<Map<String, Object>> summaryList = new ArrayList<>();
        for (StudentInfo student : pageStudents) {
            Map<String, Object> summary = new HashMap<>();
            summary.put("stuId", student.getStuId());
            summary.put("stuNo", student.getStuNo());
            summary.put("stuName", student.getStuName());
            summary.put("className", classNameMap.getOrDefault(student.getClassOrgId(), "未知班级"));
            summary.put("enrollYear", student.getEnrollYear());
            summary.put("trainLevel", student.getTrainLevel());
            summary.put("totalScore", totalScoreMap.getOrDefault(student.getStuId(), BigDecimal.ZERO));
            summary.put("recordCount", recordCountMap.getOrDefault(student.getStuId(), 0));
            summaryList.add(summary);
        }

        Map<String, Object> stats = scoreRecordMapper.getScoreStats(classOrgId, enrollYear, trainLevel);
        Map<String, Object> result = new HashMap<>();
        result.put("page", PageResult.of(summaryList, total, page, pageSize));
        result.put("stats", stats);

        return Result.success(result);
    }

    @PostMapping("/query")
    public Result<?> queryScores(@RequestBody ScoreQueryDTO queryDTO) {
        return scoreQueryService.queryScores(queryDTO);
    }

    @GetMapping("/event/{eventId}")
    public Result<?> getScoresByEvent(@PathVariable Integer eventId) {
        return scoreQueryService.getScoresByEvent(eventId);
    }

    @GetMapping("/student/{stuId}")
    public Result<?> getStudentScoreDetail(@PathVariable Integer stuId) {
        return scoreQueryService.exportScoreReport(stuId);
    }

    @GetMapping("/dateRange")
    public Result<?> getScoresByDateRange(
            @RequestParam Integer stuId,
            @RequestParam String startDate,
            @RequestParam String endDate) {
        return scoreQueryService.getScoresByDateRange(stuId, startDate, endDate);
    }

    @GetMapping("/export/{stuId}")
    public Result<?> exportScoreReport(@PathVariable Integer stuId) {
        return scoreQueryService.exportScoreReport(stuId);
    }

    @DeleteMapping("/{scoreId}")
    public Result<?> deleteScore(@PathVariable Integer scoreId) {
        int rows = scoreRecordMapper.deleteById(scoreId);
        if (rows > 0) {
            return Result.success("删除成功");
        }
        return Result.error("删除失败");
    }

    @DeleteMapping
    public Result<?> batchDelete(@RequestParam String ids) {
        for (String id : ids.split(",")) {
            scoreRecordMapper.deleteById(Integer.parseInt(id.trim()));
        }
        return Result.success("删除成功");
    }
}

