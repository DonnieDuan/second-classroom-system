package edu.ynjgy.mapper;

import edu.ynjgy.entity.StudentInfo;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface StudentInfoMapper {

    @Select("SELECT * FROM student_info WHERE stu_id = #{stuId}")
    StudentInfo selectById(Integer stuId);

    @Select("SELECT * FROM student_info WHERE stu_no = #{stuNo}")
    StudentInfo selectByStuNo(String stuNo);

    @Select("SELECT * FROM student_info WHERE class_org_id = #{classOrgId}")
    List<StudentInfo> selectByClassId(Integer classOrgId);

    @Insert("INSERT INTO student_info(stu_no, stu_name, gender, phone, class_org_id, enroll_year, id_card, birth_date, train_level) " +
            "VALUES(#{stuNo}, #{stuName}, #{gender}, #{phone}, #{classOrgId}, #{enrollYear}, #{idCard}, #{birthDate}, #{trainLevel})")
    @Options(useGeneratedKeys = true, keyProperty = "stuId")
    int insert(StudentInfo student);

    @Update("UPDATE student_info SET stu_name=#{stuName}, gender=#{gender}, phone=#{phone}, " +
            "class_org_id=#{classOrgId}, enroll_year=#{enrollYear}, id_card=#{idCard}, " +
            "birth_date=#{birthDate}, train_level=#{trainLevel} WHERE stu_id=#{stuId}")
    int update(StudentInfo student);

    @Delete("DELETE FROM student_info WHERE stu_id=#{stuId}")
    int deleteById(Integer stuId);

    @Select("SELECT * FROM student_info")
    List<StudentInfo> selectAll();

    @Select("SELECT COUNT(*) FROM student_info")
    int countAll();

    @Select("<script>" +
            "SELECT * FROM student_info WHERE 1=1 " +
            "<if test='keyword != null and keyword != \"\"'>" +
            "AND (stu_name LIKE CONCAT('%', #{keyword}, '%') OR stu_no LIKE CONCAT('%', #{keyword}, '%'))" +
            "</if> " +
            "<if test='gender != null and gender != \"\"'>AND gender = #{gender}</if> " +
            "<if test='classOrgId != null'>AND class_org_id = #{classOrgId}</if> " +
            "<if test='enrollYear != null and enrollYear != \"\"'>AND enroll_year = #{enrollYear}</if> " +
            "<if test='trainLevel != null and trainLevel != \"\"'>AND train_level LIKE CONCAT('%', #{trainLevel}, '%')</if> " +
            "ORDER BY stu_id DESC LIMIT #{offset}, #{pageSize}" +
            "</script>")
    List<StudentInfo> searchPage(@Param("keyword") String keyword,
                                  @Param("gender") String gender,
                                  @Param("classOrgId") Integer classOrgId,
                                  @Param("enrollYear") String enrollYear,
                                  @Param("trainLevel") String trainLevel,
                                  @Param("offset") int offset, @Param("pageSize") int pageSize);

    @Select("<script>" +
            "SELECT COUNT(*) FROM student_info WHERE 1=1 " +
            "<if test='keyword != null and keyword != \"\"'>" +
            "AND (stu_name LIKE CONCAT('%', #{keyword}, '%') OR stu_no LIKE CONCAT('%', #{keyword}, '%'))" +
            "</if>" +
            "<if test='gender != null and gender != \"\"'>AND gender = #{gender}</if> " +
            "<if test='classOrgId != null'>AND class_org_id = #{classOrgId}</if> " +
            "<if test='enrollYear != null and enrollYear != \"\"'>AND enroll_year = #{enrollYear}</if> " +
            "<if test='trainLevel != null and trainLevel != \"\"'>AND train_level LIKE CONCAT('%', #{trainLevel}, '%')</if>" +
            "</script>")
    Long countSearch(@Param("keyword") String keyword,
                     @Param("gender") String gender,
                     @Param("classOrgId") Integer classOrgId,
                     @Param("enrollYear") String enrollYear,
                     @Param("trainLevel") String trainLevel);

    @Select("<script>" +
            "SELECT * FROM student_info WHERE 1=1 " +
            "<if test='classOrgId != null'>AND class_org_id = #{classOrgId}</if> " +
            "<if test='enrollYear != null and enrollYear != \"\"'>AND enroll_year = #{enrollYear}</if> " +
            "<if test='trainLevel != null and trainLevel != \"\"'>AND train_level LIKE CONCAT('%', #{trainLevel}, '%')</if> " +
            "ORDER BY stu_id DESC LIMIT #{offset}, #{pageSize}" +
            "</script>")
    List<StudentInfo> selectSummaryPage(@Param("classOrgId") Integer classOrgId,
                                         @Param("enrollYear") String enrollYear,
                                         @Param("trainLevel") String trainLevel,
                                         @Param("offset") int offset, @Param("pageSize") int pageSize);

    @Select("<script>" +
            "SELECT COUNT(*) FROM student_info WHERE 1=1 " +
            "<if test='classOrgId != null'>AND class_org_id = #{classOrgId}</if> " +
            "<if test='enrollYear != null and enrollYear != \"\"'>AND enroll_year = #{enrollYear}</if> " +
            "<if test='trainLevel != null and trainLevel != \"\"'>AND train_level LIKE CONCAT('%', #{trainLevel}, '%')</if>" +
            "</script>")
    Long countSummary(@Param("classOrgId") Integer classOrgId,
                      @Param("enrollYear") String enrollYear,
                      @Param("trainLevel") String trainLevel);

    @Select("<script>" +
            "SELECT * FROM student_info WHERE stu_id IN " +
            "<foreach item='id' collection='ids' open='(' separator=',' close=')'>#{id}</foreach>" +
            "</script>")
    List<StudentInfo> selectByIds(@Param("ids") List<Integer> ids);
}
