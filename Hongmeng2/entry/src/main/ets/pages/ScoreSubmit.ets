import router from '@ohos.router';
import { getUser } from '../store/user';
import { getAllEvents, getItemsByEvent, submitScore } from '../api/score';
import type { EventInfo, ItemInfo } from '../api/score';
import picker from '@ohos.file.picker';
import request from '@ohos.request';
import common from '@ohos.app.ability.common';
import { BASE_URL } from '../utils/http';

@Entry
@Component
struct ScoreSubmit {
  @State events: EventInfo[] = [];
  @State items: ItemInfo[] = [];
  @State selectedEventId: number = 0;
  @State selectedItemId: number = 0;
  @State examScore: number = 0;
  @State selectedLevelId: number = 0;
  @State certDate: string = '';
  @State certPath: string = '';
  @State certFileName: string = '';
  private levelIdMap: Map<string, number> = new Map([
    ['国家级-特等奖', 1],
    ['国家级-一等奖', 2],
    ['国家级-二等奖', 3],
    ['国家级-三等奖', 4],
    ['省级-特等奖', 5],
    ['省级-一等奖', 6],
    ['省级-二等奖', 7],
    ['省级-三等奖', 8],
    ['校级-一等奖', 9],
    ['校级-二等奖', 10]
  ]);
  @State isExam: boolean = false;
  @State loading: boolean = false;
  @State errorMsg: string = '';

  @State showPicker: boolean = false;
  @State pickerRange: string[] = [];
  @State pickerSelected: number = 0;
  @State pickerTitle: string = '';
  @State pickerMode: 'event' | 'item' | 'level' = 'event';

  @State showDatePicker: boolean = false;
  @State datePickerSelected: Date = new Date();
  private pendingDate: Date = new Date();

  private levelOptions: string[] = ['国家级-特等奖', '国家级-一等奖', '国家级-二等奖', '国家级-三等奖', '省级-特等奖', '省级-一等奖', '省级-二等奖', '省级-三等奖', '校级-一等奖', '校级-二等奖'];

  build() {
    Stack() {
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

          Text('成绩填报')
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
            // 表单卡片
            Column({ space: 14 }) {
              // 赛事选择
              Column({ space: 6 }) {
                Text('赛事名称')
                  .fontSize(13)
                  .fontColor('#303133')
                  .fontWeight(FontWeight.Medium);
                if (this.events.length > 0) {
                  this.SelectField(
                    this.getEventName(),
                    '请选择赛事',
                    () => this.openEventPicker()
                  )
                } else {
                  this.SelectField(
                    '',
                    '加载中...',
                    () => {}
                  )
                }
              }
              .width('100%');

              // 赛项选择
              Column({ space: 6 }) {
                Text('赛项名称')
                  .fontSize(13)
                  .fontColor('#303133')
                  .fontWeight(FontWeight.Medium);
                if (this.events.length > 0 && this.selectedEventId > 0) {
                  if (this.items.length > 0) {
                    this.SelectField(
                      this.getItemName(),
                      '请选择赛项',
                      () => this.openItemPicker()
                    )
                  } else {
                    this.SelectField(
                      '',
                      '加载中...',
                      () => {}
                    )
                  }
                } else {
                  this.SelectField(
                    '',
                    '请先选择赛事',
                    () => {}
                  )
                }
              }
              .width('100%');

              // 考试分数 / 获奖级别
              if (this.isExam) {
                Column({ space: 6 }) {
                  Text('考试分数')
                    .fontSize(13)
                    .fontColor('#303133')
                    .fontWeight(FontWeight.Medium);
                  TextInput({ placeholder: '请输入分数(0-750)' })
                    .width('100%')
                    .height(44)
                    .borderRadius(8)
                    .backgroundColor('#f5f7fa')
                    .padding({ left: 12 })
                    .type(InputType.Number)
                    .onChange((value: string) => {
                      this.examScore = parseInt(value);
                    });
                  Text('积分对照：425→2分  450→3分  500→5分  550→8分  600→10分  650→15分  700→20分')
                    .fontSize(11)
                    .fontColor('#909399');
                }
                .width('100%');
              } else {
                Column({ space: 6 }) {
                  Text('获奖级别')
                    .fontSize(13)
                    .fontColor('#303133')
                    .fontWeight(FontWeight.Medium);
                  this.SelectField(
                    this.getLevelName(),
                    '请选择获奖级别',
                    () => this.openLevelPicker()
                  )
                }
                .width('100%');
              }

              // 日期
              Column({ space: 6 }) {
                Text('获奖日期')
                  .fontSize(13)
                  .fontColor('#303133')
                  .fontWeight(FontWeight.Medium);
                this.SelectField(
                  this.certDate,
                  '请选择日期',
                  () => this.openDatePicker()
                )
              }
              .width('100%');

              // 证书上传
              Column({ space: 6 }) {
                Text('证书上传')
                  .fontSize(13)
                  .fontColor('#303133')
                  .fontWeight(FontWeight.Medium);
                Button(this.certFileName || '点击上传证书')
                  .width('100%')
                  .height(44)
                  .borderRadius(8)
                  .backgroundColor(this.certFileName ? '#e8f4fd' : '#f5f7fa')
                  .fontColor(this.certFileName ? '#409EFF' : '#909399')
                  .fontSize(14)
                  .onClick(() => this.chooseCertFile());
                if (this.certFileName) {
                  Text('已上传: ' + this.certFileName)
                    .fontSize(12)
                    .fontColor('#67c23a')
                    .width('100%');
                }
              }
              .width('100%');

              // 错误提示
              if (this.errorMsg) {
                Text(this.errorMsg)
                  .fontColor('#ff4d4f')
                  .fontSize(13)
                  .width('100%');
              }

              // 提交按钮
              Button('提交成绩')
                .width('100%')
                .height(46)
                .backgroundColor('#409EFF')
                .fontColor('#fff')
                .fontSize(16)
                .fontWeight(FontWeight.Medium)
                .borderRadius(23)
                .enabled(!this.loading)
                .onClick(() => this.doSubmit());
            }
            .width('100%')
            .padding(16)
            .backgroundColor('#fff')
            .borderRadius(12)
            .shadow({ radius: 6, color: '#00000008', offsetY: 1 });

            Blank().height(80);
          }
          .width('100%')
          .padding({ left: 16, right: 16, top: 12 });
        }
        .layoutWeight(1)
        .scrollBar(BarState.Off);

