# -*- coding: utf-8 -*-
"""
生成微信小程序学生端页面截图（手机框架模拟）
使用 Pillow 绘制仿真手机界面，展示 7 个核心页面
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 手机屏幕尺寸 (iPhone 14 比例)
SCREEN_W, SCREEN_H = 390, 844
PHONE_FRAME = 30
OUTPUT_DIR = r'd:\java\1\screenshots\miniprogram'

# 颜色方案
COLORS = {
    'primary': '#07C160',      # 微信绿
    'primary_light': '#4CD964',
    'blue': '#409EFF',
    'blue_dark': '#003366',
    'bg': '#F5F6FA',
    'white': '#FFFFFF',
    'text': '#303133',
    'text_sec': '#606266',
    'text_light': '#909399',
    'success': '#67C23A',
    'warning': '#E6A23C',
    'danger': '#F56C6C',
    'border': '#E4E7ED',
}

def get_font(size, bold=False):
    """获取字体"""
    font_paths = [
        r'C:\Windows\Fonts\msyh.ttc',      # 微软雅黑
        r'C:\Windows\Fonts\msyhbd.ttc',    # 微软雅黑 Bold
        r'C:\Windows\Fonts\simhei.ttf',    # 黑体
        r'C:\Windows\Fonts\simsun.ttc',    # 宋体
    ]
    if bold:
        font_paths = [r'C:\Windows\Fonts\msyhbd.ttc'] + font_paths
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()

def draw_phone_frame(img):
    """绘制手机外框"""
    draw = ImageDraw.Draw(img)
    # 圆角手机框
    draw.rounded_rectangle(
        [PHONE_FRAME-8, PHONE_FRAME-8, SCREEN_W+PHONE_FRAME+8, SCREEN_H+PHONE_FRAME+8],
        radius=40, outline='#333333', width=3
    )
    # 屏幕区域
    draw.rounded_rectangle(
        [PHONE_FRAME, PHONE_FRAME, SCREEN_W+PHONE_FRAME, SCREEN_H+PHONE_FRAME],
        radius=32, fill='white'
    )
    # 顶部刘海
    draw.rounded_rectangle(
        [SCREEN_W//2-50+PHONE_FRAME, PHONE_FRAME-5, SCREEN_W//2+50+PHONE_FRAME, PHONE_FRAME+25],
        radius=10, fill='#333333'
    )
    # 底部指示条
    draw.rounded_rectangle(
        [SCREEN_W//2-60+PHONE_FRAME, SCREEN_H+PHONE_FRAME-12, SCREEN_W//2+60+PHONE_FRAME, SCREEN_H+PHONE_FRAME-5],
        radius=3, fill='#333333'
    )

def create_screen():
    """创建手机屏幕画布"""
    img = Image.new('RGB', (SCREEN_W + PHONE_FRAME*2, SCREEN_H + PHONE_FRAME*2), '#1a1a1a')
    draw_phone_frame(img)
    return img

def draw_status_bar(draw, y_start):
    """绘制状态栏"""
    # 时间
    font = get_font(16, bold=True)
    draw.text((SCREEN_W+PHONE_FRAME-70, y_start+5), '9:41', fill='white', font=font)
    # 信号/电量图标 (简化)
    draw.text((PHONE_FRAME+15, y_start+5), '●●●  5G  100%', fill='white', font=get_font(12))

def draw_nav_bar(draw, title, y_start, color='#07C160'):
    """绘制导航栏"""
    draw.rectangle([PHONE_FRAME, y_start, SCREEN_W+PHONE_FRAME, y_start+88], fill=color)
    font = get_font(18, bold=True)
    tw = draw.textlength(title, font=font)
    draw.text((PHONE_FRAME + (SCREEN_W-tw)/2, y_start+30), title, fill='white', font=font)
    return y_start + 88

def draw_tab_bar(draw, y_start, active_idx=0):
    """绘制底部TabBar"""
    icons = ['🏠', '📊', '📋', '👤']
    labels = ['首页', '成绩', '填报', '我的']
    tab_h = 70
    bar_y = y_start
    # 背景
    draw.rectangle([PHONE_FRAME, bar_y, SCREEN_W+PHONE_FRAME, bar_y+tab_h], fill='white')
    # 顶部分割线
    draw.line([PHONE_FRAME, bar_y, SCREEN_W+PHONE_FRAME, bar_y], fill=COLORS['border'], width=1)
    
    tab_w = SCREEN_W // 4
    for i in range(4):
        cx = PHONE_FRAME + tab_w*i + tab_w//2
        cy = bar_y + 25
        color = COLORS['primary'] if i == active_idx else COLORS['text_light']
        font = get_font(22)
        draw.text((cx-10, cy), icons[i], fill=color, font=font)
        font_sm = get_font(10)
        label_w = draw.textlength(labels[i], font=font_sm)
        draw.text((cx-label_w//2, cy+28), labels[i], fill=color, font=font_sm)

def draw_card(draw, x, y, w, h, color='white'):
    """绘制卡片"""
    draw.rounded_rectangle([x, y, x+w, y+h], radius=12, fill=color,
                          outline=COLORS['border'], width=1)

def draw_text(draw, text, x, y, size=14, color='#303133', bold=False):
    """绘制文字"""
    font = get_font(size, bold=bold)
    draw.text((x, y), text, fill=color, font=font)

# ==============================================
# 页面1: 登录页
# ==============================================
def gen_login():
    img = create_screen()
    draw = ImageDraw.Draw(img)
    
    # 背景渐变
    for y in range(SCREEN_H):
        t = y / SCREEN_H
        r = int(7 + (240-7)*t)
        g = int(193 + (246-193)*t)
        b = int(96 + (250-96)*t)
        draw.line([PHONE_FRAME, PHONE_FRAME+y, SCREEN_W+PHONE_FRAME, PHONE_FRAME+y], fill=(r,g,b))
    
    draw_status_bar(draw, PHONE_FRAME)
    
    # Logo 区
    cx = SCREEN_W//2 + PHONE_FRAME
    # Logo 圆
    draw.ellipse([cx-50, 120, cx+50, 220], fill='white')
    font = get_font(36)
    draw.text((cx-18, 140), '📚', fill='#409EFF', font=font)
    
    draw_text(draw, '第二课堂成绩管理', cx-85, 240, size=22, color='white', bold=True)
    draw_text(draw, 'WeChat 小程序 · 学生端', cx-70, 275, size=13, color='#E6F9EE')
    
    # 登录卡片
    card_x, card_y, card_w, card_h = PHONE_FRAME+30, 310, SCREEN_W-60, 300
    draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], radius=20, fill='white')
    
    # 学号输入框
    draw_text(draw, '绑定学号（可选）', card_x+20, card_y+20, size=12, color='#909399')
    draw.rounded_rectangle([card_x+15, card_y+45, card_x+card_w-15, card_y+90], radius=10, fill='#f7f8fa')
    draw_text(draw, '👤', card_x+25, card_y+55, size=16)
    draw_text(draw, '请输入学号，如 2023101203', card_x+55, card_y+55, size=14, color='#c0c4cc')
    
    # 微信登录按钮
    btn_y = card_y+115
    draw.rounded_rectangle([card_x+15, btn_y, card_x+card_w-15, btn_y+50], radius=25, fill='#07C160')
    draw_text(draw, '🟢', card_x+card_w//2-55, btn_y+12, size=16)
    draw_text(draw, '微信一键登录', card_x+card_w//2-25, btn_y+15, size=16, color='white', bold=True)
    
    # 分隔线
    mid_y = btn_y + 80
    draw.line([card_x+20, mid_y+8, card_x+card_w//2-30, mid_y+8], fill='#e4e7ed', width=1)
    draw_text(draw, '其他方式', card_x+card_w//2-20, mid_y, size=11, color='#909399')
    draw.line([card_x+card_w//2+20, mid_y+8, card_x+card_w-20, mid_y+8], fill='#e4e7ed', width=1)
    
    # 账号密码登录
    btn2_y = mid_y + 25
    draw.rounded_rectangle([card_x+15, btn2_y, card_x+card_w-15, btn2_y+45], radius=22, fill='white', outline='#dcdfe6', width=2)
    draw_text(draw, '账号密码登录', card_x+card_w//2-40, btn2_y+13, size=15, color='#606266')
    
    # 底部
    draw_text(draw, '© 2024 第二课堂成绩管理系统', PHONE_FRAME+80, SCREEN_H+PHONE_FRAME-50, size=11, color='#606266')
    draw_text(draw, '登录即代表同意《用户协议》和《隐私政策》', PHONE_FRAME+55, SCREEN_H+PHONE_FRAME-30, size=10, color='#909399')
    
    img.save(f'{OUTPUT_DIR}/01_login.png', quality=95)
    print('✅ 登录页截图已生成')

# ==============================================
# 页面2: 首页仪表盘
# ==============================================
def gen_home():
    img = create_screen()
    draw = ImageDraw.Draw(img)
    
    # 背景
    draw.rectangle([PHONE_FRAME, PHONE_FRAME, SCREEN_W+PHONE_FRAME, SCREEN_H+PHONE_FRAME], fill='#F5F6FA')
    
    # 顶部导航 (蓝色渐变)
    nav_y = PHONE_FRAME
    for y in range(100):
        t = y / 100
        r = int(74 + (64-74)*t)
        g = int(158 + (158-158)*t)
        b = int(255 + (255-255)*t)
        draw.line([PHONE_FRAME, nav_y+y, SCREEN_W+PHONE_FRAME, nav_y+y], fill=(74,158,255))
    
    draw_status_bar(draw, PHONE_FRAME)
    draw_text(draw, '首页', PHONE_FRAME+SCREEN_W//2-25, PHONE_FRAME+30, size=18, color='white', bold=True)
    
    # 用户信息
    draw_text(draw, 'Hi, 刘备 👋', PHONE_FRAME+20, PHONE_FRAME+95, size=16, color='white', bold=True)
    draw_text(draw, '学号: 20231012023 · 计算机2班', PHONE_FRAME+20, PHONE_FRAME+118, size=12, color='#E6F9EE')
    
    # 总积分卡片
    card_x, card_y = PHONE_FRAME+15, PHONE_FRAME+150
    card_w, card_h = SCREEN_W-30, 140
    draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], radius=16, fill='white',
                          outline='#409EFF', width=2)
    
    draw_text(draw, '总积分', card_x+20, card_y+20, size=12, color='#909399')
    draw_text(draw, '71.4', card_x+20, card_y+45, size=40, color='#409EFF', bold=True)
    draw_text(draw, '分', card_x+95, card_y+60, size=16, color='#409EFF')
    draw_text(draw, '↑ 本月+15.0', card_x+20, card_y+95, size=11, color='#67C23A')
    draw_text(draw, '上次更新: 2026-06-01', card_x+card_w-110, card_y+95, size=10, color='#c0c4cc')
    
    # 快捷入口
    icons_data = [
        ('📝', '填报成绩', '#409EFF'),
        ('🏆', '赛事列表', '#67C23A'),
        ('📈', '学习计划', '#E6A23C'),
        ('📊', '成绩分析', '#F56C6C'),
    ]
    grid_y = card_y + card_h + 15
    for i, (icon, label, color) in enumerate(icons_data):
        gx = card_x + i*(card_w//4)
        # 图标圆
        cx, cy = gx + (card_w//4)//2, grid_y + 30
        draw.ellipse([cx-22, cy-22, cx+22, cy+22], fill=color+'22')
        draw_text(draw, icon, cx-14, cy-16, size=22)
        draw_text(draw, label, cx-28, cy+30, size=11, color='#303133')
    
    # 最近成绩
    recent_y = grid_y + 70
    draw_text(draw, '📋 最近成绩', PHONE_FRAME+20, recent_y, size=14, color='#303133', bold=True)
    draw.textlength('更多 ›', font=get_font(12))
    draw_text(draw, '更多 ›', PHONE_FRAME+SCREEN_W-55, recent_y, size=12, color='#909399')
    
    # 成绩卡片列表
    scores = [
        ('ACM国际大学生程序设计竞赛', '赛项: ACM程序设计赛项', '国家级-特等奖', '+10.0分', '#F56C6C'),
        ('全国英语四级考试(CET-4)', '英语四级笔试赛项', '优异', '+10.0分', '#409EFF'),
        ('蓝桥杯软件类C++组', 'C++设计赛项', '省一等奖', '+5.0分', '#67C23A'),
    ]
    for i, (name, item, level, score, color) in enumerate(scores):
        sy = recent_y + 25 + i*68
        draw.rounded_rectangle([PHONE_FRAME+15, sy, PHONE_FRAME+SCREEN_W-15, sy+62], radius=10, fill='white')
        draw_text(draw, name[:15], PHONE_FRAME+25, sy+8, size=13, color='#303133', bold=True)
        draw_text(draw, item, PHONE_FRAME+25, sy+30, size=11, color='#909399')
        # 右侧
        draw.rounded_rectangle([PHONE_FRAME+SCREEN_W-90, sy+15, PHONE_FRAME+SCREEN_W-25, sy+35], radius=8, fill=color+'22')
        draw_text(draw, level[:4], PHONE_FRAME+SCREEN_W-83, sy+18, size=10, color=color)
        draw_text(draw, score, PHONE_FRAME+SCREEN_W-80, sy+38, size=14, color=color, bold=True)
    
    # TabBar
    draw_tab_bar(draw, SCREEN_H+PHONE_FRAME-70, active_idx=0)
    
    img.save(f'{OUTPUT_DIR}/02_home.png', quality=95)
    print('✅ 首页截图已生成')

# ==============================================
# 页面3: 我的成绩
# ==============================================
def gen_scores():
    img = create_screen()
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([PHONE_FRAME, PHONE_FRAME, SCREEN_W+PHONE_FRAME, SCREEN_H+PHONE_FRAME], fill='#F5F6FA')
    nav_y = draw_nav_bar(draw, '我的成绩', PHONE_FRAME)
    draw_status_bar(draw, PHONE_FRAME)
    
    # 总积分卡
    card_y = nav_y + 10
    draw.rounded_rectangle([PHONE_FRAME+15, card_y, PHONE_FRAME+SCREEN_W-15, card_y+100], radius=12, fill='white')
    draw_text(draw, '总积分', PHONE_FRAME+30, card_y+15, size=11, color='#909399')
    draw_text(draw, '71.4', PHONE_FRAME+30, card_y+35, size=32, color='#409EFF', bold=True)
    draw_text(draw, '分', PHONE_FRAME+100, card_y+45, size=14, color='#409EFF')
    draw_text(draw, '共8条成绩记录', PHONE_FRAME+SCREEN_W-110, card_y+60, size=11, color='#909399')
    
    # 筛选标签
    filter_y = card_y + 115
    tabs = ['全部', '待审核', '已通过', '已拒绝']
    for i, tab in enumerate(tabs):
        tx = PHONE_FRAME + 15 + i*88
        active = i == 0
        bg = '#409EFF' if active else '#f0f2f5'
        fg = 'white' if active else '#606266'
        draw.rounded_rectangle([tx, filter_y, tx+75, filter_y+30], radius=15, fill=bg)
        draw_text(draw, tab, tx+18, filter_y+8, size=12, color=fg, bold=active)
    
    # 成绩列表
    scores = [
        ('全国英语四级考试（CET-4）', '英语四级笔试赛项', '优异', 644, 10.0, '2026-06-01', 1),
        ('ACM国际大学生程序设计竞赛', 'ACM程序设计赛项', '国家级-特等奖', 95, 15.0, '2026-05-15', 1),
        ('蓝桥杯软件类C++组', 'C++设计赛项', '省一等奖', 88, 8.0, '2026-04-20', 1),
        ('全国大学生数学建模竞赛', '数学建模赛项', '市级二等奖', 80, 5.0, '2026-03-10', 0),
        ('中国大学生计算机设计大赛', 'Web应用赛项', '校级一等奖', 90, 6.0, '2026-02-28', 1),
    ]
    status_map = {0: ('待审核', '#E6A23C'), 1: ('已通过', '#67C23A'), 2: ('已拒绝', '#F56C6C')}
    
    list_y = filter_y + 50
    for i, (event, item, level, raw, score, date, status) in enumerate(scores):
        sy = list_y + i*95
        draw.rounded_rectangle([PHONE_FRAME+15, sy, PHONE_FRAME+SCREEN_W-15, sy+88], radius=10, fill='white')
        
        # 左侧色块
        draw.rounded_rectangle([PHONE_FRAME+15, sy, PHONE_FRAME+20, sy+88], radius=3, fill='#409EFF')
        
        draw_text(draw, event[:18], PHONE_FRAME+30, sy+8, size=13, color='#303133', bold=True)
        draw_text(draw, f'赛项: {item}  |  级别: {level}', PHONE_FRAME+30, sy+32, size=11, color='#909399')
        draw_text(draw, f'原始分: {raw}  |  日期: {date}', PHONE_FRAME+30, sy+52, size=10, color='#c0c4cc')
        
        # 右侧分数和状态
        stext, scolor = status_map[status]
        draw_text(draw, f'+{score}', PHONE_FRAME+SCREEN_W-65, sy+15, size=18, color='#409EFF', bold=True)
        draw.rounded_rectangle([PHONE_FRAME+SCREEN_W-80, sy+50, PHONE_FRAME+SCREEN_W-25, sy+70], radius=8, fill=scolor+'22')
        draw_text(draw, stext, PHONE_FRAME+SCREEN_W-73, sy+54, size=10, color=scolor)
    
    draw_tab_bar(draw, SCREEN_H+PHONE_FRAME-70, active_idx=1)
    
    img.save(f'{OUTPUT_DIR}/03_scores.png', quality=95)
    print('✅ 我的成绩截图已生成')

# ==============================================
# 页面4: 成绩填报
# ==============================================
def gen_submit():
    img = create_screen()
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([PHONE_FRAME, PHONE_FRAME, SCREEN_W+PHONE_FRAME, SCREEN_H+PHONE_FRAME], fill='#F5F6FA')
    nav_y = draw_nav_bar(draw, '成绩填报', PHONE_FRAME)
    draw_status_bar(draw, PHONE_FRAME)
    
    form_y = nav_y + 15
    form_h = 480
    draw.rounded_rectangle([PHONE_FRAME+15, form_y, PHONE_FRAME+SCREEN_W-15, form_y+form_h], radius=12, fill='white')
    
    # 赛事选择
    row_y = form_y + 20
    draw_text(draw, '赛事名称', PHONE_FRAME+30, row_y, size=12, color='#606266')
    draw_text(draw, 'ACM国际大学生程序设计竞赛', PHONE_FRAME+30, row_y+20, size=14, color='#303133', bold=True)
    draw_text(draw, '▼', PHONE_FRAME+SCREEN_W-40, row_y+15, size=14, color='#909399')
    draw.line([PHONE_FRAME+30, row_y+45, PHONE_FRAME+SCREEN_W-30, row_y+45], fill='#ebeef5', width=1)
    
    # 赛项选择
    row_y += 60
    draw_text(draw, '赛项名称', PHONE_FRAME+30, row_y, size=12, color='#606266')
    draw_text(draw, 'ACM程序设计赛项', PHONE_FRAME+30, row_y+20, size=14, color='#303133', bold=True)
    draw_text(draw, '▼', PHONE_FRAME+SCREEN_W-40, row_y+15, size=14, color='#909399')
    draw.line([PHONE_FRAME+30, row_y+45, PHONE_FRAME+SCREEN_W-30, row_y+45], fill='#ebeef5', width=1)
    
    # 级别选择
    row_y += 60
    draw_text(draw, '获奖级别', PHONE_FRAME+30, row_y, size=12, color='#606266')
    # 级别标签
    levels = ['国家级-特等奖', '国家级-一等奖', '国家级-二等奖', '省级一等奖']
    for i, lv in enumerate(levels):
        lx = PHONE_FRAME + 30 + (i%2)*175
        ly = row_y + 20 + (i//2)*28
        active = i == 0
        bg = '#409EFF' if active else '#f0f2f5'
        fg = 'white' if active else '#606266'
        draw.rounded_rectangle([lx, ly, lx+160, ly+24], radius=12, fill=bg)
        draw_text(draw, lv, lx+10, ly+5, size=10, color=fg)
    
    # 日期选择
    row_y += 90
    draw_text(draw, '获奖日期', PHONE_FRAME+30, row_y, size=12, color='#606266')
    draw_text(draw, '📅  2026-05-15', PHONE_FRAME+30, row_y+20, size=14, color='#303133')
    draw.line([PHONE_FRAME+30, row_y+45, PHONE_FRAME+SCREEN_W-30, row_y+45], fill='#ebeef5', width=1)
    
    # 分数
    row_y += 60
    draw_text(draw, '获奖分数', PHONE_FRAME+30, row_y, size=12, color='#606266')
    draw_text(draw, '95', PHONE_FRAME+30, row_y+20, size=14, color='#303133')
    draw_text(draw, '▼', PHONE_FRAME+SCREEN_W-40, row_y+15, size=14, color='#909399')
    draw.line([PHONE_FRAME+30, row_y+45, PHONE_FRAME+SCREEN_W-30, row_y+45], fill='#ebeef5', width=1)
    
    # 证书上传
    row_y += 60
    draw_text(draw, '证书上传', PHONE_FRAME+30, row_y, size=12, color='#606266')
    # 上传框
    draw.rounded_rectangle([PHONE_FRAME+30, row_y+15, PHONE_FRAME+120, row_y+55], radius=8, fill='#f7f8fa', outline='#dcdfe6', width=1)
    draw_text(draw, '📎', PHONE_FRAME+70, row_y+20, size=16)
    draw_text(draw, '点击上传证书', PHONE_FRAME+35, row_y+40, size=10, color='#909399')
    
    # 提交按钮
    btn_y = form_y + form_h + 20
    draw.rounded_rectangle([PHONE_FRAME+15, btn_y, PHONE_FRAME+SCREEN_W-15, btn_y+50], radius=25, fill='#07C160')
    draw_text(draw, '提  交', PHONE_FRAME+SCREEN_W//2-15, btn_y+12, size=17, color='white', bold=True)
    
    draw_tab_bar(draw, SCREEN_H+PHONE_FRAME-70, active_idx=2)
    
    img.save(f'{OUTPUT_DIR}/04_submit.png', quality=95)
    print('✅ 成绩填报截图已生成')

# ==============================================
# 页面5: 赛事列表
# ==============================================
def gen_events():
    img = create_screen()
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([PHONE_FRAME, PHONE_FRAME, SCREEN_W+PHONE_FRAME, SCREEN_H+PHONE_FRAME], fill='#F5F6FA')
    nav_y = draw_nav_bar(draw, '赛事列表', PHONE_FRAME)
    draw_status_bar(draw, PHONE_FRAME)
    
    # 搜索框
    search_y = nav_y + 12
    draw.rounded_rectangle([PHONE_FRAME+15, search_y, PHONE_FRAME+SCREEN_W-15, search_y+40], radius=20, fill='white',
                          outline='#e4e7ed', width=1)
    draw_text(draw, '🔍', PHONE_FRAME+25, search_y+10, size=14)
    draw_text(draw, '搜索赛事名称...', PHONE_FRAME+50, search_y+12, size=13, color='#c0c4cc')
    
    # 分类
    cat_y = search_y + 55
    categories = ['全部', '程序设计', '数学建模', '英语考试', '物理竞赛', '其他']
    for i, cat in enumerate(categories):
        cx = PHONE_FRAME + 25 + i*62
        active = i == 0
        color = '#409EFF' if active else '#606266'
        if active:
            draw.textlength(cat, font=get_font(11))
            draw.line([cx, cat_y+20, cx+45, cat_y+20], fill=color, width=2)
        draw_text(draw, cat, cx, cat_y, size=11, color=color, bold=active)
    
    # 赛事列表
    events = [
        ('ACM国际大学生程序设计竞赛', 'ACM/ICPC基金会', '国家级', '2026-09-01', 1),
        ('全国大学生数学建模竞赛', '教育部高教司', '国家级', '2026-09-15', 2),
        ('蓝桥杯软件类C++组', '蓝桥杯大赛组委会', '省级', '2026-10-01', 3),
        ('全国英语四级考试(CET-4)', '教育部考试中心', '国家级', '2026-06-15', 1),
        ('中国大学生计算机设计大赛', '教育部计算机教指委', '校级', '2026-07-01', 2),
    ]
    level_colors = ['#F56C6C', '#409EFF', '#E6A23C', '#67C23A', '#909399']
    
    list_y = cat_y + 40
    for i, (name, host, level, date, idx) in enumerate(events):
        ey = list_y + i*95
        draw.rounded_rectangle([PHONE_FRAME+15, ey, PHONE_FRAME+SCREEN_W-15, ey+88], radius=10, fill='white')
        
        # 左侧标签
        tag_color = level_colors[idx-1]
        draw.rounded_rectangle([PHONE_FRAME+15, ey, PHONE_FRAME+95, ey+88], radius=10, fill=tag_color+'22')
        draw_text(draw, level, PHONE_FRAME+25, ey+35, size=11, color=tag_color, bold=True)
        
        draw_text(draw, name, PHONE_FRAME+105, ey+10, size=13, color='#303133', bold=True)
        draw_text(draw, f'主办: {host}', PHONE_FRAME+105, ey+35, size=11, color='#909399')
        draw_text(draw, f'📅 报名截止: {date}', PHONE_FRAME+105, ey+55, size=11, color='#c0c4cc')
        
        # 立即报名按钮
        btn_x = PHONE_FRAME + SCREEN_W - 90
        draw.rounded_rectangle([btn_x, ey+30, btn_x+65, ey+50], radius=10, fill='#409EFF22')
        draw_text(draw, '立即报名', btn_x+8, ey+33, size=10, color='#409EFF')
    
    draw_tab_bar(draw, SCREEN_H+PHONE_FRAME-70, active_idx=2)
    
    img.save(f'{OUTPUT_DIR}/05_events.png', quality=95)
    print('✅ 赛事列表截图已生成')

# ==============================================
# 页面6: 学习计划
# ==============================================
def gen_plan():
    img = create_screen()
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([PHONE_FRAME, PHONE_FRAME, SCREEN_W+PHONE_FRAME, SCREEN_H+PHONE_FRAME], fill='#F5F6FA')
    nav_y = draw_nav_bar(draw, '学习计划', PHONE_FRAME)
    draw_status_bar(draw, PHONE_FRAME)
    
    # 学分进度卡
    card_y = nav_y + 15
    draw.rounded_rectangle([PHONE_FRAME+15, card_y, PHONE_FRAME+SCREEN_W-15, card_y+180], radius=12, fill='white')
    
    draw_text(draw, '学分进度', PHONE_FRAME+30, card_y+15, size=13, color='#303133', bold=True)
    draw_text(draw, '当前学期', PHONE_FRAME+SCREEN_W-80, card_y+15, size=11, color='#909399')
    
    # 大环
    cx, cy = PHONE_FRAME+80, card_y+100
    draw.ellipse([cx-50, cy-50, cx+50, cy+50], outline='#ebeef5', width=10)
    draw.ellipse([cx-45, cy-45, cx+45, cy+45], outline='#409EFF', width=10)
    draw_text(draw, '14.3', cx-25, cy-10, size=24, color='#409EFF', bold=True)
    draw_text(draw, '/ 30 学分', cx-20, cy+18, size=10, color='#909399')
    
    # 右侧统计
    rx = PHONE_FRAME + 160
    stats = [
        ('已获学分', '14.3', '#409EFF'),
        ('目标学分', '30.0', '#606266'),
        ('完成进度', '47.7%', '#67C23A'),
        ('差距学分', '15.7', '#E6A23C'),
    ]
    for i, (label, val, color) in enumerate(stats):
        ry = card_y + 40 + i*30
        draw_text(draw, label, rx, ry, size=11, color='#909399')
        draw_text(draw, val, rx+70, ry-2, size=14, color=color, bold=True)
    
    # 赛事分类推荐
    rec_y = card_y + 200
    draw_text(draw, '📌 赛事分类推荐', PHONE_FRAME+20, rec_y, size=13, color='#303133', bold=True)
    
    categories = [
        ('程序设计类', '推荐5项赛事', '#409EFF', 'ACM, 蓝桥杯, 华为杯'),
        ('学科竞赛类', '推荐3项赛事', '#67C23A', '数模, 挑战杯, 互联网+'),
        ('技能认证类', '推荐4项赛事', '#E6A23C', 'CET, 计算机二级, 软考'),
    ]
    for i, (cat, desc, color, detail) in enumerate(categories):
        ry = rec_y + 25 + i*65
        draw.rounded_rectangle([PHONE_FRAME+15, ry, PHONE_FRAME+SCREEN_W-15, ry+58], radius=10, fill='white')
        draw.rounded_rectangle([PHONE_FRAME+15, ry, PHONE_FRAME+22, ry+58], radius=3, fill=color)
        draw_text(draw, cat, PHONE_FRAME+30, ry+10, size=13, color='#303133', bold=True)
        draw_text(draw, desc, PHONE_FRAME+30, ry+30, size=11, color='#909399')
        draw_text(draw, detail, PHONE_FRAME+SCREEN_W-130, ry+10, size=10, color='#c0c4cc')
    
    # 学分要求说明
    note_y = rec_y + 230
    draw.rounded_rectangle([PHONE_FRAME+15, note_y, PHONE_FRAME+SCREEN_W-15, note_y+75], radius=10, fill='#f0f9ff')
    draw_text(draw, '💡 学分要求', PHONE_FRAME+25, note_y+10, size=12, color='#409EFF', bold=True)
    draw_text(draw, '• 每学期至少获得 20 学分', PHONE_FRAME+25, note_y+30, size=11, color='#606266')
    draw_text(draw, '• 国家级赛事可获 10-20 学分', PHONE_FRAME+25, note_y+48, size=11, color='#606266')
    
    draw_tab_bar(draw, SCREEN_H+PHONE_FRAME-70, active_idx=1)
    
    img.save(f'{OUTPUT_DIR}/06_plan.png', quality=95)
    print('✅ 学习计划截图已生成')

# ==============================================
# 页面7: 个人中心
# ==============================================
def gen_profile():
    img = create_screen()
    draw = ImageDraw.Draw(img)
    
    # 顶部背景
    for y in range(180):
        t = y / 180
        r = int(7 + (245-7)*t)
        g = int(193 + (245-193)*t)
        b = int(96 + (245-96)*t)
        draw.line([PHONE_FRAME, PHONE_FRAME+y, SCREEN_W+PHONE_FRAME, PHONE_FRAME+y], fill=(r,g,b))
    
    draw_status_bar(draw, PHONE_FRAME)
    draw_text(draw, '个人中心', PHONE_FRAME+SCREEN_W//2-28, PHONE_FRAME+30, size=18, color='white', bold=True)
    
    # 头像
    cx = SCREEN_W//2 + PHONE_FRAME
    draw.ellipse([cx-35, 100, cx+35, 170], fill='white')
    draw.ellipse([cx-30, 105, cx+30, 165], fill='#409EFF')
    draw_text(draw, '👤', cx-15, 115, size=26)
    
    draw_text(draw, '刘备', cx-20, 180, size=18, color='white', bold=True)
    draw_text(draw, '20231012023 · 计算机科学与技术', cx-85, 205, size=11, color='#E6F9EE')
    
    # 信息卡片
    card_y = 240
    draw.rounded_rectangle([PHONE_FRAME+15, card_y, PHONE_FRAME+SCREEN_W-15, card_y+120], radius=12, fill='white')
    
    info_items = [
        ('学号', '20231012023', '👤'),
        ('姓名', '刘备', '📝'),
        ('班级', '计算机科学与技术2班', '🏫'),
        ('专业', '计算机科学与技术', '💻'),
    ]
    for i, (label, val, icon) in enumerate(info_items):
        iy = card_y + 10 + i*27
        draw_text(draw, icon, PHONE_FRAME+30, iy, size=14)
        draw_text(draw, label, PHONE_FRAME+55, iy+2, size=12, color='#909399')
        draw_text(draw, val, PHONE_FRAME+130, iy+2, size=12, color='#303133')
    
    # 功能列表
    func_y = card_y + 135
    functions = [
        ('🔔', '消息通知', '未读3条', '#F56C6C'),
        ('📊', '成绩报告', '', '#409EFF'),
        ('🏆', '获奖证书', '', '#67C23A'),
        ('⚙️', '设置', '', '#606266'),
        ('❓', '帮助与反馈', '', '#606266'),
        ('ℹ️', '关于我们', 'V1.0.0', '#909399'),
    ]
    for i, (icon, name, badge, color) in enumerate(functions):
        fy = func_y + i*56
        draw.rounded_rectangle([PHONE_FRAME+15, fy, PHONE_FRAME+SCREEN_W-15, fy+48], radius=10, fill='white')
        draw_text(draw, icon, PHONE_FRAME+30, fy+15, size=16)
        draw_text(draw, name, PHONE_FRAME+60, fy+17, size=13, color='#303133')
        if badge:
            bx = PHONE_FRAME + SCREEN_W - 65
            draw.rounded_rectangle([bx, fy+12, bx+45, fy+28], radius=8, fill='#F56C6C')
            draw_text(draw, badge, bx+5, fy+15, size=10, color='white')
        else:
            draw_text(draw, '›', PHONE_FRAME+SCREEN_W-30, fy+15, size=16, color='#c0c4cc')
    
    # 退出登录
    exit_y = func_y + 6*56 + 15
    draw.rounded_rectangle([PHONE_FRAME+15, exit_y, PHONE_FRAME+SCREEN_W-15, exit_y+48], radius=10, fill='white')
    draw_text(draw, '🚪', PHONE_FRAME+30, exit_y+15, size=16)
    draw_text(draw, '退出登录', PHONE_FRAME+60, exit_y+17, size=13, color='#F56C6C', bold=True)
    
    draw_tab_bar(draw, SCREEN_H+PHONE_FRAME-70, active_idx=3)
    
    img.save(f'{OUTPUT_DIR}/07_profile.png', quality=95)
    print('✅ 个人中心截图已生成')

# ==============================================
# 生成所有截图
# ==============================================
if __name__ == '__main__':
    print('🖼️ 开始生成微信小程序学生端截图...')
    print('='*50)
    gen_login()
    gen_home()
    gen_scores()
    gen_submit()
    gen_events()
    gen_plan()
    gen_profile()
    print('='*50)
    print(f'✅ 全部7张截图已保存到: {OUTPUT_DIR}')
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f'   {f} ({size/1024:.1f} KB)')
