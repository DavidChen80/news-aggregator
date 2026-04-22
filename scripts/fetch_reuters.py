import feedparser
import json
import os
from datetime import datetime
from hashlib import md5

# Reuters RSS 源（官方 feed.reuters.com）
RSS_URLS = [
    "https://feeds.reuters.com/reuters/businessNews",
    "https://feeds.reuters.com/reuters/technologyNews",
    "https://feeds.reuters.com/reuters/environment",
    "https://feeds.reuters.com/reuters/wealth",
]

def fetch_reuters():
    all_news = []
    
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                news_item = {
                    "id": md5(entry.link.encode()).hexdigest()[:12],
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.link,
                    "published": entry.get("published", ""),
                    "source": "Reuters",
                    "fetched_at": datetime.utcnow().isoformat()
                }
                all_news.append(news_item)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    
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
    
    print(f"Saved {len(unique_news)} Reuters articles to {filename}")

if __name__ == "__main__":
    fetch_reuters()
