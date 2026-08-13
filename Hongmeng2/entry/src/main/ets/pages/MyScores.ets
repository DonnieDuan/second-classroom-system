import router from '@ohos.router';
import { getUser } from '../store/user';
import { getMyScores, getMyTotalScore } from '../api/score';
import type { StuScoreRecord } from '../api/score';

@Entry
@Component
struct MyScores {
  @State totalScore: number = 0;
  @State scoreCount: number = 0;
  @State scores: StuScoreRecord[] = [];
  @State loading: boolean = false;

  build() {
    Stack({ alignContent: Alignment.Bottom }) {
      Column() {
        Row() {
          Text('<')
            .fontSize(24)
            .fontColor('#fff')
            .width(40)
            .height(40)
            .textAlign(TextAlign.Center)
            .onClick(() => router.back());

          Text('我的成绩')
            .fontSize(20)
            .fontWeight(FontWeight.Bold)
            .fontColor('#fff')
            .flexGrow(1)
            .textAlign(TextAlign.Center);

          Blank().width(40);
        }
        .width('100%')
        .height(56)
        .padding({ left: 12, right: 12 })
        .backgroundColor('#409EFF');

        Scroll() {
          Column({ space: 20 }) {
            Row({ space: 16 }) {
              Column({ space: 8 }) {
                Text(`${this.totalScore}`)
                  .fontSize(40)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#409EFF');
                Text('总积分')
                  .fontSize(14)
                  .fontColor('#909399');
              }
              .width('46%')
              .height(100)
              .backgroundColor('#fff')
              .borderRadius(16)
              .justifyContent(FlexAlign.Center)
              .shadow({ radius: 8, color: '#00000008', offsetY: 2 });

              Column({ space: 8 }) {
                Text(`${this.scoreCount}`)
                  .fontSize(40)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#67C23A');
                Text('获奖次数')
                  .fontSize(14)
                  .fontColor('#909399');
              }
              .width('46%')
              .height(100)
              .backgroundColor('#fff')
              .borderRadius(16)
              .justifyContent(FlexAlign.Center)
              .shadow({ radius: 8, color: '#00000008', offsetY: 2 });
            }
            .width('100%')
            .padding({ left: 16, right: 16 });

            Column({ space: 16 }) {
              Row() {
                Text('成绩记录')
                  .fontSize(16)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#303133');
                Button('填报成绩')
                  .width(100)
                  .height(36)
                  .backgroundColor('#409EFF')
                  .fontColor('#fff')
                  .fontSize(14)
                  .borderRadius(18)
                  .onClick(() => router.pushUrl({ url: 'pages/ScoreSubmit' }));
              }
              .width('100%')
              .justifyContent(FlexAlign.SpaceBetween);

              if (this.scores.length > 0) {
                Column({ space: 10 }) {
                  ForEach(this.scores, (item: StuScoreRecord) => {
                    this.ScoreCard(item);
                  });
                }
                .width('100%');
              } else {
                Column({ space: 16 }) {
                  Text('📋')
                    .fontSize(48);
                  Text('暂无成绩记录')
                    .fontSize(15)
                    .fontColor('#909399');
                  Button('去填报')
                    .width(120)
                    .height(40)
                    .backgroundColor('#409EFF')
                    .fontColor('#fff')
                    .fontSize(15)
                    .borderRadius(20)
                    .onClick(() => router.pushUrl({ url: 'pages/ScoreSubmit' }));
                }
                .width('100%')
                .height(200)
                .backgroundColor('#fff')
                .borderRadius(16)
                .justifyContent(FlexAlign.Center)
                .shadow({ radius: 8, color: '#00000008', offsetY: 2 });
              }
            }
            .width('100%')
            .padding({ left: 16, right: 16 });

            Blank().height(80);
          }
          .width('100%');
        }
        .layoutWeight(1)
        .scrollBar(BarState.Off);
      }
      .width('100%')
      .height('100%')
      .backgroundColor('#f5f7fa');

      Row() {
        this.NavItem('🏠', '首页', false, 'pages/StudentHome');
        this.NavItem('📅', '计划', false, 'pages/StudyPlan');
        this.NavItem('✏️', '填报', false, 'pages/ScoreSubmit');
        this.NavItem('📈', '成绩', true, '');
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
  ScoreCard(item: StuScoreRecord) {
    Column({ space: 12 }) {
      Row({ space: 12 }) {
        Column({ space: 4 }) {
          Text(item.eventName)
            .fontSize(16)
            .fontWeight(FontWeight.Medium)
            .fontColor('#303133');
          Text(item.itemName)
            .fontSize(12)
            .fontColor('#909399');
        }
        .flexGrow(1);
        Text(`+${item.finalScore}`)
          .fontSize(22)
          .fontWeight(FontWeight.Bold)
          .fontColor(this.getScoreColor(item.auditStatus));
      }
      .width('100%');

      Row({ space: 12 }) {
        Text(item.levelName)
          .fontSize(12)
          .fontColor('#409EFF')
          .backgroundColor('#ecf5ff')
          .padding({ left: 8, right: 8, top: 2, bottom: 2 })
          .borderRadius(4);
        if (item.rawScore !== undefined && item.rawScore > 0) {
          Text(`原始分: ${item.rawScore}`)
            .fontSize(12)
            .fontColor('#909399');
        }
        Text(item.certDate)
          .fontSize(12)
          .fontColor('#909399');
      }
      .width('100%');

      Row({ space: 8 }) {
        Text(this.getAuditStatusText(item.auditStatus))
          .fontSize(12)
          .fontColor(this.getAuditStatusColor(item.auditStatus))
          .backgroundColor(this.getAuditStatusBgColor(item.auditStatus))
          .padding({ left: 8, right: 8, top: 2, bottom: 2 })
          .borderRadius(4);
        if (item.auditStatus === 2 && item.auditRemark) {
          Text(item.auditRemark)
            .fontSize(12)
            .fontColor('#ff4d4f')
            .maxLines(1)
            .flexGrow(1);
        }
      }
      .width('100%');
    }
    .width('100%')
    .padding({ left: 16, right: 16, top: 14, bottom: 14 })
    .backgroundColor('#fff')
    .borderRadius(16)
    .shadow({ radius: 6, color: '#00000006', offsetY: 2 });
  }

  getScoreColor(auditStatus: number): string {
    if (auditStatus === 1) {
      return '#67C23A';
    }
    return '#909399';
  }

  getAuditStatusText(auditStatus: number): string {
    if (auditStatus === 0) {
      return '待审核';
    } else if (auditStatus === 1) {
      return '已通过';
    } else if (auditStatus === 2) {
      return '未通过';
    }
    return '未知';
  }

  getAuditStatusColor(auditStatus: number): string {
    if (auditStatus === 0) {
      return '#E6A23C';
    } else if (auditStatus === 1) {
      return '#67C23A';
    } else if (auditStatus === 2) {
      return '#ff4d4f';
    }
    return '#909399';
  }

  getAuditStatusBgColor(auditStatus: number): string {
    if (auditStatus === 0) {
      return '#FDF6EC';
    } else if (auditStatus === 1) {
      return '#F0F9EB';
    } else if (auditStatus === 2) {
      return '#FEF0F0';
    }
    return '#f5f7fa';
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
    const stuId = getUser().stuId;
    if (!stuId) return;
    this.loading = true;
    try {
      const totalRes = await getMyTotalScore(stuId);
      const scoresRes = await getMyScores(stuId);
      this.totalScore = totalRes.data || 0;
      this.scores = scoresRes.data || [];
      this.scoreCount = this.scores.length;
    } catch (e) {
      console.error(`获取成绩失败: ${(e as Object).toString()}`);
    } finally {
      this.loading = false;
    }
  }
}
