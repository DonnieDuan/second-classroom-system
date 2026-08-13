package edu.ynjgy.Controller;

import edu.ynjgy.Service.UserService;
import edu.ynjgy.entity.UserInfo;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/user")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/list")
    public Result<?> getUserList(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer pageSize,
            @RequestParam(required = false) String role) {
        return userService.getUserList(page, pageSize, role);
    }

    @PutMapping("/{userId}")
    public Result<?> updateUser(@PathVariable Integer userId, @RequestBody UserInfo userInfo) {
        userInfo.setUserId(userId);
        return userService.updateUser(userInfo);
    }

    @DeleteMapping("/{userId}")
    public Result<?> deleteUser(@PathVariable Integer userId) {
        return userService.deleteUser(userId);
    }
}