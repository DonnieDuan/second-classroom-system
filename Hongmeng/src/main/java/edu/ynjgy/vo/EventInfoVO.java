package edu.ynjgy.vo;
import lombok.Data;
import java.math.BigDecimal;
@Data
public class EventInfoVO {
    private Integer eventId;
    private String eventNo;
    private String eventName;
    private String hostUnit;
    private String eventLevel;
    private String eventDesc;
    private String charterPath;
    private Integer eventStatus;
    private String statusDesc;
    private BigDecimal baseScore;
    private String backStr1;
    private Integer participantCount;
}
