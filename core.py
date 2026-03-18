import feedparser
import json
import requests
from bs4 import BeautifulSoup

def translate(text):
    if not text or len(text) < 3: return text
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={requests.utils.quote(text)}"
        res = requests.get(url, timeout=5).json()
        return "".join([s[0] for s in res[0]])
    except:
        return text

def scrape():
    feed = feedparser.parse("https://www.animenewsnetwork.com/newsfeed/")
    news_data = []

    for entry in feed.entries[:10]:
        print(f"Syncing: {entry.title}")
        
        en_title = translate(entry.title)

        summary = entry.summary.split('<')[0] if '<' in entry.summary else entry.summary
        en_summary = translate(summary)

        news_data.append({
            "title": en_title,
            "link": entry.link,
            "date": entry.published,
            "summary": en_summary,
            "id": entry.id
        })

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape()
