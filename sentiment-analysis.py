import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import nltk

# Define the NLTK data directory
nltk_data_dir = os.path.expanduser('~/nltk_data')
nltk.data.path.append(nltk_data_dir)

# Load the data from your CSV file
df = pd.read_csv('reddit_posts.csv')

# Initialize Lemmatizer and Analyzer
lemmatizer = WordNetLemmatizer()
analyzer = SentimentIntensityAnalyzer()


# Preprocessing Functions
def preprocess_text(text):
    """Preprocesses text by removing URLs, special characters, stopwords, and lemmatizing."""
    text = re.sub(r'http\S+|[^\w\s]', '', text).lower()
    words = [lemmatizer.lemmatize(word) for word in text.split() if word.lower() not in stopwords.words('english')]
    return ' '.join(words)


# Apply preprocessing to the title column
df['clean_title'] = df['title'].astype(str).apply(preprocess_text)

# --- Data Visualization ---

# Bar Plot: Frequency of posts in each subreddit
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")
df['subreddit'].value_counts().plot(kind='bar')
plt.title('Frequency of Posts in Each Subreddit')
plt.xlabel('Subreddit')
plt.ylabel('Frequency')
plt.xticks(rotation=0, ha='right')
plt.tight_layout()
plt.show()

# Word Cloud: Most frequent words in the cleaned title column (excluding 'samsung' and 'phone')
text = ' '.join(word for word in df['clean_title'].str.cat(sep=' ').split() if word.lower() not in ['samsung', 'phone'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Title Column (Ignoring "samsung" and "phone")')
plt.axis('off')
plt.show()

# --- Sentiment Analysis ---


# Calculate sentiment polarity and subjectivity using TextBlob
def get_textblob_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity


df['polarity'], df['subjectivity'] = zip(*df['clean_title'].apply(get_textblob_sentiment))


# Calculate sentiment polarity using VADER
def get_vader_sentiment(text):
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']


df['vader_polarity'] = df['clean_title'].apply(get_vader_sentiment)

# Word Frequency Pie Chart
word_counts = df['clean_title'].str.split(expand=True).stack().value_counts()
word_counts = word_counts.drop(['samsung', 'phone'], errors='ignore')

# Plot the pie chart for word frequencies
plt.figure(figsize=(8, 8))
top_n = 30
word_counts[:top_n].plot(kind='pie', autopct='%1.1f%%')
plt.title(f'Distribution of Word Frequencies (Top {top_n})')
plt.ylabel('')
plt.axis('equal')
plt.show()

# --- Plotting ---

plt.figure(figsize=(10, 8))

# Plot the distribution of VADER sentiment polarity
plt.subplot(3, 1, 1)
sns.histplot(df['vader_polarity'], bins=20, kde=True)
plt.title('Distribution of VADER Sentiment Polarity')
plt.xlabel('Polarity')
plt.ylabel('Frequency')

# Plot the distribution of subjectivity
plt.subplot(3, 1, 2)
sns.histplot(df['subjectivity'], bins=20, kde=True)
plt.title('Distribution of Sentiment Subjectivity')
plt.xlabel('Subjectivity')
plt.ylabel('Frequency')

# Scatter plot of VADER polarity
plt.subplot(3, 1, 3)
sns.scatterplot(x='index', y='vader_polarity', data=df.reset_index(), alpha=0.5)
plt.title('VADER Polarity of Posts')
plt.xlabel('Post Index')
plt.ylabel('Polarity')

plt.tight_layout()
plt.show()

# Save the updated DataFrame to a new CSV file
df.to_csv('reddit_posts_with_sentiment.csv', index=False)
print("Data with sentiment analysis saved to 'reddit_posts_with_sentiment.csv'")
