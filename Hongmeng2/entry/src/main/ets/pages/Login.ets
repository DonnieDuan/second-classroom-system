import router from '@ohos.router';
import { studentLogin, LoginResponse } from '../api/auth';
import { setUser, initUser } from '../store/user';
import { ApiResult } from '../utils/http';

@Entry
@Component
struct Login {
  @State username: string = '';
  @State password: string = '';
  @State loading: boolean = false;
  @State errorMsg: string = '';

  aboutToAppear(): void {
    initUser();
  }

  build() {
    Column({ space: 20 }) {
      Text('第二课堂成绩管理')
        .fontSize(32)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 80 });

      TextInput({ placeholder: '请输入学号/工号' })
        .width('80%')
        .height(56)
        .borderRadius(12)
        .backgroundColor('#f5f7fa')
        .padding({ left: 20 })
        .onChange((value: string) => {
          this.username = value;
        });

      TextInput({ placeholder: '请输入密码' })
        .type(InputType.Password)
        .width('80%')
        .height(56)
        .borderRadius(12)
        .backgroundColor('#f5f7fa')
        .padding({ left: 20 })
        .onChange((value: string) => {
          this.password = value;
        });

      if (this.errorMsg) {
        Text(this.errorMsg)
          .fontColor('#ff4d4f')
          .fontSize(14)
          .textAlign(TextAlign.Center);
      }

      Button('学生登录')
        .width('80%')
        .height(56)
        .backgroundColor('#409EFF')
        .fontColor('#fff')
        .fontSize(18)
        .fontWeight(FontWeight.Medium)
        .borderRadius(12)
        .enabled(!this.loading)
        .onClick(() => this.doLogin());
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .backgroundColor('#f0f2f5');
  }

  async doLogin(): Promise<void> {
    if (!this.username || !this.password) {
      this.errorMsg = '请输入账号和密码';
      return;
    }
    this.loading = true;
    this.errorMsg = '';
    try {
      let result: ApiResult<LoginResponse> =
        await studentLogin({ username: this.username, password: this.password });
      if (result.code === 200) {
        setUser({
          userId: result.data.userId,
          name: result.data.name,
          role: 'student',
          stuId: result.data.stuId,
          classOrgId: result.data.classOrgId,
          isLoggedIn: true
        });
        try {
          await router.pushUrl({ url: 'pages/StudentHome' });
        } catch (e) {
          console.error(`跳转失败: ${(e as Object).toString()}`);
        }
      } else {
        this.errorMsg = result.msg || '登录失败';
      }
    } catch (e) {
      this.errorMsg = '网络连接失败，请检查后端服务';
      console.error(`登录异常: ${(e as Object).toString()}`);
    } finally {
      this.loading = false;
    }
  }
}
