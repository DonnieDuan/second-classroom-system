
        package edu.ynjgy.Controller;
import edu.ynjgy.Service.AdminService;
import edu.ynjgy.dto.BatchScoreImportDTO;
import edu.ynjgy.dto.ScoreAuditDTO;
import edu.ynjgy.utils.Result;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/admin")
@RequiredArgsConstructor
@Validated
public class AdminController {

    private final AdminService adminService;

    @PostMapping("/audit")
    public Result<?> auditScore(@Valid @RequestBody ScoreAuditDTO auditDTO) {
        return adminService.auditScore(auditDTO);
    }

    @PostMapping("/batchImport")
    public Result<?> batchImportScores(@Valid @RequestBody BatchScoreImportDTO importDTO) {
        return adminService.batchImportScores(importDTO);
    }

    @GetMapping("/dashboard")
    public Result<?> getDashboardStatistics() {
        return adminService.getDashboardStatistics();
    }

    @GetMapping("/report/class/{classOrgId}")
    public Result<?> generateClassReport(@PathVariable Integer classOrgId) {
        return adminService.generateClassReport(classOrgId);
    }
}
