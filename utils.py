import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from config import headers
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random

def fetch_article_content(article_url, use_selenium=False, retries=3):
    """Extracts full article content by navigating to the article link and detecting the right content structure."""
    if not article_url:
        return "No URL provided"

    for attempt in range(retries):
        try:
            response = requests.get(article_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "lxml")

                # Check if the response contains valid HTML
                if not soup.find():
                    print(f"⚠ Empty response received from {article_url}")
                    return "Invalid response"

                # Print available tags for debugging
                print(f"🔍 Debug: Available tags in {article_url}")
                print([tag.name for tag in soup.find_all()][:50])  # Print first 50 tags

                possible_tags = ["article", "div", "section", "main"]
                content = None

                for tag in possible_tags:
                    main_content = soup.find(tag)
                    if main_content:
                        paragraphs = main_content.find_all("p")
                        if paragraphs:
                            content = " ".join([p.get_text(strip=True) for p in paragraphs])
                            break  
                
                # If no <p> tags found, extract text from entire main content
                if not content and main_content:
                    content = main_content.get_text(strip=True)

                if content:
                    print(f"✅ Extracted content from {article_url[:50]}...: {content[:200]}")
                    return content.strip()
                
                print(f"⚠ Content not found for {article_url}, switching to Selenium...")
                return fetch_article_content_selenium(article_url) if use_selenium else "Failed to fetch content"

            print(f"⚠ Retrying {article_url} (Status: {response.status_code})")
        except requests.RequestException as e:
            print(f"⚠ Error fetching {article_url}: {e}. Retrying {attempt + 1}/{retries}...")
            time.sleep(random.uniform(2, 5))

    return "Failed to fetch content"

def fetch_article_content_selenium(article_url):
    """Uses Selenium to extract content from JavaScript-loaded pages."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    print(f"🟡 Using Selenium to fetch content from: {article_url}")  

    try:
        driver.get(article_url)
        driver.set_page_load_timeout(20)  # Ensure the page doesn't hang forever
        time.sleep(5)  # Wait for JavaScript content to load

        # Scroll down to trigger lazy-loaded content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        content = " ".join([p.text.strip() for p in paragraphs])

        driver.quit()
        return content.strip() if content else "Content not available"

    except Exception as e:
        print(f"❌ Selenium failed for {article_url}: {e}")
        driver.quit()
        return "Failed to fetch content"

def fetch_articles_selenium(url, article_tag, max_articles=5):
    """Extracts multiple dynamically loaded articles using Selenium in one session."""
    print(f"🟡 Starting Selenium for: {url}")  
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript to load content
        print(f"✅ Page loaded successfully: {url}")  

        article_elements = driver.find_elements(By.TAG_NAME, article_tag)
        print(f"🔍 Found {len(article_elements)} articles on {url}")  

        articles = []
        for tag in article_elements[:max_articles]:  # Process only first 5 articles
            title = tag.text.strip()
            link = tag.find_element(By.TAG_NAME, "a").get_attribute("href") if tag.find_elements(By.TAG_NAME, "a") else None
            articles.append({"title": title, "url": link})

        driver.quit()
        print(f"✅ Extracted {len(articles)} articles from {url}")  
        return articles

    except Exception as e:
        print(f"❌ Error scraping {url} using Selenium: {e}")  
        driver.quit()
        return []

def save_to_csv(data, filename):
    """Saves scraped data to CSV, ensuring 'content' column exists before filtering missing values."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Auto-create directory

    df = pd.DataFrame(data)

    # Ensure 'content' column exists before filtering
    if "content" not in df.columns:
        df["content"] = ""

    df = df.dropna(subset=['title', 'url', 'content'], how='all')

    missing_content = df[df["content"].str.contains("Failed|No URL|Content not available", na=False)]
    print(f"⚠ {len(missing_content)} articles have missing content in {filename}")

    df.to_csv(filename, index=False)
