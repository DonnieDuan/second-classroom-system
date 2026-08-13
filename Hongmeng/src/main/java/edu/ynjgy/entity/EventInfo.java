package edu.ynjgy.entity;
import lombok.Data;
import java.math.BigDecimal;

@Data
public class EventInfo {
    private Integer eventId;
    private String eventNo;
    private String eventName;
    private String hostUnit;
    private String eventLevel;
    private String eventDesc;
    private String charterPath;
    private Integer eventStatus;
    private BigDecimal baseScore;
    private String backStr1;
    private String backStr2;
    private String backStr3;
    private Integer backInt1;
    private Integer backInt2;
}