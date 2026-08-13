package edu.ynjgy.Service;

import edu.ynjgy.dto.ScoreQueryDTO;
import edu.ynjgy.utils.PageResult;
import edu.ynjgy.utils.Result;
import edu.ynjgy.vo.ScoreRecordDetailVO;

import java.util.List;
import java.util.Map;

public interface ScoreQueryService {
    Result<PageResult<ScoreRecordDetailVO>> queryScores(ScoreQueryDTO queryDTO);
    Result<List<ScoreRecordDetailVO>> getScoresByEvent(Integer eventId);
    Result<List<Map<String, Object>>> getScoresByDateRange(Integer stuId, String startDate, String endDate);
    Result<?> exportScoreReport(Integer stuId);
}