# AI-Agent

## 🌍 Live Website
Our website is now live! 🎉
🔗 **URL**: [http://34.93.62.126:3000](http://34.93.62.126:3000)

## 🚀 Performance & SEO Excellence  
We are proud to announce that our web application has achieved outstanding performance and SEO scores:  

📱 **Mobile Performance:**  
✅ **100% SEO Score** – Perfect optimization for search engines  
✅ **97% Overall Performance** – Lightning-fast load times and seamless user experience  

💻 **Web Performance:**  
✅ **100% SEO Score** – Fully optimized for search engines  
✅ **80% Overall Performance** – Efficient, responsive, and highly accessible  

## Overview  
AI-Agent is an automated web scraper designed to fetch and process Telangana and Hyderabad news articles. It dynamically extracts content from multiple sources and updates the database for further analysis and summarization.  

## Features  
✅ Scrapes multiple news websites dynamically  
✅ Extracts and stores full article content  
✅ Uses **Selenium** as a fallback for dynamic content  
✅ Periodically updates the database with new articles  
✅ Supports multilingual content  

## Prerequisites  
Ensure you have the following installed:  
- **Python 3.11+**  
- **pip**  
- **Git**  
- **Google Chrome** (for Selenium)  
- **ChromeDriver** (compatible with your Chrome version)  

## Installation  

### 1. Clone the Repository  
```bash
git clone https://github.com/shashipreetham-4/AI-Agent.git
cd AI-Agent
```

### 2. Create a Virtual Environment  
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4. Set Up Configuration  
- Edit **config.py** to add or remove news sources.  
- Ensure **ChromeDriver** is in your system path.  

## Usage  

### Run the Scraper  
```bash
python scrape.py
```

### Run the my-blog-app 
- change the directory to my-blog-app
```bash
npm install
npm run dev
```

### Debugging Issues  
- If content extraction fails, check the **HTML tags** used for extraction.  
- If **Selenium is blocked**, increase delays or add user-agents in headers.  

## Deployment (Google Cloud)  
1. **Set up a VM instance** on Google Cloud with Python and required dependencies.  
2. **Clone the repository**, install dependencies, and schedule the scraper using a cron job or systemd.  

## Contributors  
💡 **Project Developers:**  
- [Shashipreetham](https://github.com/shashipreetham-4)  
- [Sai Varun](https://github.com/Saivarunn2004)  
- [Kaushik](https://github.com/kaushik87599)  
- [Vaishnav](https://github.com/vaishnavv04)  

## License  
This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.  
