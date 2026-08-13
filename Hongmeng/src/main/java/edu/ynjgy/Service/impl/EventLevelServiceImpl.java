package edu.ynjgy.Service.impl;

import edu.ynjgy.Service.EventLevelService;
import edu.ynjgy.entity.EventLevelInfo;
import edu.ynjgy.mapper.EventLevelInfoMapper;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@RequiredArgsConstructor
public class EventLevelServiceImpl implements EventLevelService {

    private final EventLevelInfoMapper mapper;

    @Override
    public Result<List<EventLevelInfo>> getAllLevels() {
        return Result.success(mapper.selectAll());
    }

    @Override
    public Result<?> getLevelById(Integer levelId) {
        EventLevelInfo level = mapper.selectById(levelId);
        if (level == null) {
            return Result.error("级别不存在");
        }
        return Result.success(level);
    }

    @Override
    public Result<?> createLevel(EventLevelInfo level) {
        int rows = mapper.insert(level);
        if (rows > 0) return Result.success("创建成功");
        return Result.error("创建失败");
    }

    @Override
    public Result<?> updateLevel(Integer levelId, EventLevelInfo level) {
        level.setLevelId(levelId);
        int rows = mapper.update(level);
        if (rows > 0) return Result.success("更新成功");
        return Result.error("更新失败");
    }

    @Override
    public Result<?> deleteLevel(Integer levelId) {
        int rows = mapper.deleteById(levelId);
        if (rows > 0) return Result.success("删除成功");
        return Result.error("删除失败");
    }
}
