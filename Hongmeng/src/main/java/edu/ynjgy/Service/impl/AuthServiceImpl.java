package edu.ynjgy.Service.impl;

import edu.ynjgy.Service.AuthService;
import edu.ynjgy.dto.LoginDTO;
import edu.ynjgy.dto.RegisterDTO;
import edu.ynjgy.entity.UserInfo;
import edu.ynjgy.entity.StudentInfo;
import edu.ynjgy.exception.BusinessException;
import edu.ynjgy.mapper.UserInfoMapper;
import edu.ynjgy.mapper.StudentInfoMapper;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {

    private final UserInfoMapper userInfoMapper;
    private final StudentInfoMapper studentInfoMapper;

    @Override
    public Result<?> login(LoginDTO loginDTO) {
        UserInfo user = userInfoMapper.selectByUsername(loginDTO.getUsername());
        if (user == null) {
            throw new BusinessException(401, "账号不存在");
        }
        if (!user.getPassword().equals(loginDTO.getPassword())) {
            throw new BusinessException(401, "密码错误");
        }
        if (!user.getRole().equals(loginDTO.getRole())) {
            throw new BusinessException(401, "角色不匹配，请选择正确的身份登录");
        }

        Map<String, Object> data = new HashMap<>();
        data.put("token", "token-" + user.getUserId() + "-" + user.getRole());
        data.put("userId", user.getUserId());
        data.put("username", user.getUsername());
        data.put("name", user.getName());
        data.put("role", user.getRole());
        
        // 学生登录时，额外返回 stuId
        if ("student".equals(user.getRole())) {
            StudentInfo student = studentInfoMapper.selectByStuNo(user.getUsername());
            if (student != null) {
                data.put("stuId", student.getStuId());
                data.put("classOrgId", student.getClassOrgId());
            }
        }
        
        return Result.success("登录成功", data);
    }

    @Override
    public Result<?> register(RegisterDTO registerDTO) {
        UserInfo existUser = userInfoMapper.selectByUsername(registerDTO.getUsername());
        if (existUser != null) {
            throw new BusinessException("该账号已被注册");
        }

        UserInfo userInfo = new UserInfo();
        userInfo.setUsername(registerDTO.getUsername());
        userInfo.setPassword(registerDTO.getPassword());
        userInfo.setName(registerDTO.getName());
        userInfo.setRole(registerDTO.getRole());
        userInfo.setPhone(registerDTO.getPhone());
        userInfo.setAdminCode(registerDTO.getAdminCode());
        userInfo.setDeptName(registerDTO.getDeptName());
        userInfo.setTitle(registerDTO.getTitle());
        userInfo.setClassOrgId(registerDTO.getClassOrgId());
        userInfo.setEnrollYear(registerDTO.getEnrollYear());

        userInfoMapper.insert(userInfo);
        return Result.success("注册成功");
    }
}
