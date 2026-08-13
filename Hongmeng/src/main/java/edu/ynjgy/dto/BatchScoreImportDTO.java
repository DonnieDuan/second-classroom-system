package edu.ynjgy.dto;

import lombok.Data;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDate;
import java.util.List;

@Data
public class BatchScoreImportDTO {
    @NotNull(message = "赛事ID不能为空")
    private Integer eventId;

    @NotNull(message = "赛项ID不能为空")
    private Integer itemId;

    @NotNull(message = "获奖级别ID不能为空")
    private Integer levelId;

    private LocalDate certDate;

    @NotNull(message = "成绩列表不能为空")
    private List<ScoreItem> scores;

    @Data
    public static class ScoreItem {
        @NotNull(message = "学生ID不能为空")
        private Integer stuId;
        private String certPath;
    }
}