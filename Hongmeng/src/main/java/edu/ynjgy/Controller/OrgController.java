package edu.ynjgy.Controller;

import edu.ynjgy.Service.OrgService;
import edu.ynjgy.entity.OrgInfo;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/org")
@RequiredArgsConstructor
public class OrgController {

    private final OrgService orgService;

    @GetMapping("/tree")
    public Result<?> getOrgTree() {
        return orgService.getOrgTree();
    }

    @GetMapping("/{orgId}")
    public Result<?> getOrgById(@PathVariable Integer orgId) {
        return orgService.getOrgById(orgId);
    }

    @PostMapping
    public Result<?> createOrg(@RequestBody OrgInfo orgInfo) {
        return orgService.createOrg(orgInfo);
    }

    @PutMapping("/{orgId}")
    public Result<?> updateOrg(@PathVariable Integer orgId, @RequestBody OrgInfo orgInfo) {
        return orgService.updateOrg(orgId, orgInfo);
    }

    @DeleteMapping("/{orgId}")
    public Result<?> deleteOrg(@PathVariable Integer orgId) {
        return orgService.deleteOrg(orgId);
    }

    @DeleteMapping
    public Result<?> batchDelete(@RequestParam String ids) {
        for (String id : ids.split(",")) {
            orgService.deleteOrg(Integer.parseInt(id.trim()));
        }
        return Result.success("删除成功");
    }
}
