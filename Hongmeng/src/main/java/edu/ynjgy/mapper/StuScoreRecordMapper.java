package edu.ynjgy.mapper;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import edu.ynjgy.entity.StuScoreRecord;

@Mapper
public interface StuScoreRecordMapper {

    @Select("SELECT * FROM stu_score_record WHERE score_id = #{scoreId}")
    StuScoreRecord selectById(Integer scoreId);

    @Select("SELECT * FROM stu_score_record WHERE stu_id = #{stuId}")
    List<StuScoreRecord> selectByStuId(Integer stuId);

    @Insert("INSERT INTO stu_score_record(stu_id, event_id, event_name, item_id, item_name, level_id, level_name, " +
            "base_score, level_index, final_score, raw_score, cert_date, cert_path, audit_status) " +
            "VALUES(#{stuId}, #{eventId}, #{eventName}, #{itemId}, #{itemName}, #{levelId}, #{levelName}, " +
            "#{baseScore}, #{levelIndex}, #{finalScore}, #{rawScore}, #{certDate}, #{certPath}, #{auditStatus})")
    @Options(useGeneratedKeys = true, keyProperty = "scoreId")
    int insert(StuScoreRecord record);

    @Select("SELECT IFNULL(SUM(final_score), 0) FROM stu_score_record WHERE stu_id = #{stuId}")
    BigDecimal sumScoreByStuId(Integer stuId);

    @Select("SELECT IFNULL(SUM(final_score), 0) FROM stu_score_record WHERE stu_id = #{stuId} AND (audit_status = 1 OR audit_status IS NULL)")
    BigDecimal sumApprovedScoreByStuId(Integer stuId);

    @Select("SELECT s.stu_id, s.stu_name, IFNULL(SUM(r.final_score), 0) as total_score " +
            "FROM student_info s LEFT JOIN stu_score_record r ON s.stu_id = r.stu_id " +
            "WHERE s.class_org_id = #{classId} GROUP BY s.stu_id, s.stu_name")
    List<Map<String, Object>> getClassScoreSummary(Integer classId);

    @Select("SELECT event_id, event_name, COUNT(*) as participant_count, AVG(final_score) as avg_score " +
            "FROM stu_score_record GROUP BY event_id, event_name")
    List<Map<String, Object>> getEventTrend();

    @Select("SELECT " +
            "  CASE " +
            "    WHEN r.final_score >= 90 THEN '优秀' " +
            "    WHEN r.final_score >= 75 THEN '良好' " +
            "    WHEN r.final_score >= 60 THEN '及格' " +
            "    ELSE '不及格' " +
            "  END as grade_level, " +
            "  COUNT(*) as count " +
            "FROM stu_score_record r " +
            "JOIN student_info s ON r.stu_id = s.stu_id " +
            "JOIN org_info o ON s.class_org_id = o.org_id " +
            "WHERE o.parent_org_code = (SELECT org_code FROM org_info WHERE org_id = #{majorId}) " +
            "GROUP BY grade_level")
    List<Map<String, Object>> getMajorScoreDistribution(Integer majorId);

    @Select("SELECT * FROM stu_score_record")
    List<StuScoreRecord> selectAll();

    @Select("SELECT * FROM stu_score_record WHERE event_id = #{eventId}")
    List<StuScoreRecord> selectByEventId(Integer eventId);

    @Update("UPDATE stu_score_record SET audit_status=#{auditStatus}, audit_remark=#{auditRemark}, " +
            "back_int1=#{backInt1}, back_str1=#{backStr1} WHERE score_id=#{scoreId}")
    int update(StuScoreRecord record);

    @Select("SELECT COUNT(*) FROM stu_score_record")
    int countAll();

    @Select("<script>" +
            "SELECT r.* FROM stu_score_record r " +
            "<if test='stuName != null or classOrgId != null'>" +
            "JOIN student_info s ON r.stu_id = s.stu_id " +
            "<if test='classOrgId != null'>AND s.class_org_id = #{classOrgId}</if> " +
            "</if>" +
            "WHERE 1=1 " +
            "<if test='stuId != null'>AND r.stu_id = #{stuId}</if> " +
            "<if test='eventId != null'>AND r.event_id = #{eventId}</if> " +
            "<if test='itemId != null'>AND r.item_id = #{itemId}</if> " +
            "<if test='levelId != null'>AND r.level_id = #{levelId}</if> " +
            "<if test='stuName != null and stuName != \"\"'>AND s.stu_name LIKE CONCAT('%', #{stuName}, '%')</if> " +
            "<if test='eventName != null and eventName != \"\"'>AND r.event_name LIKE CONCAT('%', #{eventName}, '%')</if> " +
            "<if test='startDate != null'>AND r.cert_date &gt;= #{startDate}</if> " +
            "<if test='endDate != null'>AND r.cert_date &lt;= #{endDate}</if> " +
            "ORDER BY r.score_id DESC LIMIT #{offset}, #{pageSize}" +
            "</script>")
    List<StuScoreRecord> queryPage(@Param("stuId") Integer stuId, @Param("eventId") Integer eventId,
                                    @Param("itemId") Integer itemId, @Param("levelId") Integer levelId,
                                    @Param("classOrgId") Integer classOrgId,
                                    @Param("stuName") String stuName, @Param("eventName") String eventName,
                                    @Param("startDate") LocalDate startDate, @Param("endDate") LocalDate endDate,
                                    @Param("offset") int offset, @Param("pageSize") int pageSize);

