package edu.ynjgy.Service.impl;

import edu.ynjgy.Service.UserService;
import edu.ynjgy.entity.UserInfo;
import edu.ynjgy.mapper.UserInfoMapper;
import edu.ynjgy.utils.PageResult;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserInfoMapper userInfoMapper;

    @Override
    public Result<PageResult<UserInfo>> getUserList(Integer page, Integer pageSize, String role) {
        List<UserInfo> allUsers;
        Long total;

        if (role != null && !role.isEmpty()) {
            allUsers = userInfoMapper.selectByRole(role);
            total = userInfoMapper.countByRole(role);
        } else {
            allUsers = userInfoMapper.selectAll();
            total = userInfoMapper.countAll();
        }

        // 分页处理
        int start = (page - 1) * pageSize;
        int end = Math.min(start + pageSize, allUsers.size());
        List<UserInfo> pageUsers = allUsers.subList(start, end);

        PageResult<UserInfo> pageResult = new PageResult<>();
        pageResult.setTotal(total);
        pageResult.setRows(pageUsers);

        return Result.success(pageResult);
    }

    @Override
    public Result<UserInfo> getUserById(Integer userId) {
        // 暂不实现单个查询
        return Result.error("功能暂未实现");
    }

    @Override
    public Result<?> updateUser(UserInfo userInfo) {
        int rows = userInfoMapper.update(userInfo);
        if (rows > 0) {
            return Result.success("更新成功");
        }
        return Result.error("更新失败");
    }

    @Override
    public Result<?> deleteUser(Integer userId) {
        int rows = userInfoMapper.deleteById(userId);
        if (rows > 0) {
            return Result.success("删除成功");
        }
        return Result.error("删除失败");
    }
}