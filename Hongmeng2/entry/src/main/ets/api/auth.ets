import { httpClient, ApiResult } from '../utils/http';

export interface LoginResponse {
  userId: number;
  name: string;
  stuId?: number;
  classOrgId?: number;
}

export interface LoginForm {
  username: string;
  password: string;
}

interface LoginRequestData {
  username: string;
  password: string;
  role: string;
}

export async function studentLogin(form: LoginForm): Promise<ApiResult<LoginResponse>> {
  const data: LoginRequestData = { username: form.username, password: form.password, role: 'student' };
  return await httpClient.post('/auth/login', data);
}
