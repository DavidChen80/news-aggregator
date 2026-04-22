"""
QClaw 本地读取脚本 - 从 GitHub 仓库获取新闻
"""
import requests
import json
from datetime import datetime

# 修改为你的 GitHub 用户名
GITHUB_USER = "davy80"
REPO = "news-aggregator"

def fetch_latest_news():
    """从 GitHub 仓库获取最新新闻"""
    
    today = datetime.now().strftime('%Y%m%d')
    
    # 获取 Reuters 新闻
    reuters_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO}/main/data/reuters_{today}.json"
    bloomberg_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO}/main/data/bloomberg_{today}.json"
    
    all_news = []
    
    for url, source in [(reuters_url, "Reuters"), (bloomberg_url, "Bloomberg")]:
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
        "沪金", "沪银", "原油", "铜", "镍", "锡", "期货", "生猪"
    ]
    
    filtered = []
    for news in news_list:
        text = f"{news.get('title', '')} {news.get('summary', '')}".lower()
        if any(kw in text for kw in keywords):
            filtered.append(news)
    
    return filtered

def format_for_push(news_list, max_count=5):
    """格式化为微信推送文本"""
    if not news_list:
        return "暂无相关新闻"
    
    lines = [f"📰 国际财经新闻 ({datetime.now().strftime('%m-%d %H:%M')})", ""]
    
    for item in news_list[:max_count]:
        source_emoji = "🇺🇸" if item['source'] == 'Reuters' else "📊"
        lines.append(f"{source_emoji} [{item['source']}] {item['title']}")
        summary = item.get('summary', '')
        if summary:
            lines.append(f"   {summary[:80]}...")
        lines.append("")
    
    return "\n".join(lines)

if __name__ == "__main__":
    news = fetch_latest_news()
    commodity_news = filter_commodity_news(news)
    
    print(f"\n=== 今日共 {len(news)} 条新闻，期货相关 {len(commodity_news)} 条 ===\n")
    
    # 输出格式化结果
    output = format_for_push(commodity_news)
    print(output)
