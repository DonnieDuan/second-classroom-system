import router from '@ohos.router';
import { getUser } from '../store/user';
import { getMyScores, getMyTotalScore } from '../api/score';
import type { StuScoreRecord } from '../api/score';

@Entry
@Component
struct StudentHome {
  @State userName: string = '';
  @State totalScore: number = 0;
  @State scoreCount: number = 0;
  @State recentScores: StuScoreRecord[] = [];
  @State loading: boolean = false;

  build() {
    Stack() {
      Column() {
        // 顶部标题栏
        Row() {
          Column({ space: 2 }) {
            Text('欢迎回来')
              .fontSize(13)
              .fontColor('#ffffff90');
            Text(`${this.userName}`)
              .fontSize(20)
              .fontWeight(FontWeight.Bold)
              .fontColor('#fff');
          }
          .alignItems(HorizontalAlign.Start)
          .flexGrow(1);

          Text('退出')
            .fontSize(14)
            .fontColor('#ffffff')
            .fontWeight(FontWeight.Medium)
            .padding({ left: 16, right: 16, top: 8, bottom: 8 })
            .onClick(() => {
              router.pushUrl({ url: 'pages/Login' });
            });
        }
        .width('100%')
        .padding({ top: 40, left: 20, right: 20, bottom: 12 })
        .backgroundColor('#409EFF')
        .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP]);

        Scroll() {
          Column({ space: 12 }) {
            // 统计概览卡片
            Row({ space: 12 }) {
              Column({ space: 4 }) {
                Text(`${this.totalScore}`)
                  .fontSize(28)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#409EFF');
                Text('总积分')
                  .fontSize(12)
                  .fontColor('#909399');
              }
              .width('48%')
              .height(72)
              .backgroundColor('#fff')
              .borderRadius(12)
              .justifyContent(FlexAlign.Center);

              Column({ space: 4 }) {
                Text(`${this.scoreCount}`)
                  .fontSize(28)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#67C23A');
                Text('获奖次数')
                  .fontSize(12)
                  .fontColor('#909399');
              }
              .width('48%')
              .height(72)
              .backgroundColor('#fff')
              .borderRadius(12)
              .justifyContent(FlexAlign.Center);
            }
            .width('100%')
            .padding({ left: 16, right: 16 })
            .margin({ top: -16 });

            // 快速入口
            Column({ space: 10 }) {
              Text('功能入口')
                .fontSize(15)
                .fontWeight(FontWeight.Bold)
                .fontColor('#303133')
                .alignSelf(ItemAlign.Start);

              Row({ space: 10 }) {
                this.QuickEntry('\uD83D\uDCDA', '学习计划', '#E6F2FF', '#409EFF', 'pages/StudyPlan');
                this.QuickEntry('\uD83D\uDCDC', '成绩填报', '#E6F7E6', '#67C23A', 'pages/ScoreSubmit');
                this.QuickEntry('\uD83D\uDCCA', '我的成绩', '#FFF5E6', '#E6A23C', 'pages/MyScores');
              }
              .width('100%');
            }
            .width('100%')
            .padding({ left: 16, right: 16, top: 8 });

            // 近期成绩
            Column({ space: 10 }) {
              Row() {
                Text('近期成绩')
                  .fontSize(15)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#303133');
                Text('查看全部')
                  .fontSize(12)
                  .fontColor('#409EFF')
                  .onClick(() => router.pushUrl({ url: 'pages/MyScores' }));
              }
              .width('100%')
              .justifyContent(FlexAlign.SpaceBetween);

              if (this.recentScores.length > 0) {
                Column({ space: 8 }) {
                  ForEach(this.recentScores, (item: StuScoreRecord) => {
                    this.ScoreItem(item);
                  });
                }
                .width('100%');
              } else {
                Column({ space: 12 }) {
                  Text('\uD83D\uDCCB')
                    .fontSize(36);
                  Text('暂无成绩记录')
                    .fontSize(14)
                    .fontColor('#909399');
                  Button('去填报')
                    .width(100)
                    .height(32)
                    .backgroundColor('#409EFF')
                    .fontColor('#fff')
                    .fontSize(13)
                    .borderRadius(16)
                    .onClick(() => router.pushUrl({ url: 'pages/ScoreSubmit' }));
                }
                .width('100%')
                .height(140)
                .backgroundColor('#fff')
                .borderRadius(12)
                .justifyContent(FlexAlign.Center);
              }
            }
            .width('100%')
            .padding({ left: 16, right: 16 });

            // 积分说明
            Column({ space: 8 }) {
              Text('积分说明')
                .fontSize(15)
                .fontWeight(FontWeight.Bold)
                .fontColor('#303133')
                .alignSelf(ItemAlign.Start);

              Column({ space: 6 }) {
                this.RuleItem('考试类', '按分数段获得对应积分');
                this.RuleItem('竞赛类', '按获奖级别获得对应积分');
                this.RuleItem('积分用途', '用于综合测评和奖学金评定');
              }
              .width('100%')
              .padding(12)
              .backgroundColor('#fff')
              .borderRadius(12);
            }
            .width('100%')
            .padding({ left: 16, right: 16 });

            Blank().height(80);
          }
          .width('100%');
        }
        .layoutWeight(1)
        .scrollBar(BarState.Off);

        // 底部导航
        Row() {
          this.NavItem('\uD83C\uDFE0', '首页', true, '');
          this.NavItem('\uD83D\uDCC5', '计划', false, 'pages/StudyPlan');
          this.NavItem('\u270F\uFE0F', '填报', false, 'pages/ScoreSubmit');
          this.NavItem('\uD83D\uDCC8', '成绩', false, 'pages/MyScores');
        }
        .width('100%')
        .height(56)
        .backgroundColor('#fff')
        .shadow({ radius: 8, color: '#00000008', offsetY: -2 });
      }
      .width('100%')
      .height('100%')
      .backgroundColor('#f5f7fa');
    }
    .width('100%')
    .height('100%');
  }

  @Builder
  QuickEntry(icon: string, label: string, bg: string, color: string, page: string) {
    Column({ space: 6 }) {
      Text(icon)
        .fontSize(22);
      Text(label)
        .fontSize(12)
        .fontColor('#303133');
    }
    .width('31%')
    .height(80)
    .backgroundColor('#fff')
    .borderRadius(12)
    .justifyContent(FlexAlign.Center)
    .shadow({ radius: 4, color: '#00000006', offsetY: 1 })
    .onClick(() => router.pushUrl({ url: page }));
  }

  @Builder
  ScoreItem(item: StuScoreRecord) {
    Row({ space: 12 }) {
      Column({ space: 4 }) {
        Text(item.eventName)
          .fontSize(14)
          .fontWeight(FontWeight.Medium)
          .fontColor('#303133');
        Text(item.certDate)
          .fontSize(12)
          .fontColor('#909399');
      }
      .flexGrow(1)
      .alignItems(HorizontalAlign.Start);

      Text(`+${item.finalScore}`)
        .fontSize(17)
        .fontWeight(FontWeight.Bold)
        .fontColor('#67C23A');
    }
    .width('100%')
    .padding(14)
    .backgroundColor('#fff')
    .borderRadius(12)
    .shadow({ radius: 4, color: '#00000006', offsetY: 1 });
  }

  @Builder
  RuleItem(label: string, desc: string) {
    Row({ space: 8 }) {
      Text(label)
        .fontSize(12)
        .fontColor('#409EFF')
        .backgroundColor('#ecf5ff')
        .padding({ left: 6, right: 6, top: 2, bottom: 2 })
        .borderRadius(4);
      Text(desc)
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
    this.fetchData();
  }

  async fetchData(): Promise<void> {
    this.loading = true;
    try {
      const user = getUser();
      this.userName = user.name || '';

      const stuId = user.stuId;
      if (stuId !== undefined && stuId !== null) {
        const scoreRes = await getMyTotalScore(stuId);
        const total = scoreRes.data ?? 0;
        this.totalScore = typeof total === 'number' ? total : 0;

        const scoresRes = await getMyScores(stuId);
        const scoresData = scoresRes.data ?? [];
        this.recentScores = Array.isArray(scoresData) ? scoresData.slice(0, 5) : [];
        this.scoreCount = this.recentScores.length;
      }
    } catch (e) {
      console.error(`获取数据失败: ${(e as Object).toString()}`);
    } finally {
      this.loading = false;
    }
  }
}
