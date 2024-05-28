# Reddit Sentiment Analyzer

This project scrapes Reddit posts from specific subreddits related to Samsung, analyzes the sentiment within those posts, and provides visualizations of the results.

## Installation

1. **Clone the Repository:**

   `git clone https://github.com/vladstoenica/SMA-Project.git`

2. **Install Dependencies:**

   `pip install selenium pandas matplotlib seaborn nltk textblob vaderSentiment wordcloud`

3. **Download NLTK Data:**

   `python -m nltk.downloader stopwords`

   `python -m nltk.downloader wordnet`

4. **Obtain Selenium WebDriver:** Download the WebDriver for your browser (e.g., ChromeDriver) and ensure it's in your system's PATH.

## Usage

1. **Scrape Data:**

   `python scraper.py`

   This will collect Reddit posts from specified subreddits and save them to `reddit_posts.csv`.

2. **Analyze and Visualize:**

   `python sentiment-analysis.py`

   This script performs sentiment analysis on the scraped data, generates visualizations, and saves results to `reddit_posts_with_sentiment.csv`.

## Features

*   **Data Scraping:** Collects posts from specified subreddits using Selenium.
*   **Sentiment Analysis:**
    *   Calculates polarity and subjectivity using TextBlob.
    *   Calculates polarity using VADER (optimized for social media).
*   **Visualizations:**
    *   Bar chart of post frequency per subreddit.
    *   Word cloud of common terms (excluding "Samsung" and "phone").
    *   Pie chart of word frequencies.
    *   Histograms and scatter plot of sentiment distributions.
 
