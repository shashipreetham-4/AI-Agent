# AI-Agent

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

### Debugging Issues  
- If content extraction fails, check the **HTML tags** used for extraction.  
- If **Selenium is blocked**, increase delays or add user-agents in headers.  

## Deployment (AWS)  
1. **Set up an EC2 instance** with Python and necessary libraries.  
2. **Clone the repository** and install dependencies.  
3. **Run the scraper periodically** using a cron job or systemd service.  

## Contributors  
💡 **Project Developers:**  
- [Shashipreetham](https://github.com/shashipreetham-4)  
- [Sai Varun](https://github.com/Saivarunn2004)  
- [Kaushik](https://github.com/kaushik87599)  
- [Vaishnav](https://github.com/vaishnavv04)  

## License  
This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.  
