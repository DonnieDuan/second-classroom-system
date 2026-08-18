package edu.ynjgy.Service.impl;

import java.util.HashMap;
import java.util.Map;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import edu.ynjgy.Service.AuthService;
import edu.ynjgy.dto.LoginDTO;
import edu.ynjgy.dto.RegisterDTO;
import edu.ynjgy.dto.WxLoginDTO;
import edu.ynjgy.entity.StudentInfo;
import edu.ynjgy.entity.UserInfo;
import edu.ynjgy.exception.BusinessException;
import edu.ynjgy.mapper.StudentInfoMapper;
import edu.ynjgy.mapper.UserInfoMapper;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {

    private final UserInfoMapper userInfoMapper;
    private final StudentInfoMapper studentInfoMapper;
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @Override
    public Result<?> login(LoginDTO loginDTO) {
        UserInfo user = userInfoMapper.selectByUsername(loginDTO.getUsername());
        if (user == null) {
            throw new BusinessException(401, "账号不存在");
        }
        if (!verifyPassword(loginDTO.getPassword(), user.getPassword())) {
            throw new BusinessException(401, "密码错误");
        }
        if (!user.getRole().equals(loginDTO.getRole())) {
            throw new BusinessException(401, "角色不匹配，请选择正确的身份登录");
        }

        Map<String, Object> data = buildLoginData(user);
        return Result.success("登录成功", data);
    }

    private boolean verifyPassword(String rawPassword, String storedPassword) {
        if (storedPassword == null) {
            return false;
        }
        // BCrypt密码校验（以 $2a$ 开头）
        if (storedPassword.startsWith("$2a$")) {
            return passwordEncoder.matches(rawPassword, storedPassword);
        }
        // 明文密码校验（兼容旧数据）
        return storedPassword.equals(rawPassword);
    }

    @Override
    public Result<?> wxLogin(WxLoginDTO wxLoginDTO) {
        String code = wxLoginDTO.getCode();
        String stuNo = wxLoginDTO.getStuNo();
        
        // 优先用 stuNo 查找（小程序一键绑定学号场景）
        UserInfo user = null;
        if (stuNo != null && !stuNo.trim().isEmpty()) {
            user = userInfoMapper.selectByUsername(stuNo.trim());
        }
        
        // 如果没有 stuNo，用 code 作为学号查找（测试/演示场景）
        if (user == null && code != null && !code.trim().isEmpty()) {
            user = userInfoMapper.selectByUsername(code.trim());
        }
        
        // 都找不到，使用演示账号
        if (user == null) {
            user = userInfoMapper.selectByUsername("20231012023");
        }
        
        if (user == null) {
            throw new BusinessException(401, "账号不存在");
        }
        if (!"student".equals(user.getRole())) {
            throw new BusinessException(401, "该账号非学生身份");
        }

        Map<String, Object> data = buildLoginData(user);
        // 微信登录额外返回 code 用于追踪
        data.put("wxCode", code);
        return Result.success("微信登录成功", data);
    }

    private Map<String, Object> buildLoginData(UserInfo user) {
        Map<String, Object> data = new HashMap<>();
        data.put("token", "token-" + user.getUserId() + "-" + user.getRole());
        data.put("userId", user.getUserId());
        data.put("username", user.getUsername());
        data.put("name", user.getName());
        data.put("role", user.getRole());

        if ("student".equals(user.getRole())) {
            StudentInfo student = studentInfoMapper.selectByStuNo(user.getUsername());
            if (student != null) {
                data.put("stuId", student.getStuId());
                data.put("classOrgId", student.getClassOrgId());
            }
        }

        return data;
    }

    @Override
    public Result<?> register(RegisterDTO registerDTO) {
        UserInfo existUser = userInfoMapper.selectByUsername(registerDTO.getUsername());
        if (existUser != null) {
            throw new BusinessException("该账号已被注册");
        }

        UserInfo userInfo = new UserInfo();
        userInfo.setUsername(registerDTO.getUsername());
        // BCrypt加密存储密码
        userInfo.setPassword(passwordEncoder.encode(registerDTO.getPassword()));
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
