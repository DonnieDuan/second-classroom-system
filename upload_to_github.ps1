# ============================================================
#  学生第二课堂成绩管理系统 - 上传到 GitHub 的一键脚本
#  适用环境：Windows PowerShell
#  使用方法：
#    1. 先在 GitHub 网站手动创建一个空仓库（不选 README/.gitignore）
#    2. 把下面的 YOUR_GITHUB_USERNAME 改成你自己的 GitHub 用户名
#    3. 把 YOUR_REPO_NAME 改成你的仓库名（例如：second-classroom-system）
#    4. 右键本文件 → 使用 PowerShell 运行；或复制到 PowerShell 中执行
# ============================================================

# ------------------- 请修改这两个配置 -------------------
$GITHUB_USERNAME = "YOUR_GITHUB_USERNAME"     # 你的 GitHub 用户名
$REPO_NAME      = "second-classroom-system"   # 你的仓库名
# -------------------------------------------------------

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   学生第二课堂系统 - GitHub 上传脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "目标仓库: https://github.com/$GITHUB_USERNAME/$REPO_NAME" -ForegroundColor Yellow
Write-Host ""

# 1. 初始化 Git 仓库
Write-Host "[1/5] 初始化 Git 仓库..." -ForegroundColor Green
git init
git branch -M main

# 2. 配置用户信息（如果没有全局配置的话）
Write-Host "[2/5] 检查 Git 用户信息..." -ForegroundColor Green
$userName  = git config user.name  2>$null
$userEmail = git config user.email 2>$null
if ([string]::IsNullOrWhiteSpace($userName)) {
    git config user.name  "$GITHUB_USERNAME"
    Write-Host "   已设置 Git 用户名: $GITHUB_USERNAME"
} else {
    Write-Host "   当前用户名: $userName"
}
if ([string]::IsNullOrWhiteSpace($userEmail)) {
    git config user.email "$GITHUB_USERNAME@users.noreply.github.com"
    Write-Host "   已设置 Git 邮箱: $GITHUB_USERNAME@users.noreply.github.com"
} else {
    Write-Host "   当前邮箱: $userEmail"
}

# 3. 添加所有文件
Write-Host "[3/5] 添加项目文件（.gitignore 已自动排除 node_modules、target、报告等）..." -ForegroundColor Green
git add -A
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "   （无新增文件，使用最近一次提交）"
} else {
    $count = ($status -split "`r?`n").Count
    Write-Host "   本次将添加 $count 个文件变更"
}

# 4. 提交
Write-Host "[4/5] 提交代码到本地仓库..." -ForegroundColor Green
git commit -m "feat: 初始化学生第二课堂成绩管理系统

功能特性:
- 后端: Spring Boot 3 + MyBatis + MySQL, 完整 REST API
- 前端: Vue 3 + Element Plus + Vite (教师端成绩审核/统计/预警/机构管理)
- 移动端: 鸿蒙 ArkTS 原生应用 (学生端成绩填报/学习计划/积分统计)
- 自动化测试: pytest 接口测试 + Playwright UI 测试 (49+ 用例)
- CI/CD: GitHub Actions 自动化测试流水线 + HTML/XML 报告上传
"
if ($LASTEXITCODE -ne 0) {
    Write-Host "   （无变更需要提交，跳过）" -ForegroundColor Yellow
}

# 5. 添加远端并推送
Write-Host "[5/5] 关联远端仓库并推送到 GitHub..." -ForegroundColor Green
$remote = git remote get-url origin 2>$null
if ([string]::IsNullOrWhiteSpace($remote)) {
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    Write-Host "   已添加远端 origin: https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
} else {
    Write-Host "   已存在远端 origin: $remote" -ForegroundColor Yellow
    $answer = Read-Host "   是否覆盖远端地址为新仓库? (y/N，默认N)"
    if ($answer -eq 'y' -or $answer -eq 'Y') {
        git remote set-url origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
        Write-Host "   已覆盖远端地址"
    }
}

Write-Host ""
Write-Host "现在执行首次推送（main 分支）..." -ForegroundColor Yellow
Write-Host "  git push -u origin main"
Write-Host ""
Write-Host "如果出现 Username/Password 弹窗:" -ForegroundColor Magenta
Write-Host "  • Username: 输入你的 GitHub 用户名"
Write-Host "  • Password: 不要输入密码，而是输入 GitHub Token (PAT)" -ForegroundColor Red
Write-Host ""
Write-Host "如何获取 GitHub Token:" -ForegroundColor Magenta
Write-Host "  1. 打开 https://github.com/settings/tokens"
Write-Host "  2. Generate new token (classic)"
Write-Host "  3. 勾选 repo 权限，生成，复制，粘贴到密码提示处"
Write-Host ""

# 让用户确认后再 push
$go = Read-Host "现在执行 git push 吗? (Y/n)"
if ($go -ne 'n' -and $go -ne 'N') {
    git push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉  上传成功！" -ForegroundColor Green
        Write-Host "现在可访问: https://github.com/$GITHUB_USERNAME/$REPO_NAME" -ForegroundColor Cyan
        Write-Host "进入 Actions 页面可看自动化测试流水线运行结果" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "❌  推送失败，请根据上面的报错信息检查：" -ForegroundColor Red
        Write-Host "   - 仓库是否已在 GitHub 上创建"
        Write-Host "   - 用户名/仓库名是否正确"
        Write-Host "   - 你是否有该仓库的 push 权限"
        Write-Host "   - 认证方式：请用 Token(PAT) 而非账户密码"
    }
} else {
    Write-Host ""
    Write-Host "已跳过推送。稍后你可以手动执行:" -ForegroundColor Yellow
    Write-Host "   git push -u origin main"
}
