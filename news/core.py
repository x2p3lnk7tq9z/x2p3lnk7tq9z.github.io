import feedparser
import json
import requests
from bs4 import BeautifulSoup
import os

def get_full_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_content = soup.find('div', class_='meat') or soup.find('div', class_='maincontent')
        if main_content:
            for junk in main_content.find_all(['script', 'style', 'aside', 'iframe']):
                junk.decompose()
            return str(main_content)
        return "Extraction failed."
    except:
        return "Source unreachable."

def scrape():
    feed = feedparser.parse("https://www.animenewsnetwork.com/newsfeed/")
    news_data = []

    for entry in feed.entries[:10]:
        print(f"Scraping: {entry.title}")
        full_html = get_full_content(entry.link)
        
        news_data.append({
            "title": entry.title,
            "link": entry.link,
            "date": entry.published,
            "content": full_html
        })

    path = os.path.join(os.path.dirname(__file__), "news.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape()
