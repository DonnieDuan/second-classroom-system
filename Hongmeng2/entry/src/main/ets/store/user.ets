import preferences from '@ohos.data.preferences';

export interface UserState {
  userId: number;
  name: string;
  role: string;
  stuId?: number;
  classOrgId?: number;
  isLoggedIn: boolean;
}

let userState: UserState = {
  userId: 0,
  name: '',
  role: '',
  stuId: undefined,
  classOrgId: undefined,
  isLoggedIn: false
};

const STORAGE_KEY: string = 'user_state';

export async function initUser(): Promise<void> {
  try {
    const store = await preferences.getPreferences(getContext(), STORAGE_KEY);
    const savedValue = await store.get('user', '');
    const saved = savedValue as string;
    if (saved) {
      try {
        const parsed = JSON.parse(saved) as Partial<UserState>;
        if (parsed.userId !== undefined) {
          userState.userId = parsed.userId;
        }
        if (parsed.name !== undefined) {
          userState.name = parsed.name;
        }
        if (parsed.role !== undefined) {
          userState.role = parsed.role;
        }
        if (parsed.stuId !== undefined) {
          userState.stuId = parsed.stuId;
        }
        if (parsed.classOrgId !== undefined) {
          userState.classOrgId = parsed.classOrgId;
        }
        if (parsed.isLoggedIn !== undefined) {
          userState.isLoggedIn = parsed.isLoggedIn;
        }
      } catch (e) {
        console.error('解析保存的用户数据失败');
      }
    }
  } catch (e) {
    console.error('初始化用户存储失败');
  }
}

async function saveUser(): Promise<void> {
  try {
    const store = await preferences.getPreferences(getContext(), STORAGE_KEY);
    await store.put('user', JSON.stringify(userState));
    await store.flush();
  } catch (e) {
    console.error('保存用户数据失败');
  }
}

export function setUser(state: Partial<UserState>): void {
  if (state.userId !== undefined) {
    userState.userId = state.userId;
  }
  if (state.name !== undefined) {
    userState.name = state.name;
  }
  if (state.role !== undefined) {
    userState.role = state.role;
  }
  if (state.stuId !== undefined) {
    userState.stuId = state.stuId;
  }
  if (state.classOrgId !== undefined) {
    userState.classOrgId = state.classOrgId;
  }
  if (state.isLoggedIn !== undefined) {
    userState.isLoggedIn = state.isLoggedIn;
  }
  saveUser();
}

export function getUser(): UserState {
  return userState;
}

export function clearUser(): void {
  userState = {
    userId: 0,
    name: '',
    role: '',
    stuId: undefined,
    classOrgId: undefined,
    isLoggedIn: false
  };
  saveUser();
}

export function isStudent(): boolean {
  return userState.role === 'student' && userState.isLoggedIn;
}

export function getStuId(): number | undefined {
  return userState.stuId;
}