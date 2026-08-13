package edu.ynjgy.dto;

import lombok.Data;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.LocalDate;

@Data
public class ScoreSubmitDTO {
    @NotNull(message = "学生ID不能为空")
    private Integer stuId;

    @NotNull(message = "赛事ID不能为空")
    private Integer eventId;

    @NotNull(message = "赛项ID不能为空")
    private Integer itemId;

    private Integer levelId;

    private BigDecimal score;

    private LocalDate certDate;
    private String certPath;
}
