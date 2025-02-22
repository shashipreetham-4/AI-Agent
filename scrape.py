import requests
from bs4 import BeautifulSoup
from config import news_sources, headers
from utils import fetch_article_content, fetch_articles_selenium, save_to_csv
import time
import random

def extract_articles(soup, source):
    """Extracts headlines, links, and full content from a page."""
    articles = []
    for tag in soup.find_all(source["article_tag"]):
        title = tag.get_text(strip=True)
        if not title:  # Skip articles with no title
            continue  

        link = tag.find("a")["href"] if tag.find("a") else None
        if link and not link.startswith("http"):
            link = source["link_prefix"] + link  

        full_content = fetch_article_content(link, source.get("use_selenium", False)) if link else "No content"

        if title and link and full_content:
            articles.append({"title": title, "url": link, "content": full_content})
    
    return articles

news_data = {}

for name, source in news_sources.items():
    print(f"Scraping {name}...")

    if source.get("use_selenium"):
        articles = fetch_articles_selenium(source["url"], source["article_tag"])
        csv_file = source["csv_file"]
        if csv_file not in news_data:
            news_data[csv_file] = []
        news_data[csv_file].extend(articles)
        continue  

    for page in range(1, source.get("max_pages", 2) + 1):
        paginated_url = source["pagination_format"].format(page=page) if source.get("pagination") else source["url"]
        
        print(f"Fetching: {paginated_url}")
        time.sleep(random.uniform(2, 5))  

        response = requests.get(paginated_url, headers=headers)
        if response.status_code != 200:
            print(f"Skipping {paginated_url}, status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "lxml")
        articles = extract_articles(soup, source)
        
        csv_file = source["csv_file"]
        if csv_file not in news_data:
            news_data[csv_file] = []
        news_data[csv_file].extend(articles)

for csv_file, articles in news_data.items():
    if not articles:
        print(f"⚠ No articles found for '{csv_file}', skipping file creation.")
        continue

    save_to_csv(articles, csv_file)
    print(f"✅ Saved {len(articles)} articles to '{csv_file}'")
