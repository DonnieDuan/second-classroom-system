package edu.ynjgy.mapper;

import edu.ynjgy.entity.UserInfo;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface UserInfoMapper {

    @Select("SELECT * FROM user_info WHERE username = #{username}")
    UserInfo selectByUsername(@Param("username") String username);

    @Select("SELECT * FROM user_info ORDER BY create_time DESC")
    List<UserInfo> selectAll();

    @Select("SELECT * FROM user_info WHERE role = #{role} ORDER BY create_time DESC")
    List<UserInfo> selectByRole(@Param("role") String role);

    @Select("SELECT COUNT(*) FROM user_info")
    Long countAll();

    @Select("SELECT COUNT(*) FROM user_info WHERE role = #{role}")
    Long countByRole(@Param("role") String role);

    @Insert("INSERT INTO user_info (username, password, name, role, phone, admin_code, dept_name, title, class_org_id, enroll_year, create_time) " +
            "VALUES (#{username}, #{password}, #{name}, #{role}, #{phone}, #{adminCode}, #{deptName}, #{title}, #{classOrgId}, #{enrollYear}, NOW())")
    @Options(useGeneratedKeys = true, keyProperty = "userId")
    int insert(UserInfo userInfo);

    @Update("UPDATE user_info SET name=#{name}, role=#{role}, phone=#{phone}, dept_name=#{deptName}, title=#{title} WHERE user_id=#{userId}")
    int update(UserInfo userInfo);

    @Delete("DELETE FROM user_info WHERE user_id=#{userId}")
    int deleteById(@Param("userId") Integer userId);
}
