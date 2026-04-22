# 手动推送指引

由于 GitHub 已禁用密码认证，请按以下步骤操作：

## 方案一：浏览器登录（推荐）

在 PowerShell 中执行：

```powershell
cd C:\Users\Administrator\.qclaw\workspace\news-aggregator

# 初始化 git
git init

# 添加文件
git add .
git commit -m "Initial commit: news aggregator workflow"

# 在浏览器中创建仓库后关联推送
# 访问: https://github.com/new
# 仓库名: news-aggregator
# 选 Public，然后点击 Create repository

# 关联远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/davy80/news-aggregator.git

# 推送（会弹出窗口让你登录）
git push -u origin main
```

## 方案二：使用 Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成后复制 token

然后：

```powershell
cd C:\Users\Administrator\.qclaw\workspace\news-aggregator

# 使用 token 推送（把 YOUR_TOKEN 替换为实际 token）
$token = "YOUR_TOKEN"
git remote add origin https://$token@github.com/davy80/news-aggregator.git
git push -u origin main
```

## 方案三：使用 GitHub CLI 登录

```powershell
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")

# 登录（会打开浏览器）
gh auth login

# 然后创建仓库
gh repo create news-aggregator --public --source=. --push
```

## 验证

推送成功后，访问：
https://github.com/davy80/news-aggregator

应该能看到：
- `.github/workflows/fetch-news.yml` - 工作流配置
- `scripts/` - 抓取脚本
- `data/` - 数据目录

## 启动 Actions

1. 进入仓库页面
2. 点击 Actions 标签
3. 找到 "Fetch Financial News" 工作流
4. 点击 "Enable workflow"
5. 点击 "Run workflow" 手动测试一次

完成后，每15分钟会自动抓取新闻到 `data/` 目录。
