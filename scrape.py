import requests
from bs4 import BeautifulSoup
from config import news_sources, headers
from utils import fetch_article_content, fetch_articles_selenium, save_to_csv
import time
import random
import schedule
import subprocess  

import requests
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
from config import news_sources, headers
from utils import fetch_article_content, fetch_articles_selenium, save_to_csv

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

def get_existing_links(csv_file):
    """Reads the existing CSV and returns a set of links to avoid duplicates."""
    try:
        df = pd.read_csv(csv_file)
        return set(df["url"].dropna().tolist())
    except FileNotFoundError:
        return set()  

def scrape_news():
    """Scrapes news websites periodically and updates the CSV with new articles."""
    news_data = {}

    for name, source in news_sources.items():
        print(f"Scraping {name}...")

        existing_links = get_existing_links(source["csv_file"])  # Check existing articles

        if source.get("use_selenium"):
            articles = fetch_articles_selenium(source["url"], source["article_tag"])
        else:
            articles = []
            for page in range(1, source.get("max_pages", 2) + 1):
                paginated_url = source["pagination_format"].format(page=page) if source.get("pagination") else source["url"]
                print(f"Fetching: {paginated_url}")
                time.sleep(random.uniform(2, 5))

                response = requests.get(paginated_url, headers=headers)
                if response.status_code != 200:
                    print(f"Skipping {paginated_url}, status code: {response.status_code}")
                    break

                soup = BeautifulSoup(response.text, "lxml")
                new_articles = extract_articles(soup, source)

                # Filter out duplicates
                new_articles = [article for article in new_articles if article["url"] not in existing_links]

                if new_articles:
                    if source["csv_file"] not in news_data:
                        news_data[source["csv_file"]] = []
                    news_data[source["csv_file"]].extend(new_articles)


    for csv_file, articles in news_data.items():
        if articles:
            save_to_csv(articles, csv_file, append=True)  # Append new articles
            print(f" {len(articles)} new articles added to '{csv_file}'")
        else:
            print(f"⚠ No new articles found for '{csv_file}'")


    print("🚀 Running dbs.py to process scraped data...")
    try:
        subprocess.run(["python", "dbs.py"], check=True)
        print("✅ Successfully ran dbs.py")
    except subprocess.CalledProcessError as e:
        print(f" Error running dbs.py: {e}")


def start_scheduler():
    """Schedules the scraper to run every hour."""
    print("🚀 Starting the news scraper...")
    

    scrape_news()

    # Schedule it to run every hour
    schedule.every(1).hours.do(scrape_news)

    while True:
        print("⏳ Waiting for next run...")
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_scheduler()