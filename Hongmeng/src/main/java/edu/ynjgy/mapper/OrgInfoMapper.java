package edu.ynjgy.mapper;

import edu.ynjgy.entity.OrgInfo;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface OrgInfoMapper {

    @Select("SELECT * FROM org_info")
    List<OrgInfo> selectAll();

    @Select("SELECT * FROM org_info WHERE org_id = #{orgId}")
    OrgInfo selectById(Integer orgId);

    @Select("SELECT * FROM org_info WHERE parent_org_code = #{parentOrgCode}")
    List<OrgInfo> selectByParentCode(String parentOrgCode);

    @Select("SELECT * FROM org_info WHERE org_level = #{level}")
    List<OrgInfo> selectByLevel(Integer level);

    @Insert("INSERT INTO org_info(org_code, org_name, org_level, parent_org_code, remark) " +
            "VALUES(#{orgCode}, #{orgName}, #{orgLevel}, #{parentOrgCode}, #{remark})")
    @Options(useGeneratedKeys = true, keyProperty = "orgId")
    int insert(OrgInfo orgInfo);

    @Update("UPDATE org_info SET org_name=#{orgName}, org_level=#{orgLevel}, parent_org_code=#{parentOrgCode}, " +
            "remark=#{remark} WHERE org_id=#{orgId}")
    int update(OrgInfo orgInfo);

    @Delete("DELETE FROM org_info WHERE org_id=#{orgId}")
    int deleteById(Integer orgId);
}