    @Select("<script>" +
            "SELECT COUNT(*) FROM stu_score_record r " +
            "<if test='stuName != null or classOrgId != null'>" +
            "JOIN student_info s ON r.stu_id = s.stu_id " +
            "<if test='classOrgId != null'>AND s.class_org_id = #{classOrgId}</if> " +
            "</if>" +
            "WHERE 1=1 " +
            "<if test='stuId != null'>AND r.stu_id = #{stuId}</if> " +
            "<if test='eventId != null'>AND r.event_id = #{eventId}</if> " +
            "<if test='itemId != null'>AND r.item_id = #{itemId}</if> " +
            "<if test='levelId != null'>AND r.level_id = #{levelId}</if> " +
            "<if test='stuName != null and stuName != \"\"'>AND s.stu_name LIKE CONCAT('%', #{stuName}, '%')</if> " +
            "<if test='eventName != null and eventName != \"\"'>AND r.event_name LIKE CONCAT('%', #{eventName}, '%')</if> " +
            "<if test='startDate != null'>AND r.cert_date &gt;= #{startDate}</if> " +
            "<if test='endDate != null'>AND r.cert_date &lt;= #{endDate}</if>" +
            "</script>")
    Long countQuery(@Param("stuId") Integer stuId, @Param("eventId") Integer eventId,
                    @Param("itemId") Integer itemId, @Param("levelId") Integer levelId,
                    @Param("classOrgId") Integer classOrgId,
                    @Param("stuName") String stuName, @Param("eventName") String eventName,
                    @Param("startDate") LocalDate startDate, @Param("endDate") LocalDate endDate);

    @Select("SELECT IFNULL(AVG(final_score), 0) FROM stu_score_record")
    BigDecimal getGlobalAvgScore();

    @Select("SELECT IFNULL(AVG(final_score), 0) FROM stu_score_record r " +
            "JOIN student_info s ON r.stu_id = s.stu_id " +
            "WHERE s.class_org_id = #{classId}")
    BigDecimal getClassAvgScore(Integer classId);

    @Select("SELECT s.stu_id, s.stu_name, SUM(r.final_score) as total_score " +
            "FROM stu_score_record r " +
            "JOIN student_info s ON r.stu_id = s.stu_id " +
            "GROUP BY s.stu_id, s.stu_name " +
            "ORDER BY total_score DESC LIMIT #{limit}")
    List<Map<String, Object>> getTopStudents(Integer limit);

    @Select("SELECT event_id, event_name, COUNT(*) as participant_count " +
            "FROM stu_score_record " +
            "GROUP BY event_id, event_name " +
            "ORDER BY participant_count DESC LIMIT #{limit}")
    List<Map<String, Object>> getPopularEvents(Integer limit);

    @Select("SELECT level_name, COUNT(*) as cnt " +
            "FROM stu_score_record " +
            "GROUP BY level_name " +
            "ORDER BY cnt DESC")
    List<Map<String, Object>> getLevelDistribution();

    @Select("SELECT DATE(cert_date) as score_date, COUNT(*) as count, AVG(final_score) as avg_score " +
            "FROM stu_score_record " +
            "WHERE stu_id = #{stuId} " +
            "AND cert_date BETWEEN #{startDate} AND #{endDate} " +
            "GROUP BY DATE(cert_date) " +
            "ORDER BY score_date")
    List<Map<String, Object>> getScoresByDateRange(Integer stuId, String startDate, String endDate);

    @Select("<script>" +
            "SELECT * FROM stu_score_record WHERE stu_id IN " +
            "<foreach item='id' collection='ids' open='(' separator=',' close=')'>#{id}</foreach>" +
            "</script>")
    List<StuScoreRecord> selectByStuIds(@Param("ids") List<Integer> ids);

    @Select("<script>" +
            "SELECT stu_id, IFNULL(SUM(final_score), 0) as total_score " +
            "FROM stu_score_record WHERE stu_id IN " +
            "<foreach item='id' collection='ids' open='(' separator=',' close=')'>#{id}</foreach> " +
            "GROUP BY stu_id" +
            "</script>")
    List<Map<String, Object>> sumScoresByStuIds(@Param("ids") List<Integer> ids);

    @Select("<script>" +
            "SELECT stu_id, COUNT(*) as cnt " +
            "FROM stu_score_record WHERE stu_id IN " +
            "<foreach item='id' collection='ids' open='(' separator=',' close=')'>#{id}</foreach> " +
            "GROUP BY stu_id" +
            "</script>")
    List<Map<String, Object>> countRecordsByStuIds(@Param("ids") List<Integer> ids);

    @Delete("DELETE FROM stu_score_record WHERE score_id = #{scoreId}")
    int deleteById(Integer scoreId);

    @Select("<script>" +
            "SELECT IFNULL(AVG(r.final_score), 0) as avgScore, " +
            "IFNULL(MAX(r.final_score), 0) as maxScore, " +
            "IFNULL(MIN(r.final_score), 0) as minScore " +
            "FROM stu_score_record r " +
            "JOIN student_info s ON r.stu_id = s.stu_id " +
            "WHERE 1=1 " +
            "<if test='classOrgId != null'>AND s.class_org_id = #{classOrgId}</if> " +
            "<if test='enrollYear != null and enrollYear != \"\"'>AND s.enroll_year = #{enrollYear}</if> " +
            "<if test='trainLevel != null and trainLevel != \"\"'>AND s.train_level LIKE CONCAT('%', #{trainLevel}, '%')</if>" +
            "</script>")
    Map<String, Object> getScoreStats(@Param("classOrgId") Integer classOrgId,
                                       @Param("enrollYear") String enrollYear,
                                       @Param("trainLevel") String trainLevel);
}
