import feedparser
import json
import requests
import re
from html import unescape

def translate(text):
    if not text: return ""
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=de&tl=en&dt=t&q={requests.utils.quote(text)}"
        res = requests.get(url).json()
        return "".join([sentence[0] for sentence in res[0]])
    except:
        return text

def scrape():
    feed = feedparser.parse("https://www.anime2you.de/feed/")
    news_data = []

    for entry in feed.entries[:10]:
        print(f"Processing: {entry.title}")
      
        img_match = re.search(r'<img [^>]*src="([^"]+)"', entry.description)
        img_url = img_match.group(1) if img_match else ""
        
        clean_summary = re.sub('<[^<]+?>', '', entry.description).split('Der Beitrag')[0]
        
        news_data.append({
            "title": translate(entry.title),
            "link": entry.link,
            "date": entry.published,
            "image": img_url,
            "content": translate(clean_summary)
        })

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape()
