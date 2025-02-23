import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def fetch_article_content(article_url, use_selenium=False):
    """Extracts full article content by navigating to the article link."""
    if not article_url:
        return "No URL provided"

    try:
        response = requests.get(article_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")

            paragraphs = soup.find_all("p")
            content = " ".join([p.get_text(strip=True) for p in paragraphs]) if paragraphs else None
            
            if content:
                return content.strip()
            
            return fetch_article_content_selenium(article_url) if use_selenium else "Failed to fetch content"
        
        return "Failed to fetch content"
    except Exception as e:
        return f"Error fetching content: {e}"

def fetch_article_content_selenium(article_url):
    """Uses Selenium to extract content from JavaScript-loaded pages."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(article_url)
        time.sleep(5)

        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        content = " ".join([p.text.strip() for p in paragraphs])

        driver.quit()
        return content.strip() if content else "Content not available"

    except Exception as e:
        driver.quit()
        return f"Error with Selenium: {e}"

def fetch_articles_selenium(url, article_tag, max_articles=5):
    """Extracts dynamically loaded articles using Selenium."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(5)

        article_elements = driver.find_elements(By.TAG_NAME, article_tag)

        articles = []
        for tag in article_elements[:max_articles]:
            title = tag.text.strip()
            link = tag.find_element(By.TAG_NAME, "a").get_attribute("href") if tag.find_elements(By.TAG_NAME, "a") else None
            articles.append({"title": title, "url": link})

        driver.quit()
        return articles

    except Exception as e:
        driver.quit()
        return f"Error scraping {url} with Selenium: {e}"

def save_to_csv(data, filename, append=False):
    """Saves scraped data to CSV, ensuring 'content' column exists before filtering missing values."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    df = pd.DataFrame(data)

    if "content" not in df.columns:
        df["content"] = ""

    df = df.dropna(subset=['title', 'url', 'content'], how='all')

    if append and os.path.exists(filename):
        df.to_csv(filename, mode='a', index=False, header=False)
    else:
        df.to_csv(filename, index=False)