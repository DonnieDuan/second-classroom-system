package edu.ynjgy.entity;
import lombok.Data;
import java.math.BigDecimal;

@Data
public class ScoreRequire {
    private Integer reqId;
    private String levelName;
    private BigDecimal minScore;
    private BigDecimal maxScore;
    private String backStr1;
    private String backStr2;
    private Integer backInt1;
    private Integer backInt2;
}