        // 底部导航
        Row() {
          this.NavItem('\uD83C\uDFE0', '首页', false, 'pages/StudentHome');
          this.NavItem('\uD83D\uDCC5', '计划', false, 'pages/StudyPlan');
          this.NavItem('\u270F\uFE0F', '填报', true, '');
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

      // 底部选择弹窗
      if (this.showPicker) {
        Stack({ alignContent: Alignment.Bottom }) {
          Column()
            .width('100%')
            .height('100%')
            .backgroundColor('#00000040')
            .onClick(() => this.showPicker = false)

          Column({ space: 0 }) {
            Row() {
              Text('取消')
                .fontSize(16)
                .fontColor('#909399')
                .onClick(() => this.showPicker = false)
              Blank()
              Text(this.pickerTitle)
                .fontSize(16)
                .fontColor('#303133')
                .fontWeight(FontWeight.Medium)
              Blank()
              Text('确定')
                .fontSize(16)
                .fontColor('#409EFF')
                .fontWeight(FontWeight.Medium)
                .onClick(() => {
                  if (this.pickerMode === 'event') {
                    const event = this.events[this.pickerSelected];
                    if (event) {
                      this.selectedEventId = event.eventId;
                      this.isExam = event.backStr1 === 'exam';
                      this.selectedItemId = 0;
                      this.selectedLevelId = 0;
                      this.examScore = 0;
                      this.items = [];
                      this.fetchItems();
                    }
                  } else if (this.pickerMode === 'item') {
                    const item = this.items[this.pickerSelected];
                    if (item) {
                      this.selectedItemId = item.itemId;
                    }
                  } else if (this.pickerMode === 'level') {
                    const levelName = this.pickerRange[this.pickerSelected];
                    const levelId = this.levelIdMap.get(levelName);
                    this.selectedLevelId = levelId || 1;
                  }
                  setTimeout(() => {
                    this.showPicker = false;
                  }, 50);
                })
            }
            .width('100%')
            .padding(16)
            .height(56)

            List() {
              ForEach(this.pickerRange, (item: string, index: number) => {
                ListItem() {
                  Text(item)
                    .fontSize(16)
                    .fontColor(this.pickerSelected === index ? '#409EFF' : '#303133')
                    .fontWeight(this.pickerSelected === index ? FontWeight.Bold : FontWeight.Normal)
                    .width('100%')
                    .height(44)
                    .textAlign(TextAlign.Center)
                }
                .width('100%')
                .onClick(() => {
                  this.pickerSelected = index;
                })
              })
            }
            .width('100%')
            .height(200)
            .divider({ strokeWidth: 0.5, color: '#ebeef5' })
          }
          .width('100%')
          .backgroundColor('#fff')
          .borderRadius({ topLeft: 20, topRight: 20 })
        }
        .width('100%')
        .height('100%')
      }

      // 底部日期弹窗
      if (this.showDatePicker) {
        Stack({ alignContent: Alignment.Bottom }) {
          Column()
            .width('100%')
            .height('100%')
            .backgroundColor('#00000040')
            .onClick(() => this.showDatePicker = false)

          Column({ space: 0 }) {
            Row() {
              Text('取消')
                .fontSize(16)
                .fontColor('#909399')
                .onClick(() => this.showDatePicker = false)
              Blank()
              Text('选择日期')
                .fontSize(16)
                .fontColor('#303133')
                .fontWeight(FontWeight.Medium)
              Blank()
              Text('确定')
                .fontSize(16)
                .fontColor('#409EFF')
                .fontWeight(FontWeight.Medium)
                .onClick(() => {
                  this.datePickerSelected = new Date(this.pendingDate);
                  const y = this.pendingDate.getFullYear();
                  const m = String(this.pendingDate.getMonth() + 1).padStart(2, '0');
                  const d = String(this.pendingDate.getDate()).padStart(2, '0');
                  this.certDate = `${y}-${m}-${d}`;
                  setTimeout(() => {
                    this.showDatePicker = false;
                  }, 50);
                })
            }
            .width('100%')
            .padding(16)
            .height(56)

            DatePicker({
              start: new Date('1900-1-1'),
              end: new Date('2100-12-31'),
              selected: this.datePickerSelected
            })
              .width('100%')
              .height(200)
              .onChange((value: DatePickerResult) => {
                const year = value.year !== undefined ? value.year : this.pendingDate.getFullYear()
                const month = value.month !== undefined ? value.month : (this.pendingDate.getMonth() + 1)
                const day = value.day !== undefined ? value.day : this.pendingDate.getDate()
                this.pendingDate = new Date(year, month - 1, day)
              })
          }
          .width('100%')
          .backgroundColor('#fff')
          .borderRadius({ topLeft: 20, topRight: 20 })
        }
        .width('100%')
        .height('100%')
      }
    }
    .width('100%')
    .height('100%');
  }

  @Builder
  SelectField(value: string, placeholder: string, onClick: () => void) {
    Row() {
      Text(value || placeholder)
        .fontSize(14)
        .fontColor(value ? '#303133' : '#909399')
        .flexGrow(1);
      Text('\u25BC')
        .fontSize(10)
        .fontColor('#C0C4CC');
    }
    .width('100%')
    .height(44)
    .backgroundColor('#f5f7fa')
    .borderRadius(8)
    .padding({ left: 12, right: 12 })
    .onClick(onClick);
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

  getEventName(): string {
    const event = this.events.find((e: EventInfo): boolean => e.eventId === this.selectedEventId);
    return event ? event.eventName : '';
  }

  getItemName(): string {
    const item = this.items.find((i: ItemInfo): boolean => i.itemId === this.selectedItemId);
    return item ? item.itemName : '';
  }

  getLevelName(): string {
    if (this.selectedLevelId > 0 && this.selectedLevelId <= this.levelOptions.length) {
      return this.levelOptions[this.selectedLevelId - 1];
    }
    return '';
  }

  openEventPicker(): void {
    const currentIndex = this.events.findIndex((e: EventInfo): boolean => e.eventId === this.selectedEventId);
    this.pickerRange = this.events.map((e: EventInfo) => e.eventName);
    this.pickerSelected = currentIndex >= 0 ? currentIndex : 0;
    this.pickerTitle = '选择赛事';
    this.pickerMode = 'event';
    this.showPicker = true;
  }

  openItemPicker(): void {
    const currentIndex = this.items.findIndex((i: ItemInfo): boolean => i.itemId === this.selectedItemId);
    this.pickerRange = this.items.map((i: ItemInfo) => i.itemName);
    this.pickerSelected = currentIndex >= 0 ? currentIndex : 0;
    this.pickerTitle = '选择赛项';
    this.pickerMode = 'item';
    this.showPicker = true;
  }

  openLevelPicker(): void {
    this.pickerRange = this.levelOptions;
    this.pickerSelected = this.selectedLevelId > 0 ? this.selectedLevelId - 1 : 0;
    this.pickerTitle = '选择获奖级别';
    this.pickerMode = 'level';
    this.showPicker = true;
  }

  openDatePicker(): void {
    const dateValue: string = this.certDate;
    this.datePickerSelected = dateValue ? new Date(dateValue) : new Date();
    this.pendingDate = new Date(this.datePickerSelected.getTime());
    this.showDatePicker = true;
  }

  async chooseCertFile(): Promise<void> {
    try {
      const photoPicker = new picker.PhotoViewPicker();
      const selectOptions = new picker.PhotoSelectOptions();
      selectOptions.maxSelectNumber = 1;
      const result: picker.PhotoSelectResult = await photoPicker.select(selectOptions);
      if (result.photoUris && result.photoUris.length > 0) {
        const uri: string = result.photoUris[0];
        this.certFileName = uri.substring(uri.lastIndexOf('/') + 1);
        this.certPath = uri;
        await this.uploadCertFile(uri);
      }
    } catch (e) {
      console.error(`选择文件失败: ${(e as Object).toString()}`);
      this.errorMsg = '选择文件失败';
    }
  }

  async uploadCertFile(uri: string): Promise<void> {
    try {
      const context: common.UIAbilityContext = getContext(this) as common.UIAbilityContext;
      const config: request.UploadConfig = {
        url: `${BASE_URL}/upload/cert`,
        method: 'POST',
        header: { 'Content-Type': 'multipart/form-data' },
        files: [{ filename: 'file', name: 'file', uri: uri, type: 'image/jpeg' }],
        data: []
      };
      const task: request.UploadTask = await request.uploadFile(context, config);
      task.on('complete', () => {
        console.info('文件上传完成');
      });
      task.on('fail', () => {
        this.errorMsg = '文件上传失败';
      });
    } catch (e) {
      console.error(`上传文件失败: ${(e as Object).toString()}`);
      this.errorMsg = '文件上传失败';
    }
  }

  onPageShow(): void {
    this.fetchEvents();
  }

  async fetchEvents(): Promise<void> {
    try {
      const res = await getAllEvents();
      this.events = res.data || [];
      if (this.events.length > 0) {
        this.selectedEventId = this.events[0].eventId;
        this.isExam = this.events[0].backStr1 === 'exam';
        await this.fetchItems();
      }
    } catch (e) {
      console.error(`获取赛事列表失败: ${(e as Object).toString()}`);
    }
  }

  async fetchItems(): Promise<void> {
    if (!this.selectedEventId) return;
    try {
      const res = await getItemsByEvent(this.selectedEventId);
      this.items = res.data || [];
      if (this.items.length > 0) {
        this.selectedItemId = this.items[0].itemId;
      } else {
        this.selectedItemId = 0;
      }
    } catch (e) {
      console.error(`获取赛项列表失败: ${(e as Object).toString()}`);
      this.items = [];
      this.selectedItemId = 0;
    }
  }

  aboutToAppear(): void {
    const user = getUser();
    if (!user.isLoggedIn) {
      try {
        router.pushUrl({ url: 'pages/Login' });
      } catch (e) {
        console.error(`跳转登录失败: ${(e as Object).toString()}`);
      }
    }
  }

  async doSubmit(): Promise<void> {
    const user = getUser();
    console.log(`当前用户信息: userId=${user.userId}, name=${user.name}, role=${user.role}, stuId=${user.stuId}, isLoggedIn=${user.isLoggedIn}`);
    const stuId = user.stuId;
    if (!user.isLoggedIn) {
      this.errorMsg = '请先登录';
      try {
        await router.pushUrl({ url: 'pages/Login' });
      } catch (e) {
        console.error(`跳转登录失败: ${(e as Object).toString()}`);
      }
      return;
    }
    if (!stuId) {
      this.errorMsg = '用户学号信息无效';
      return;
    }
    if (!this.selectedEventId) {
      this.errorMsg = '请选择赛事';
      return;
    }
    if (!this.selectedItemId) {
      this.errorMsg = '请选择赛项';
      return;
    }
    if (!this.isExam && !this.selectedLevelId) {
      this.errorMsg = '请选择获奖级别';
      return;
    }
    if (this.isExam && (this.examScore <= 0 || this.examScore > 750)) {
      this.errorMsg = '请输入有效的考试分数(0-750)';
      return;
    }
    if (!this.certDate || this.certDate.includes('请选择')) {
      this.errorMsg = '请选择日期';
      return;
    }

    this.loading = true;
    this.errorMsg = '';
    try {
      const result = await submitScore({
        stuId: stuId,
        eventId: this.selectedEventId,
        itemId: this.selectedItemId,
        score: this.isExam ? this.examScore : undefined,
        levelId: this.isExam ? undefined : this.selectedLevelId,
        certDate: this.certDate,
        certPath: this.certPath || undefined
      });
      if (result.code === 200) {
        router.pushUrl({ url: 'pages/MyScores' });
      } else {
        this.errorMsg = result.msg || '提交失败';
      }
    } catch (e) {
      this.errorMsg = '网络连接失败';
      console.error(`提交失败: ${(e as Object).toString()}`);
    } finally {
      this.loading = false;
    }
  }
}
