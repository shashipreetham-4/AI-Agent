news_sources = {
    # **Telangana News Sources**
    "The Hindu Telangana": {
        "url": "https://www.thehindu.com/news/national/telangana/",
        "csv_file": "data/telangana_news.csv",
        "pagination": True,
        "pagination_format": "https://www.thehindu.com/news/national/telangana/page-{page}/",
        "max_pages": 10,
        "article_tag": "h3",
        "link_prefix": "https://www.thehindu.com"
    },
    "Times of India Telangana": {
        "url": "https://timesofindia.indiatimes.com/city/hyderabad",
        "csv_file": "data/telangana_news.csv",
        "pagination": True,
        "pagination_format": "https://timesofindia.indiatimes.com/city/hyderabad/{page}",
        "max_pages": 10,
        "article_tag": "span",
        "link_prefix": "https://timesofindia.indiatimes.com",
        "use_selenium": True
    },
    "Eenadu Telangana": {
        "url": "https://www.eenadu.net/?querystring=telangana",
        "csv_file": "data/telangana_news.csv",
        "use_selenium": True,  
        "article_tag": "h2",
        "link_prefix": "https://www.eenadu.net"
    },
    "Sakshi Telangana": {
        "url": "https://www.sakshi.com/news/telangana",
        "csv_file": "data/telangana_news.csv",
        "pagination": True,
        "pagination_format": "https://www.sakshi.com/news/telangana?page={page}",
        "max_pages": 10,
        "article_tag": "h2",
        "link_prefix": "https://www.sakshi.com"
    },
    "Telangana Today": {
        "url": "https://telanganatoday.com/",
        "csv_file": "data/telangana_news.csv",
        "pagination": True,
        "pagination_format": "https://telanganatoday.com/page/{page}",
        "max_pages": 10,
        "article_tag": "h3",
        "link_prefix": "https://telanganatoday.com"
    },
    # **Hyderabad News Sources**
    "The Hindu Hyderabad": {
        "url": "https://www.thehindu.com/news/cities/Hyderabad/",
        "csv_file": "data/hyderabad_news.csv",
        "pagination": True,
        "pagination_format": "https://www.thehindu.com/news/cities/Hyderabad/page-{page}/",
        "max_pages": 10,
        "article_tag": "h3",
        "link_prefix": "https://www.thehindu.com"
    },
    "Times of India Hyderabad": {
        "url": "https://timesofindia.indiatimes.com/city/hyderabad",
        "csv_file": "data/hyderabad_news.csv",
        "pagination": True,
        "pagination_format": "https://timesofindia.indiatimes.com/city/hyderabad/{page}",
        "max_pages": 10,
        "article_tag": "span",
        "link_prefix": "https://timesofindia.indiatimes.com",
        "use_selenium": True
    },
    "Eenadu Hyderabad": {
        "url": "https://www.eenadu.net/?querystring=hyderabad",
        "csv_file": "data/hyderabad_news.csv",
        "use_selenium": True,  
        "article_tag": "h2",
        "link_prefix": "https://www.eenadu.net"
    },
    "Sakshi Hyderabad": {
        "url": "https://www.sakshi.com/news/hyderabad",
        "csv_file": "data/hyderabad_news.csv",
        "pagination": True,
        "pagination_format": "https://www.sakshi.com/news/hyderabad?page={page}",
        "max_pages": 10,
        "article_tag": "h2",
        "link_prefix": "https://www.sakshi.com"
    },
    "Telangana Today Hyderabad": {
        "url": "https://telanganatoday.com/hyderabad",
        "csv_file": "data/hyderabad_news.csv",
        "pagination": True,
        "pagination_format": "https://telanganatoday.com/hyderabad/page/{page}",
        "max_pages": 10,
        "article_tag": "h3",
        "link_prefix": "https://telanganatoday.com"
    },
    "Deccan Chronicle Hyderabad": {
        "url": "https://www.deccanchronicle.com/nation/current-affairs",
        "csv_file": "data/hyderabad_news.csv",
        "pagination": True,
        "pagination_format": "https://www.deccanchronicle.com/nation/current-affairs/page-{page}.html",
        "max_pages": 10,
        "article_tag": "h3",
        "link_prefix": "https://www.deccanchronicle.com"
    },
    "Hans India Hyderabad": {
        "url": "https://www.thehansindia.com/news/cities/hyderabad",
        "csv_file": "data/hyderabad_news.csv",
        "pagination": True,
        "pagination_format": "https://www.thehansindia.com/news/cities/hyderabad/{page}",
        "max_pages": 10,
        "article_tag": "h3",
        "link_prefix": "https://www.thehansindia.com"
    }
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}
