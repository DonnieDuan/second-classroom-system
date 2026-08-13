package edu.ynjgy.entity;
import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Data
public class OrgInfo {
    private Integer orgId;
    private String orgCode;
    private String orgName;
    private Integer orgLevel;
    private String parentOrgCode;
    private String remark;
    private String backStr1;
    private String backStr2;
    private String backStr3;
    private List<OrgInfo> children = new ArrayList<>();
}