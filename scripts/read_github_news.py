"""
QClaw 本地读取脚本 - 从 GitHub 仓库获取新闻
"""
import requests
import json
from datetime import datetime

# 修正 GitHub 用户名和分支
GITHUB_USER = "DavidChen80"
REPO = "news-aggregator"
BRANCH = "master"  # 默认分支

def fetch_latest_news():
    """从 GitHub 仓库获取最新新闻"""
    
    today = datetime.now().strftime('%Y%m%d')
    
    # 获取 Reuters 新闻（含 Bloomberg 多源）
    reuters_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO}/{BRANCH}/data/reuters_{today}.json"
    # 获取 Bloomberg 新闻
    bloomberg_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO}/{BRANCH}/data/bloomberg_{today}.json"
    
    all_news = []
    
    for url, source in [(reuters_url, "International"), (bloomberg_url, "Bloomberg")]:
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                news = resp.json()
                all_news.extend(news)
                print(f"Fetched {len(news)} articles from {source}")
        except Exception as e:
            print(f"Error fetching {source}: {e}")
    
    # 按时间排序
    all_news.sort(key=lambda x: x.get("published", ""), reverse=True)
    
    return all_news

def filter_commodity_news(news_list):
    """过滤期货相关新闻"""
    keywords = [
        "gold", "silver", "oil", "crude", "copper", "nickel", "tin",
        "commodity", "futures", "metal", "energy", "agriculture",
        "pork", "hog", "livestock", "农产品", "大宗商品",
        "沪金", "沪银", "原油", "铜", "镍", "锡", "期货", "生猪"
    ]
    
    filtered = []
    for news in news_list:
        text = f"{news.get('title', '')} {news.get('summary', '')}".lower()
        if any(kw in text for kw in keywords):
            filtered.append(news)
    
    return filtered

def format_for_push(news_list, max_count=8):
    """格式化为微信推送文本"""
    if not news_list:
        return "📰 暂无期货相关新闻"
    
    lines = [f"📰 国际财经 ({datetime.now().strftime('%H:%M')})", ""]
    
    for item in news_list[:max_count]:
        source_emoji = "🇺🇸" if item['source'] == 'International' else "📊"
        title = item.get('title', '')[:60]
        lines.append(f"{source_emoji} {title}")
        summary = item.get('summary', '')
        if summary:
            # 去掉 HTML 标签
            clean = ''.join(c for c in summary if c.isprintable())[:80].strip()
            if clean:
                lines.append(f"   {clean}...")
        lines.append("")
    
    lines.append(f"共 {len(news_list)} 条相关 | 原始 {len(news_list)} 条")
    
    return "\n".join(lines)

if __name__ == "__main__":
    news = fetch_latest_news()
    commodity_news = filter_commodity_news(news)
    
    print(f"\n=== 今日共 {len(news)} 条新闻，期货相关 {len(commodity_news)} 条 ===\n")
    
    output = format_for_push(commodity_news)
    print(output)