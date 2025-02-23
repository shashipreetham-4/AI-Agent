import pandas as pd
import requests
import os
import time
import logging
import pymongo
from newspaper import Article
from transformers import pipeline
from slugify import slugify  # For safe filenames
import textwrap  # To split long text into smaller parts

# ---------------------- Configurations ----------------------
logging.basicConfig(filename='news_agent.log', level=logging.INFO)

# MongoDB Connection
MONGO_URI = "mongodb+srv://news_db:12345@cluster0.hryxp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Change if using remote DB
DB_NAME = "news_db"

# Default collection names
DEFAULT_ARTICLES_COLLECTION = "articles"
HYD_COLLECTION = "hyd"

# Load summarization model using LED which can process long documents
summarizer = pipeline("summarization", model="allenai/led-large-16384")

# ---------------------- Translator (using Helsinki-NLP/opus-mt-en-hi) ----------------------
def translate_to_hindi(text):
    """
    Translates the given text from English to Hindi using the Helsinki-NLP/opus-mt-en-hi model.
    This model is faster and generally lighter than m2m100.
    """
    try:
        translator = pipeline("translation_en_to_hi", model="Helsinki-NLP/opus-mt-en-hi")
        translation = translator(text, max_length=512)
        return translation[0]['translation_text']
    except Exception as e:
        print(f"⚠ Error during translation: {e}")
        return "Translation not available."

# ---------------------- 1️⃣ MongoDB Connection ----------------------
def get_mongo_collection(collection_name):
    """Connects to MongoDB and returns the specified collection."""
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        return db[collection_name]
    except Exception as e:
        logging.error(f"❌ MongoDB Connection Error: {e}")
        return None

# ---------------------- 2️⃣ Read Links from CSV ----------------------
def read_news_links(csv_file):
    """Reads news URLs from a CSV file, ensuring correct format."""
    try:
        df = pd.read_csv(csv_file, header=None, usecols=[1], names=["url"])  # Reading the 2nd column
        # Drop invalid URLs (ensure they start with http)
        df = df[df["url"].str.startswith("http", na=False)]
        urls = df["url"].tolist()
        if not urls:
            raise ValueError("No valid URLs found in CSV!")
        print(f"✅ Found {len(urls)} valid URLs in {csv_file}.")
        return urls
    except Exception as e:
        print(f"❌ Error reading CSV {csv_file}: {e}")
        return []

# ---------------------- 3️⃣ Extract News Content ----------------------
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
        print(f"⚠ Error extracting from {url}: {e}")
        return None, None

# ---------------------- 4️⃣ Summarization (Handles Long Articles) ----------------------
def summarize_text(article_text):
    """
    Summarizes the article text using LED.
    LED can handle long inputs (up to 16,384 tokens) so manual chunking may not be required.
    """
    try:
        summary = summarizer(article_text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print("⚠ Error during summarization:", e)
        # Fall back to splitting text if needed:
        MAX_TOKENS = 1024
        if len(article_text.split()) > MAX_TOKENS:
            print("⚠ Article is too long! Splitting into smaller parts...")
            chunks = textwrap.wrap(article_text, width=2000)  # Approximate split
            summaries = []
            for chunk in chunks:
                try:
                    summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
                    summaries.append(summary[0]['summary_text'])
                except Exception as ce:
                    print(f"⚠ Error summarizing chunk: {ce}")
            return " ".join(summaries)
        else:
            return "Summary not available."

# ---------------------- 5️⃣ SEO Optimization ----------------------
def optimize_for_seo(summary, title):
    """Generates SEO metadata, keywords, and an SEO-friendly slug."""
    keywords = ", ".join([word.capitalize() for word in title.split()[:5]])  # Basic keyword extraction
    slug = slugify(title)
    return {
        'title': f"{title} | Latest News Update",
        'meta_description': summary[:160],
        'keywords': keywords.split(),
        'slug': slug
    }

# ---------------------- 6️⃣ Store in MongoDB ----------------------
def store_in_mongodb(article_data, seo_data, collection_name):
    """Stores article data in MongoDB under the specified collection."""
    collection = get_mongo_collection(collection_name)
    if collection is None:
        print("⚠ MongoDB Connection Failed. Skipping storage.")
        return

    try:
        document = {
            "title": article_data['title'],
            "title_hi": article_data['title_hi'],
            "date": time.ctime(),
            "keywords": seo_data['keywords'],
            "keywords_hi": seo_data['keywords_hi'],
            "meta_description": seo_data['meta_description'],
            "meta_description_hi": seo_data['meta_description_hi'],
            "text": article_data['text'],
            "text_hi": article_data['text_hi'],
            "summary": article_data['summary'],
            "summary_hi": article_data['summary_hi'],
            "topic": article_data['topic'],
            "slug": seo_data['slug']
        }
        collection.insert_one(document)
        print(f"✅ Article saved to MongoDB collection '{collection_name}': {document['title']}")
    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")

# ---------------------- 7️⃣ Classify Article ----------------------
def classify_article(article_text):
    """
    Classify the article into a topic using simple keyword matching.
    """
    topics = {
        "sports": ["sports", "football", "cricket", "basketball", "tennis"],
        "politics": ["election", "government", "senate", "parliament", "policy"],
        "crime": ["crime", "robbery", "theft", "murder", "police"],
        "current events": ["breaking", "news", "update", "current", "events"],
    }
    article_text_lower = article_text.lower()
    for topic, keywords in topics.items():
        for keyword in keywords:
            if keyword in article_text_lower:
                return topic
    return "general"

# ---------------------- 8️⃣ Execute Workflow ----------------------
def process_news_articles(csv_file, collection_name):
    """Processes news articles from the given CSV and stores them in the specified MongoDB collection."""
    urls = read_news_links(csv_file)
    if not urls:
        print(f"⚠ No URLs found in {csv_file}. Exiting...")
        return

    for url in urls:
        title, text = extract_news_content(url)
        if not text:
            continue

        summary = summarize_text(text)  # Uses LED for summarization
        seo_data = optimize_for_seo(summary, title)

        # Translate English fields into Hindi using the faster Helsinki model
        title_hi = translate_to_hindi(title)
        text_hi = translate_to_hindi(text)
        summary_hi = translate_to_hindi(summary)
        meta_description_hi = translate_to_hindi(seo_data['meta_description'])
        keywords_str = " ".join(seo_data['keywords'])
        keywords_hi = translate_to_hindi(keywords_str).split()

        topic = classify_article(text)

        article_data = {
            'title': title,
            'title_hi': title_hi,
            'text': text,
            'text_hi': text_hi,
            'summary': summary,
            'summary_hi': summary_hi,
            'topic': topic
        }
        seo_data.update({
            'meta_description_hi': meta_description_hi,
            'keywords_hi': keywords_hi
        })

        store_in_mongodb(article_data, seo_data, collection_name)

# ---------------------- Run the System ----------------------
if __name__ == '__main__':
    print("🚀 News Agent started.")

    # Process the default CSV file and store in the "articles" collection
    process_news_articles(csv_file="data/telangana_news.csv", collection_name=DEFAULT_ARTICLES_COLLECTION)
    
    # Process the hyd.csv file and store in the "hyd" collection
    process_news_articles(csv_file="data/hyderabad_news.csv", collection_name=HYD_COLLECTION)