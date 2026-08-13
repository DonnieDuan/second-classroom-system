package edu.ynjgy.Service;

import edu.ynjgy.dto.ScoreSubmitDTO;
import edu.ynjgy.entity.StuScoreRecord;
import edu.ynjgy.utils.Result;

import java.math.BigDecimal;
import java.util.List;

public interface ScoreRecordService {
    Result<?> submitScore(ScoreSubmitDTO dto);
    Result<List<StuScoreRecord>> getMyScores(Integer stuId);
    Result<BigDecimal> getMyTotalScore(Integer stuId);
}
