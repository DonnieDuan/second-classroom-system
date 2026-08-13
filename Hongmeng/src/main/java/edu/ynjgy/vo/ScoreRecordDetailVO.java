package edu.ynjgy.vo;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;

@Data
public class ScoreRecordDetailVO {
    private Integer scoreId;
    private Integer stuId;
    private String stuName;
    private String stuNo;
    private Integer eventId;
    private String eventName;
    private Integer itemId;
    private String itemName;
    private Integer levelId;
    private String levelName;
    private BigDecimal baseScore;
    private BigDecimal levelIndex;
    private BigDecimal finalScore;
    private LocalDate certDate;
    private String certPath;
    private Integer auditStatus;
    private String auditRemark;
}
