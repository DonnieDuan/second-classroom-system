package edu.ynjgy.vo;

import lombok.Data;
import java.time.LocalDate;

@Data
public class StudentInfoVO {
    private Integer stuId;
    private String stuNo;
    private String stuName;
    private String gender;
    private String phone;
    private Integer classOrgId;
    private String className;
    private String enrollYear;
    private String idCard;
    private LocalDate birthDate;
    private String trainLevel;
}