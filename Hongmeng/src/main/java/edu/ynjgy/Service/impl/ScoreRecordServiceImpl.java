package edu.ynjgy.Service.impl;

import java.math.BigDecimal;
import java.util.List;

import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import edu.ynjgy.Service.ScoreRecordService;
import edu.ynjgy.dto.ScoreSubmitDTO;
import edu.ynjgy.entity.EventInfo;
import edu.ynjgy.entity.EventLevelInfo;
import edu.ynjgy.entity.ItemInfo;
import edu.ynjgy.entity.StuScoreRecord;
import edu.ynjgy.entity.StudentInfo;
import edu.ynjgy.exception.BusinessException;
import edu.ynjgy.mapper.EventInfoMapper;
import edu.ynjgy.mapper.EventLevelInfoMapper;
import edu.ynjgy.mapper.ItemInfoMapper;
import edu.ynjgy.mapper.StuScoreRecordMapper;
import edu.ynjgy.mapper.StudentInfoMapper;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
@RequiredArgsConstructor
public class ScoreRecordServiceImpl implements ScoreRecordService {

    private final StuScoreRecordMapper scoreRecordMapper;
    private final StudentInfoMapper studentInfoMapper;
    private final EventInfoMapper eventInfoMapper;
    private final ItemInfoMapper itemInfoMapper;
    private final EventLevelInfoMapper levelInfoMapper;

    @Override
    @Transactional
    @CacheEvict(value = {"studentTotalScore", "studentScores", "classScoreStats", "majorScoreStats"}, key = "#dto.stuId")
    public Result<?> submitScore(ScoreSubmitDTO dto) {
        // 1. 校验学生存在
        StudentInfo student = studentInfoMapper.selectById(dto.getStuId());
        if (student == null) {
            throw new BusinessException("学生不存在");
        }

        // 2. 赛事信息
        EventInfo event = eventInfoMapper.selectById(dto.getEventId());
        if (event == null) {
            throw new BusinessException("赛事不存在");
        }

        // 3. 赛项信息
        ItemInfo item = itemInfoMapper.selectById(dto.getItemId());
        if (item == null) {
            throw new BusinessException("赛项不存在");
        }

        // 判断赛事类型：backStr1 = "exam" 表示考试类，否则为竞赛类
        boolean isExam = "exam".equalsIgnoreCase(event.getBackStr1());

        BigDecimal finalScore;
        Integer levelId = null;
        String levelName = null;
        BigDecimal baseScore = event.getBaseScore();
        BigDecimal levelIndex = BigDecimal.ONE;

        if (isExam) {
            // 考试类：根据分数区间计算积分（英语四六级425分及格线）
            if (dto.getScore() == null || dto.getScore().compareTo(BigDecimal.ZERO) <= 0) {
                throw new BusinessException("考试分数不能为空且必须大于0");
            }
            int score = dto.getScore().intValue();
            if (score < 425) {
                finalScore = BigDecimal.ZERO;
                levelName = "未达标";
            } else if (score <= 450) {
                finalScore = BigDecimal.valueOf(2);
                levelName = "及格";
            } else if (score <= 500) {
                finalScore = BigDecimal.valueOf(3);
                levelName = "良好";
            } else if (score <= 550) {
                finalScore = BigDecimal.valueOf(5);
                levelName = "优秀";
            } else if (score <= 600) {
                finalScore = BigDecimal.valueOf(8);
                levelName = "高分";
            } else if (score <= 650) {
                finalScore = BigDecimal.valueOf(10);
                levelName = "优异";
            } else if (score <= 700) {
                finalScore = BigDecimal.valueOf(15);
                levelName = "卓越";
            } else {
                finalScore = BigDecimal.valueOf(20);
                levelName = "满分";
            }
        } else {
            // 竞赛类：使用获奖级别计算分数
            EventLevelInfo level = levelInfoMapper.selectById(dto.getLevelId());
            if (level == null) {
                throw new BusinessException("获奖级别不存在");
            }
            finalScore = event.getBaseScore().multiply(level.getLevelIndex());
            levelId = level.getLevelId();
            levelName = level.getLevelName();
            levelIndex = level.getLevelIndex();
        }

        // 构建成绩记录
        StuScoreRecord record = new StuScoreRecord();
        record.setStuId(dto.getStuId());
        record.setEventId(event.getEventId());
        record.setEventName(event.getEventName());
        record.setItemId(item.getItemId());
        record.setItemName(item.getItemName());
        record.setLevelId(levelId);
        record.setLevelName(levelName);
        record.setBaseScore(baseScore);
        record.setLevelIndex(levelIndex);
        record.setFinalScore(finalScore);
        if (isExam) {
            record.setRawScore(dto.getScore());
        }
        record.setCertDate(dto.getCertDate());
        record.setCertPath(dto.getCertPath());
        record.setAuditStatus(0);

        scoreRecordMapper.insert(record);
        return Result.success("成绩填报成功，请等待教师审核");
    }

    @Override
    @Cacheable(value = "studentScores", key = "#stuId")
    public Result<List<StuScoreRecord>> getMyScores(Integer stuId) {
        List<StuScoreRecord> records = scoreRecordMapper.selectByStuId(stuId);
        return Result.success(records);
    }

    @Override
    @Cacheable(value = "studentTotalScore", key = "#stuId")
    public Result<BigDecimal> getMyTotalScore(Integer stuId) {
        BigDecimal total = scoreRecordMapper.sumApprovedScoreByStuId(stuId);
        return Result.success(total);
    }
}