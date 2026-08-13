import router from '@ohos.router';
import { getUser } from '../store/user';
import { getAllEvents, getMyTotalScore } from '../api/score';
import type { EventInfo } from '../api/score';

@Entry
@Component
struct StudyPlan {
  @State userName: string = '';
  @State totalScore: number = 0;
  @State requiredScore: number = 16;
  @State progress: number = 0;
  @State events: EventInfo[] = [];
  @State recommendedEvents: EventInfo[] = [];

  build() {
    Stack({ alignContent: Alignment.Bottom }) {
      Column() {
        // 顶部标题栏
        Row() {
          Text('<')
            .fontSize(24)
            .fontColor('#fff')
            .width(40)
            .height(40)
            .textAlign(TextAlign.Center)
            .onClick(() => router.back());

          Text('学习计划')
            .fontSize(20)
            .fontWeight(FontWeight.Bold)
            .fontColor('#fff')
            .flexGrow(1)
            .textAlign(TextAlign.Center);

          Blank().width(40);
        }
        .width('100%')
        .padding({ top: 40, left: 12, right: 12, bottom: 12 })
        .backgroundColor('#409EFF')
        .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP]);

        Scroll() {
          Column({ space: 12 }) {
            // 学分进度卡片
            Column({ space: 14 }) {
              Text('学分进度')
                .fontSize(15)
                .fontWeight(FontWeight.Bold)
                .fontColor('#303133')
                .alignSelf(ItemAlign.Start);

              Row() {
                Text(`${this.totalScore}`)
                  .fontSize(44)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#409EFF');
                Text(`/${this.requiredScore} 学分`)
                  .fontSize(16)
                  .fontColor('#909399');
              }
              .justifyContent(FlexAlign.Center);

              Progress({ value: this.progress, total: 100, type: ProgressType.Linear })
                .width('100%')
                .height(6)
                .color('#409EFF')
                .backgroundColor('#ebeef5');

              Text(`已完成 ${this.progress.toFixed(1)}%`)
                .fontSize(12)
                .fontColor('#909399')
                .textAlign(TextAlign.Center);
            }
            .width('100%')
            .padding(16)
            .backgroundColor('#fff')
            .borderRadius(12)
            .shadow({ radius: 4, color: '#00000006', offsetY: 1 });

            // 推荐赛事
            Column({ space: 10 }) {
              Text('推荐赛事')
                .fontSize(15)
                .fontWeight(FontWeight.Bold)
                .fontColor('#303133')
                .alignSelf(ItemAlign.Start);

              if (this.recommendedEvents.length > 0) {
                Column({ space: 8 }) {
                  ForEach(this.recommendedEvents, (item: EventInfo) => {
                    this.EventCard(item);
                  });
                }
                .width('100%');
              } else {
                Text('加载中...')
                  .fontSize(14)
                  .fontColor('#909399');
              }
            }
            .width('100%');

            // 赛事分类
            Column({ space: 10 }) {
              Text('赛事分类')
                .fontSize(15)
                .fontWeight(FontWeight.Bold)
                .fontColor('#303133')
                .alignSelf(ItemAlign.Start);

              Row({ space: 10 }) {
                this.CategoryCard('🏆', '学科竞赛', '国家级、省级、校级竞赛');
                this.CategoryCard('📝', '资格考试', '英语四六级、计算机等级等');
              }
              .width('100%');
            }
            .width('100%');

            // 学分要求说明
            Column({ space: 10 }) {
              Text('学分要求说明')
                .fontSize(15)
                .fontWeight(FontWeight.Bold)
                .fontColor('#303133')
                .alignSelf(ItemAlign.Start);

              Column({ space: 8 }) {
                this.RuleItem('1', '学科竞赛获奖可获得相应学分');
                this.RuleItem('2', '英语四级425分以上可得2-20学分');
                this.RuleItem('3', '英语六级425分以上可得3-25学分');
                this.RuleItem('4', '总学分达到16分为合格');
              }
              .width('100%')
              .padding(12)
              .backgroundColor('#fff')
              .borderRadius(12);
            }
            .width('100%');

            Blank().height(80);
          }
          .width('100%')
          .padding({ left: 16, right: 16, top: 12 });
        }
        .layoutWeight(1)
        .scrollBar(BarState.Off);
      }
      .width('100%')
      .height('100%')
      .backgroundColor('#f5f7fa');

