package edu.ynjgy.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class UserInfo {
    private Integer userId;
    private String username;
    private String password;
    private String name;
    private String role;       // admin, teacher, student
    private String phone;
    private String adminCode;
    private String deptName;
    private String title;
    private String classOrgId;
    private String enrollYear;
    private LocalDateTime createTime;
}
