package edu.ynjgy.entity;

import lombok.Data;
import java.math.BigDecimal;

@Data
public class EventLevelInfo {
    private Integer levelId;
    private String levelCode;
    private String levelName;
    private BigDecimal levelIndex;
    private String backStr1;
    private String backStr2;
    private Integer backInt1;
    private Integer backInt2;
}