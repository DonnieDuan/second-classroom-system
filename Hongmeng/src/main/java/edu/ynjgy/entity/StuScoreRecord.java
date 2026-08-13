package edu.ynjgy.entity;

import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;

@Data
public class StuScoreRecord {
    private Integer scoreId;
    private Integer stuId;
    private Integer eventId;
    private String eventName;
    private Integer itemId;
    private String itemName;
    private Integer levelId;
    private String levelName;
    private BigDecimal baseScore;
    private BigDecimal levelIndex;
    private BigDecimal finalScore;
    private BigDecimal rawScore;
    private Integer scheduleId;
    private LocalDate certDate;
    private String certPath;
    private Integer auditStatus;
    private String auditRemark;
    private String backStr1;
    private String backStr2;
    private String backStr3;
    private Integer backInt1;
    private Integer backInt2;
}