
package edu.ynjgy.dto;
import lombok.Data;
import java.time.LocalDate;

@Data
public class ScoreQueryDTO {
    private Integer stuId;
    private String stuName;
    private Integer eventId;
    private String eventName;
    private Integer itemId;
    private Integer levelId;
    private Integer classOrgId;
    private LocalDate startDate;
    private LocalDate endDate;
    private Integer pageNum = 1;
    private Integer pageSize = 10;
}
