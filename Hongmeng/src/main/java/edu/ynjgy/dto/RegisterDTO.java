package edu.ynjgy.dto;

import lombok.Data;

@Data
public class RegisterDTO {
    private String username;
    private String password;
    private String name;
    private String role;
    private String phone;
    private String adminCode;
    private String deptName;
    private String title;
    private String classOrgId;
    private String enrollYear;
}
