package edu.ynjgy.Service;

import edu.ynjgy.entity.EventLevelInfo;
import edu.ynjgy.utils.Result;
import java.util.List;

public interface EventLevelService {
    Result<List<EventLevelInfo>> getAllLevels();
    Result<?> getLevelById(Integer levelId);
    Result<?> createLevel(EventLevelInfo level);
    Result<?> updateLevel(Integer levelId, EventLevelInfo level);
    Result<?> deleteLevel(Integer levelId);
}
