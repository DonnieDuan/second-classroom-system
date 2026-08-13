package edu.ynjgy.Service;

import edu.ynjgy.dto.BatchScoreImportDTO;
import edu.ynjgy.dto.ScoreAuditDTO;
import edu.ynjgy.utils.Result;

import java.util.Map;

public interface AdminService {
    Result<?> auditScore(ScoreAuditDTO auditDTO);
    Result<?> batchImportScores(BatchScoreImportDTO importDTO);
    Result<Map<String, Object>> getDashboardStatistics();
    Result<?> generateClassReport(Integer classOrgId);
}
