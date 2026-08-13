package edu.ynjgy.Service;

import edu.ynjgy.entity.OrgInfo;
import edu.ynjgy.utils.Result;
import java.util.List;

public interface OrgService {
    Result<List<OrgInfo>> getOrgTree();
    Result<?> getOrgById(Integer orgId);
    Result<?> createOrg(OrgInfo org);
    Result<?> updateOrg(Integer orgId, OrgInfo org);
    Result<?> deleteOrg(Integer orgId);
}
