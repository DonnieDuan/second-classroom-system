package edu.ynjgy.mapper;
import edu.ynjgy.entity.ItemInfo;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface ItemInfoMapper {

    @Select("SELECT * FROM item_info WHERE item_id = #{itemId}")
    ItemInfo selectById(Integer itemId);

    @Select("SELECT * FROM item_info WHERE event_id = #{eventId}")
    List<ItemInfo> selectByEventId(Integer eventId);

    @Select("SELECT * FROM item_info")
    List<ItemInfo> selectAll();

    @Select("<script>" +
            "SELECT * FROM item_info WHERE 1=1 " +
            "<if test='eventId != null'>AND event_id = #{eventId}</if> " +
            "<if test='itemName != null and itemName != \"\"'>AND item_name LIKE CONCAT('%', #{itemName}, '%')</if> " +
            "ORDER BY item_id DESC LIMIT #{offset}, #{pageSize}" +
            "</script>")
    List<ItemInfo> selectPage(@Param("eventId") Integer eventId, @Param("itemName") String itemName,
                               @Param("offset") int offset, @Param("pageSize") int pageSize);

    @Select("<script>" +
            "SELECT COUNT(*) FROM item_info WHERE 1=1 " +
            "<if test='eventId != null'>AND event_id = #{eventId}</if> " +
            "<if test='itemName != null and itemName != \"\"'>AND item_name LIKE CONCAT('%', #{itemName}, '%')</if>" +
            "</script>")
    Long countFiltered(@Param("eventId") Integer eventId, @Param("itemName") String itemName);

    @Insert("INSERT INTO item_info(event_id, item_no, item_name, track_name, major_desc, team_type, open_cond, dept_name) " +
            "VALUES(#{eventId}, #{itemNo}, #{itemName}, #{trackName}, #{majorDesc}, #{teamType}, #{openCond}, #{deptName})")
    @Options(useGeneratedKeys = true, keyProperty = "itemId")
    int insert(ItemInfo item);

    @Update("UPDATE item_info SET event_id=#{eventId}, item_no=#{itemNo}, item_name=#{itemName}, " +
            "track_name=#{trackName}, major_desc=#{majorDesc}, team_type=#{teamType}, " +
            "open_cond=#{openCond}, dept_name=#{deptName} WHERE item_id=#{itemId}")
    int update(ItemInfo item);

    @Delete("DELETE FROM item_info WHERE item_id=#{itemId}")
    int deleteById(Integer itemId);
}
