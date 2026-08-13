package edu.ynjgy.mapper;

import edu.ynjgy.entity.ScoreRequire;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface ScoreRequireMapper {

    @Select("SELECT * FROM score_require WHERE req_id = #{reqId}")
    ScoreRequire selectById(Integer reqId);

    @Select("SELECT * FROM score_require")
    List<ScoreRequire> selectAll();

    @Select("SELECT * FROM score_require WHERE #{score} BETWEEN min_score AND max_score")
    ScoreRequire selectByScore(@Param("score") java.math.BigDecimal score);

    @Insert("INSERT INTO score_require(level_name, min_score, max_score) " +
            "VALUES(#{levelName}, #{minScore}, #{maxScore})")
    @Options(useGeneratedKeys = true, keyProperty = "reqId")
    int insert(ScoreRequire scoreRequire);

    @Update("UPDATE score_require SET level_name=#{levelName}, min_score=#{minScore}, max_score=#{maxScore} " +
            "WHERE req_id=#{reqId}")
    int update(ScoreRequire scoreRequire);

    @Delete("DELETE FROM score_require WHERE req_id=#{reqId}")
    int deleteById(Integer reqId);
}