package edu.ynjgy.Service;

import edu.ynjgy.entity.UserInfo;
import edu.ynjgy.utils.PageResult;
import edu.ynjgy.utils.Result;

public interface UserService {
    Result<PageResult<UserInfo>> getUserList(Integer page, Integer pageSize, String role);
    Result<UserInfo> getUserById(Integer userId);
    Result<?> updateUser(UserInfo userInfo);
    Result<?> deleteUser(Integer userId);
}