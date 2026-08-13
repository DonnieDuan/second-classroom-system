package edu.ynjgy.Service;

import edu.ynjgy.utils.Result;
import java.util.Map;

public interface StatisticsService {
    Result<?> getClassScoreStatistics(Integer classId);
    Result<?> getEventTrendStatistics();
    Result<?> getMajorScoreStatistics(Integer majorId);
}