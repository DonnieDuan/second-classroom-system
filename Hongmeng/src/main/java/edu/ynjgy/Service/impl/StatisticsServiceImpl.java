package edu.ynjgy.Service.impl;

import edu.ynjgy.mapper.OrgInfoMapper;
import edu.ynjgy.mapper.StuScoreRecordMapper;
import edu.ynjgy.mapper.StudentInfoMapper;
import edu.ynjgy.Service.StatisticsService;
import edu.ynjgy.utils.Result;
import edu.ynjgy.vo.ClassScoreVO;
import edu.ynjgy.vo.StudentScoreVO;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class StatisticsServiceImpl implements StatisticsService {

    private final StuScoreRecordMapper scoreRecordMapper;
    private final StudentInfoMapper studentInfoMapper;
    private final OrgInfoMapper orgInfoMapper;

    @Override
    @Cacheable(value = "classScoreStats", key = "#classId")
    public Result<?> getClassScoreStatistics(Integer classId) {
        // 1. 获取班级名称
        String className = orgInfoMapper.selectById(classId).getOrgName();

        // 2. 查询班级学生成绩汇总
        List<Map<String, Object>> rawList = scoreRecordMapper.getClassScoreSummary(classId);
        List<StudentScoreVO> students = new ArrayList<>();
        List<StudentScoreVO> warningList = new ArrayList<>();

        for (Map<String, Object> map : rawList) {
            StudentScoreVO vo = new StudentScoreVO();
            vo.setStuId((Integer) map.get("stu_id"));
            vo.setStuName((String) map.get("stu_name"));
            BigDecimal totalScore = (BigDecimal) map.get("total_score");
            vo.setTotalScore(totalScore);
            // 根据总分判定等级
            if (totalScore.compareTo(BigDecimal.valueOf(90)) >= 0) {
                vo.setScoreLevel("优秀");
            } else if (totalScore.compareTo(BigDecimal.valueOf(75)) >= 0) {
                vo.setScoreLevel("良好");
            } else if (totalScore.compareTo(BigDecimal.valueOf(60)) >= 0) {
                vo.setScoreLevel("及格");
            } else {
                vo.setScoreLevel("不及格");
            }
            students.add(vo);
            if (totalScore.compareTo(BigDecimal.valueOf(60)) < 0) {
                warningList.add(vo);
            }
        }

        ClassScoreVO classVO = new ClassScoreVO();
        classVO.setClassName(className);
        classVO.setStudents(students);
        classVO.setWarningList(warningList);
        return Result.success(classVO);
    }

    @Override
    @Cacheable(value = "eventTrend")
    public Result<?> getEventTrendStatistics() {
        List<Map<String, Object>> trend = scoreRecordMapper.getEventTrend();
        return Result.success(trend);
    }

    @Override
    @Cacheable(value = "majorScoreStats", key = "#majorId")
    public Result<?> getMajorScoreStatistics(Integer majorId) {
        List<Map<String, Object>> distribution = scoreRecordMapper.getMajorScoreDistribution(majorId);
        Map<String, Object> result = new HashMap<>();
        result.put("distribution", distribution);
        // 可选：加上专业名称
        result.put("majorName", orgInfoMapper.selectById(majorId).getOrgName());
        return Result.success(result);
    }
}