package edu.ynjgy.Controller;

import edu.ynjgy.Service.AuthService;
import edu.ynjgy.dto.LoginDTO;
import edu.ynjgy.dto.RegisterDTO;
import edu.ynjgy.dto.WxLoginDTO;
import edu.ynjgy.utils.Result;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
@Validated
public class AuthController {

    private final AuthService authService;

    @PostMapping("/login")
    public Result<?> login(@Valid @RequestBody LoginDTO loginDTO) {
        return authService.login(loginDTO);
    }

    @PostMapping("/wx-login")
    public Result<?> wxLogin(@RequestBody WxLoginDTO wxLoginDTO) {
        return authService.wxLogin(wxLoginDTO);
    }

    @PostMapping("/register")
    public Result<?> register(@Valid @RequestBody RegisterDTO registerDTO) {
        return authService.register(registerDTO);
    }
}
