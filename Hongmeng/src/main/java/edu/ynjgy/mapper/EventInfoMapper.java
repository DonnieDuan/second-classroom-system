package edu.ynjgy.mapper;

import edu.ynjgy.entity.EventInfo;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface EventInfoMapper {

    @Select("SELECT * FROM event_info WHERE event_id = #{eventId}")
    EventInfo selectById(Integer eventId);

    @Select("SELECT * FROM event_info WHERE event_status = #{status}")
    List<EventInfo> selectByStatus(Integer status);

    @Select("SELECT * FROM event_info")
    List<EventInfo> selectAll();

    @Select("<script>" +
            "SELECT * FROM event_info WHERE 1=1 " +
            "<if test='eventName != null and eventName != \"\"'>AND event_name LIKE CONCAT('%', #{eventName}, '%')</if> " +
            "<if test='eventLevel != null and eventLevel != \"\"'>AND event_level LIKE CONCAT('%', #{eventLevel}, '%')</if> " +
            "<if test='eventStatus != null'>AND event_status = #{eventStatus}</if> " +
            "ORDER BY event_id DESC LIMIT #{offset}, #{pageSize}" +
            "</script>")
    List<EventInfo> selectPage(@Param("eventName") String eventName, @Param("eventLevel") String eventLevel,
                                @Param("eventStatus") Integer eventStatus,
                                @Param("offset") int offset, @Param("pageSize") int pageSize);

    @Select("<script>" +
            "SELECT COUNT(*) FROM event_info WHERE 1=1 " +
            "<if test='eventName != null and eventName != \"\"'>AND event_name LIKE CONCAT('%', #{eventName}, '%')</if> " +
            "<if test='eventLevel != null and eventLevel != \"\"'>AND event_level LIKE CONCAT('%', #{eventLevel}, '%')</if> " +
            "<if test='eventStatus != null'>AND event_status = #{eventStatus}</if>" +
            "</script>")
    Long countFiltered(@Param("eventName") String eventName, @Param("eventLevel") String eventLevel,
                       @Param("eventStatus") Integer eventStatus);

    @Insert("INSERT INTO event_info(event_no, event_name, host_unit, event_level, event_desc, charter_path, event_status, base_score) " +
            "VALUES(#{eventNo}, #{eventName}, #{hostUnit}, #{eventLevel}, #{eventDesc}, #{charterPath}, #{eventStatus}, #{baseScore})")
    @Options(useGeneratedKeys = true, keyProperty = "eventId")
    int insert(EventInfo event);

    @Update("UPDATE event_info SET event_name=#{eventName}, host_unit=#{hostUnit}, event_level=#{eventLevel}, " +
            "event_desc=#{eventDesc}, event_status=#{eventStatus}, base_score=#{baseScore} WHERE event_id=#{eventId}")
    int update(EventInfo event);

    @Delete("DELETE FROM event_info WHERE event_id=#{eventId}")
    int deleteById(Integer eventId);

    @Select("SELECT COUNT(*) FROM event_info")
    int countAll();
}
