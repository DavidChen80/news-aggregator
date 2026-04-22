# News Aggregator

GitHub Actions 定时抓取 Reuters/Bloomberg 财经新闻，供 QClaw 本地读取。

## 架构

```
GitHub Actions (每15分钟) → GitHub 仓库 → QClaw 本地读取
```

## 本地使用

```python
from scripts.read_github_news import fetch_latest_news, filter_commodity_news

# 获取新闻
news = fetch_latest_news()

# 过滤期货相关
commodity_news = filter_commodity_news(news)
```

## 定时配置

- 抓取频率：每 15 分钟（UTC）
- 存储格式：JSON，按日期分文件
- 保留策略：Git 历史自动保留
