package edu.ynjgy.Service.impl;

import edu.ynjgy.Service.OrgService;
import edu.ynjgy.entity.OrgInfo;
import edu.ynjgy.mapper.OrgInfoMapper;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class OrgServiceImpl implements OrgService {

    private final OrgInfoMapper mapper;

    @Override
    public Result<List<OrgInfo>> getOrgTree() {
        List<OrgInfo> allOrgs = mapper.selectAll();
        List<OrgInfo> tree = buildOrgTree(allOrgs);
        return Result.success(tree);
    }

    private List<OrgInfo> buildOrgTree(List<OrgInfo> allOrgs) {
        List<OrgInfo> tree = new ArrayList<>();
        Map<String, OrgInfo> orgMap = new HashMap<>();
        
        for (OrgInfo org : allOrgs) {
            org.setChildren(new ArrayList<>());
            orgMap.put(org.getOrgCode(), org);
        }
        
        for (OrgInfo org : allOrgs) {
            String parentCode = org.getParentOrgCode();
            if (parentCode == null || parentCode.isEmpty()) {
                tree.add(org);
            } else {
                OrgInfo parent = orgMap.get(parentCode);
                if (parent != null) {
                    parent.getChildren().add(org);
                }
            }
        }
        
        return tree;
    }

    @Override
    public Result<?> getOrgById(Integer orgId) {
        OrgInfo org = mapper.selectById(orgId);
        if (org == null) return Result.error("机构不存在");
        return Result.success(org);
    }

    @Override
    public Result<?> createOrg(OrgInfo org) {
        int rows = mapper.insert(org);
        if (rows > 0) return Result.success("创建成功");
        return Result.error("创建失败");
    }

    @Override
    public Result<?> updateOrg(Integer orgId, OrgInfo org) {
        org.setOrgId(orgId);
        int rows = mapper.update(org);
        if (rows > 0) return Result.success("更新成功");
        return Result.error("更新失败");
    }

    @Override
    public Result<?> deleteOrg(Integer orgId) {
        int rows = mapper.deleteById(orgId);
        if (rows > 0) return Result.success("删除成功");
        return Result.error("删除失败");
    }
}
