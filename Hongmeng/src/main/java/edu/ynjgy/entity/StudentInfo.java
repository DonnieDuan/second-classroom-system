package edu.ynjgy.entity;
import lombok.Data;
import java.time.LocalDate;

@Data
public class StudentInfo {
    private Integer stuId;
    private String stuNo;
    private String stuName;
    private String gender;
    private String phone;
    private Integer classOrgId;
    private String enrollYear;
    private String idCard;
    private LocalDate birthDate;
    private String trainLevel;
    private String backStr1;
    private String backStr2;
    private String backStr3;
    private Integer backInt1;
    private Integer backInt2;
}