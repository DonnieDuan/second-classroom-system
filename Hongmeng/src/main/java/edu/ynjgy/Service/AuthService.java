package edu.ynjgy.Service;

import edu.ynjgy.dto.LoginDTO;
import edu.ynjgy.dto.RegisterDTO;
import edu.ynjgy.dto.WxLoginDTO;
import edu.ynjgy.utils.Result;

public interface AuthService {
    Result<?> login(LoginDTO loginDTO);
    Result<?> wxLogin(WxLoginDTO wxLoginDTO);
    Result<?> register(RegisterDTO registerDTO);
}
