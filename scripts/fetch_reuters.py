import feedparser
import json
import os
from datetime import datetime
from hashlib import md5
from deep_translator import GoogleTranslator

# 多源国际财经 RSS（Bloomberg + 备用源）
RSS_URLS = [
    # Bloomberg 多主题
    "https://feeds.bloomberg.com/business/news.rss",
    "https://feeds.bloomberg.com/markets/news.rss",
    "https://feeds.bloomberg.com/technology/news.rss",
    "https://feeds.bloomberg.com/politics/news.rss",
    "https://feeds.bloomberg.com/energy/news.rss",
]

def translate_to_chinese(text):
    """翻译到中文"""
    if not text or len(text) < 3:
        return text
    try:
        translator = GoogleTranslator(source='auto', target='zh-CN')
        return translator.translate(text[:450])
    except:
        return text

def fetch_news():
    all_news = []
    
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            count = 0
            for entry in feed.entries:
                # 翻译标题
                title_en = entry.get("title", "")
                title_cn = translate_to_chinese(title_en)
                
                news_item = {
                    "id": md5(entry.link.encode()).hexdigest()[:12],
                    "title": title_en,
                    "title_cn": title_cn,
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