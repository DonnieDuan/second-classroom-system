package edu.ynjgy.vo;

import lombok.Data;
import java.util.List;

@Data
public class ClassInfoVO {
    private Integer orgId;
    private String orgCode;
    private String orgName;
    private Integer orgLevel;
    private String parentOrgCode;
    private List<StudentInfoVO> students;
    private Integer studentCount;
}