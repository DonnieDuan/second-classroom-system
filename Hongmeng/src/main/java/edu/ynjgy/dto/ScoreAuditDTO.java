package edu.ynjgy.dto;
import lombok.Data;
import jakarta.validation.constraints.NotNull;

@Data
public class ScoreAuditDTO {
    @NotNull(message = "成绩记录ID不能为空")
    private Integer scoreId;

    @NotNull(message = "审核状态不能为空")
    private Integer auditStatus;

    private String auditRemark;
}
