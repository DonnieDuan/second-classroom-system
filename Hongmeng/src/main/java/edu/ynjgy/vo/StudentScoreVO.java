package edu.ynjgy.vo;

import lombok.Data;
import java.math.BigDecimal;

@Data
public class StudentScoreVO {
    private Integer stuId;
    private String stuName;
    private BigDecimal totalScore;
    private String scoreLevel;
}