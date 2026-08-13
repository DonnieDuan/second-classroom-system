package edu.ynjgy.Service;

import edu.ynjgy.dto.LoginDTO;
import edu.ynjgy.dto.RegisterDTO;
import edu.ynjgy.utils.Result;

public interface AuthService {
    Result<?> login(LoginDTO loginDTO);
    Result<?> register(RegisterDTO registerDTO);
}
