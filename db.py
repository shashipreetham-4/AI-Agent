import pandas as pd
import requests
import os
import time
import logging
import pymongo
from newspaper import Article
from transformers import pipeline
from slugify import slugify 
import textwrap  


logging.basicConfig(filename='news_agent.log', level=logging.INFO)


MONGO_URI = "mongodb+srv://news_db:12345@cluster0.hryxp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Change if using remote DB
DB_NAME = "news_db"
COLLECTION_NAME = "articles"

# Load summarization model once (for better performance)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def get_mongo_collection():
    """Connects to MongoDB and returns the collection."""
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        return db[COLLECTION_NAME]
    except Exception as e:
        logging.error(f" MongoDB Connection Error: {e}")
        return None


def read_news_links(csv_file="data.csv"):
    """Reads news URLs from a CSV file, ensuring correct format."""
    try:
        df = pd.read_csv(csv_file, usecols=[0], names=["url"], skiprows=1)
        
        # Drop empty values and filter valid URLs
        urls = df["url"].dropna().tolist()
        if not urls:
            raise ValueError("No valid URLs found in CSV!")

        print(f" Found {len(urls)} valid URLs in CSV.")
        return urls
    except Exception as e:
        print(f" Error reading CSV: {e}")
        return []


def extract_news_content(url):
    """Extracts article text from a given URL."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        if not article.text:
            raise ValueError("No text extracted from article!")

        print(f"✅ Extracted: {article.title}")
        return article.title, article.text
    except Exception as e:
        print(f"⚠️ Error extracting from {url}: {e}")
        return None, None


def summarize_text(article_text):
    """Summarizes article, handling long text by splitting into chunks."""
    MAX_TOKENS = 1024  # Model limit

    # If the text is too long, split into chunks
    if len(article_text.split()) > MAX_TOKENS:
        print("⚠️ Article is too long! Splitting into smaller parts...")
        chunks = textwrap.wrap(article_text, width=2000)  # Approximate split
        summaries = []
        
        for chunk in chunks:
            try:
                summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
                summaries.append(summary[0]['summary_text'])
            except Exception as e:
                print(f"⚠️ Error summarizing chunk: {e}")

        return " ".join(summaries)  # Combine chunked summaries
    else:
        # Normal summarization
        summary = summarizer(article_text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']


def optimize_for_seo(summary, title):
    """Generates SEO metadata and keywords."""
    keywords = ", ".join([word.capitalize() for word in title.split()[:5]])  # Simple keyword extraction
    return {
        'title': f"{title} | Latest News Update",
        'meta_description': summary[:160],
        'keywords': keywords.split()
    }


def store_in_mongodb(article_data, seo_data):
    """Stores article data in MongoDB."""
    collection = get_mongo_collection()
    if collection is None:
        print("⚠️ MongoDB Connection Failed. Skipping storage.")
        return

    try:
        document = {
            "title": seo_data['title'],
            "date": time.ctime(),
            "keywords": seo_data['keywords'],
            "meta_description": seo_data['meta_description'],
            "text": article_data['text'],
            "summary": article_data['summary']
        }
        collection.insert_one(document)
        print(f" Article saved to MongoDB: {seo_data['title']}")
    except Exception as e:
        print(f" Error saving to MongoDB: {e}")


def process_news_articles(csv_file="data.csv"):
    """Main function to process news articles from CSV and store in MongoDB."""
    urls = read_news_links(csv_file)
    
    if not urls:
        print("⚠️ No URLs found in CSV. Exiting...")
        return

    for url in urls:
        title, text = extract_news_content(url)
        if not text:
            continue

        summary = summarize_text(text)  # Handles long text
        seo_data = optimize_for_seo(summary, title)

        store_in_mongodb({
            'title': title,
            'text': text,
            'summary': summary
        }, seo_data)


if __name__ == "__main__":
    print(f"🚀 News Agent started. Processing links from CSV...")
    process_news_articles()