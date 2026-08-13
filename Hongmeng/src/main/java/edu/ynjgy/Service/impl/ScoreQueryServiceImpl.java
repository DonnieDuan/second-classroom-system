
        package edu.ynjgy.Service.impl;
import edu.ynjgy.Service.ScoreQueryService;
import edu.ynjgy.dto.ScoreQueryDTO;
import edu.ynjgy.entity.StuScoreRecord;
import edu.ynjgy.entity.StudentInfo;
import edu.ynjgy.mapper.StuScoreRecordMapper;
import edu.ynjgy.mapper.StudentInfoMapper;
import edu.ynjgy.utils.PageResult;
import edu.ynjgy.utils.Result;
import edu.ynjgy.vo.ScoreRecordDetailVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class ScoreQueryServiceImpl implements ScoreQueryService {

    private final StuScoreRecordMapper scoreRecordMapper;
    private final StudentInfoMapper studentInfoMapper;

    @Override
    public Result<PageResult<ScoreRecordDetailVO>> queryScores(ScoreQueryDTO queryDTO) {
        int offset = (queryDTO.getPageNum() - 1) * queryDTO.getPageSize();
        List<StuScoreRecord> pageData = scoreRecordMapper.queryPage(
                queryDTO.getStuId(), queryDTO.getEventId(), queryDTO.getItemId(),
                queryDTO.getLevelId(), queryDTO.getClassOrgId(),
                queryDTO.getStuName(), queryDTO.getEventName(),
                queryDTO.getStartDate(), queryDTO.getEndDate(),
                offset, queryDTO.getPageSize());
        Long total = scoreRecordMapper.countQuery(
                queryDTO.getStuId(), queryDTO.getEventId(), queryDTO.getItemId(),
                queryDTO.getLevelId(), queryDTO.getClassOrgId(),
                queryDTO.getStuName(), queryDTO.getEventName(),
                queryDTO.getStartDate(), queryDTO.getEndDate());
        // Batch load students for all records on this page
        Map<Integer, StudentInfo> studentMap = batchLoadStudents(pageData);
        List<ScoreRecordDetailVO> voList = pageData.stream()
                .map(r -> convertToVO(r, studentMap.get(r.getStuId())))
                .collect(Collectors.toList());
        PageResult<ScoreRecordDetailVO> pageResult = PageResult.of(voList, total,
                queryDTO.getPageNum(), queryDTO.getPageSize());
        return Result.success(pageResult);
    }

    @Override
    @Cacheable(value = "scoresByEvent", key = "#eventId")
    public Result<List<ScoreRecordDetailVO>> getScoresByEvent(Integer eventId) {
        List<StuScoreRecord> records = scoreRecordMapper.selectByEventId(eventId);
        Map<Integer, StudentInfo> studentMap = batchLoadStudents(records);
        List<ScoreRecordDetailVO> voList = records.stream()
                .map(r -> convertToVO(r, studentMap.get(r.getStuId())))
                .collect(Collectors.toList());
        return Result.success(voList);
    }

    @Override
    public Result<List<Map<String, Object>>> getScoresByDateRange(Integer stuId, String startDate, String endDate) {
        List<Map<String, Object>> result = scoreRecordMapper.getScoresByDateRange(stuId, startDate, endDate);
        return Result.success(result);
    }

    @Override
    public Result<?> exportScoreReport(Integer stuId) {
        StudentInfo student = studentInfoMapper.selectById(stuId);
        if (student == null) {
            return Result.error("学生不存在");
        }

        List<StuScoreRecord> records = scoreRecordMapper.selectByStuId(stuId);

        Map<String, Object> report = new HashMap<>();
        report.put("studentInfo", student);
        report.put("scoreRecords", records);
        report.put("totalScore", scoreRecordMapper.sumScoreByStuId(stuId));
        report.put("exportTime", LocalDate.now());

        return Result.success(report);
    }

    private Map<Integer, StudentInfo> batchLoadStudents(List<StuScoreRecord> records) {
        List<Integer> stuIds = records.stream()
                .map(StuScoreRecord::getStuId)
                .distinct()
                .collect(Collectors.toList());
        if (stuIds.isEmpty()) return Collections.emptyMap();
        return studentInfoMapper.selectByIds(stuIds).stream()
                .collect(Collectors.toMap(StudentInfo::getStuId, s -> s));
    }

    private ScoreRecordDetailVO convertToVO(StuScoreRecord record, StudentInfo student) {
        ScoreRecordDetailVO vo = new ScoreRecordDetailVO();
        vo.setScoreId(record.getScoreId());
        vo.setStuId(record.getStuId());
        vo.setEventId(record.getEventId());
        vo.setEventName(record.getEventName());
        vo.setItemId(record.getItemId());
        vo.setItemName(record.getItemName());
        vo.setLevelId(record.getLevelId());
        vo.setLevelName(record.getLevelName());
        vo.setBaseScore(record.getBaseScore());
        vo.setLevelIndex(record.getLevelIndex());
        vo.setFinalScore(record.getFinalScore());
        vo.setCertDate(record.getCertDate());
        vo.setCertPath(record.getCertPath());
        vo.setAuditStatus(record.getAuditStatus());
        vo.setAuditRemark(record.getAuditRemark());

        if (student != null) {
            vo.setStuName(student.getStuName());
            vo.setStuNo(student.getStuNo());
        }

        return vo;
    }
}