      // 底部导航
      Row() {
        this.NavItem('🏠', '首页', false, 'pages/StudentHome');
        this.NavItem('📅', '计划', true, '');
        this.NavItem('✏️', '填报', false, 'pages/ScoreSubmit');
        this.NavItem('📈', '成绩', false, 'pages/MyScores');
      }
      .width('100%')
      .height(56)
      .backgroundColor('#fff')
      .shadow({ radius: 8, color: '#00000008', offsetY: -2 });
    }
    .width('100%')
    .height('100%');
  }

  @Builder
  EventCard(item: EventInfo) {
    Row({ space: 12 }) {
      Column({ space: 4 }) {
        Text(item.eventName)
          .fontSize(14)
          .fontWeight(FontWeight.Medium)
          .fontColor('#303133');
        Text(item.backStr1 === 'exam' ? '考试类' : '竞赛类')
          .fontSize(11)
          .fontColor('#409EFF')
          .backgroundColor('#ecf5ff')
          .padding({ left: 6, right: 6, top: 1, bottom: 1 })
          .borderRadius(4);
      }
      .flexGrow(1)
      .alignItems(HorizontalAlign.Start);

      Text('›')
        .fontSize(22)
        .fontColor('#C0C4CC');
    }
    .width('100%')
    .padding(14)
    .backgroundColor('#fff')
    .borderRadius(12)
    .shadow({ radius: 4, color: '#00000006', offsetY: 1 })
    .onClick(() => router.pushUrl({ url: 'pages/ScoreSubmit' }));
  }

  @Builder
  CategoryCard(icon: string, title: string, desc: string) {
    Column({ space: 4 }) {
      Text(icon)
        .fontSize(22);
      Text(title)
        .fontSize(13)
        .fontWeight(FontWeight.Medium)
        .fontColor('#303133');
      Text(desc)
        .fontSize(11)
        .fontColor('#909399');
    }
    .width('48%')
    .height(90)
    .backgroundColor('#fff')
    .borderRadius(12)
    .justifyContent(FlexAlign.Center)
    .shadow({ radius: 4, color: '#00000006', offsetY: 1 });
  }

  @Builder
  RuleItem(num: string, text: string) {
    Row({ space: 8 }) {
      Text(num)
        .fontSize(12)
        .fontWeight(FontWeight.Bold)
        .fontColor('#409EFF');
      Text(text)
        .fontSize(12)
        .fontColor('#606266')
        .flexGrow(1);
    }
    .width('100%');
  }

  @Builder
  NavItem(icon: string, label: string, active: boolean, page: string) {
    Column({ space: 2 }) {
      Text(icon)
        .fontSize(18);
      Text(label)
        .fontSize(11)
        .fontColor(active ? '#409EFF' : '#909399');
    }
    .width('25%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .onClick(() => {
      if (!active && page) {
        router.pushUrl({ url: page });
      }
    });
  }

  onPageShow(): void {
    const user = getUser();
    this.userName = user.name || '学生';
    this.fetchData();
  }

  async fetchData(): Promise<void> {
    try {
      const user = getUser();
      const stuId = user.stuId;

      const res = await getAllEvents();
      this.events = res.data || [];
      this.recommendedEvents = this.events.slice(0, 5);

      if (stuId !== undefined && stuId !== null) {
        const scoreRes = await getMyTotalScore(stuId);
        this.totalScore = typeof scoreRes.data === 'number' ? scoreRes.data : 0;
      } else {
        this.totalScore = 0;
      }
      this.progress = (this.totalScore / this.requiredScore) * 100;
    } catch (e) {
      console.error(`获取数据失败: ${(e as Object).toString()}`);
    }
  }
}
