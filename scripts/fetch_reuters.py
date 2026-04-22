import feedparser
import json
import os
from datetime import datetime
from hashlib import md5

# 多源国际财经 RSS（Bloomberg + 备用源）
RSS_URLS = [
    # Bloomberg 多主题
    "https://feeds.bloomberg.com/business/news.rss",
    "https://feeds.bloomberg.com/markets/news.rss",
    "https://feeds.bloomberg.com/technology/news.rss",
    "https://feeds.bloomberg.com/politics/news.rss",
    "https://feeds.bloomberg.com/energy/news.rss",
    # 备用：Business Insider
    "https://feeds.businessinsider.com/homepage",
]

def fetch_news():
    all_news = []
    
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            count = 0
            for entry in feed.entries:
                news_item = {
                    "id": md5(entry.link.encode()).hexdigest()[:12],
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.link,
                    "published": entry.get("published", ""),
                    "source": "International",
                    "fetched_at": datetime.utcnow().isoformat()
                }
                all_news.append(news_item)
                count += 1
            print(f"  {url.split('/')[2]}: {count} articles")
        except Exception as e:
            print(f"  Error fetching {url}: {e}")
    
    # 去重（按 ID）
    seen = set()
    unique_news = []
    for item in all_news:
        if item["id"] not in seen:
            seen.add(item["id"])
            unique_news.append(item)
    
    # 保存
    os.makedirs("data", exist_ok=True)
    filename = f"data/reuters_{datetime.utcnow().strftime('%Y%m%d')}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(unique_news, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(unique_news)} articles to {filename}")

if __name__ == "__main__":
    fetch_news()