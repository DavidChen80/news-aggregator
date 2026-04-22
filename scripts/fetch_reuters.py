import feedparser
import json
import os
from datetime import datetime
from hashlib import md5

# 国际财经 RSS（兼容 GitHub Actions runner）
RSS_URLS = [
    # Reuters World News
    "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=reuters",
    "https://www.reutersagency.com/feed/?best-topics=tech&post_type=reuters",
    # CNBC International
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    # BBC Business
    "http://feeds.bbci.co.uk/news/business/rss.xml",
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
