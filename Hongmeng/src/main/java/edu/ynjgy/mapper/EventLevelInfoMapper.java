package edu.ynjgy.mapper;

import edu.ynjgy.entity.EventLevelInfo;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface EventLevelInfoMapper {

    @Select("SELECT * FROM event_level_info WHERE level_id = #{levelId}")
    EventLevelInfo selectById(Integer levelId);

    @Select("SELECT * FROM event_level_info")
    List<EventLevelInfo> selectAll();

    @Insert("INSERT INTO event_level_info(level_code, level_name, level_index) " +
            "VALUES(#{levelCode}, #{levelName}, #{levelIndex})")
    @Options(useGeneratedKeys = true, keyProperty = "levelId")
    int insert(EventLevelInfo level);

    @Update("UPDATE event_level_info SET level_code=#{levelCode}, level_name=#{levelName}, level_index=#{levelIndex} WHERE level_id=#{levelId}")
    int update(EventLevelInfo level);

    @Delete("DELETE FROM event_level_info WHERE level_id=#{levelId}")
    int deleteById(Integer levelId);
}