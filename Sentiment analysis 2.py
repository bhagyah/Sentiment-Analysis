### Step 1: Install Required Libraries
# Install dependencies using pip
##pip install tweepy praw kafka-python pymongo pyspark textblob vaderSentiment seaborn matplotlib boto3 dask pandas

### Step 2: Data Collection (Twitter & Reddit API)
import tweepy
import praw
import json
import pymongo
import pandas as pd
from kafka import KafkaProducer, KafkaConsumer
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt
import seaborn as sns
import dask.dataframe as dd
import boto3
import os
#from google.colab import files

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["social_data"]
collection = db["tweets"]

# Twitter API Setup
twitter_auth = tweepy.OAuthHandler('API_KEY', 'API_SECRET')
twitter_auth.set_access_token('ACCESS_TOKEN', 'ACCESS_SECRET')
twitter_api = tweepy.API(twitter_auth)

def get_tweets(keyword, count=100):
    tweets = tweepy.Cursor(twitter_api.search_tweets, q=keyword, lang='en').items(count)
    return [{'text': tweet.text, 'created_at': tweet.created_at} for tweet in tweets]

# Reddit API Setup
reddit = praw.Reddit(client_id='CLIENT_ID',
                     client_secret='CLIENT_SECRET',
                     user_agent='YOUR_APP')

def get_reddit_comments(subreddit, limit=100):
    posts = reddit.subreddit(subreddit).hot(limit=limit)
    return [{'text': post.title, 'created_at': post.created_utc} for post in posts]

# Kafka Producer (Simulating Social Media Data Stream)
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

data_samples = [
    {"user": "John", "tweet": "I love this product!", "timestamp": "2025-02-22T10:00:00"},
    {"user": "Anna", "tweet": "This service is terrible.", "timestamp": "2025-02-22T10:01:00"},
    {"user": "Mike", "tweet": "Not bad, but could be better.", "timestamp": "2025-02-22T10:02:00"}
]

for data in data_samples:
    producer.send("social_media", data)

# Kafka Consumer (Processing the Data)
consumer = KafkaConsumer(
    'social_media',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)["compound"]
    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Store tweets in MongoDB with sentiment analysis
for msg in consumer:
    tweet_data = msg.value
    tweet_data["sentiment"] = analyze_sentiment(tweet_data["tweet"])
    collection.insert_one(tweet_data)
    print("Stored in MongoDB:", tweet_data)

# Fetch data from MongoDB
stored_data = list(collection.find({}, {"_id": 0}))

df = pd.DataFrame(stored_data)

# Count sentiment values
sentiment_counts = df['sentiment'].value_counts()

# Ensure the output directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Plot Bar Chart Using Matplotlib & Seaborn
plt.figure(figsize=(8, 6))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="viridis")
plt.xlabel("Sentiment Category")
plt.ylabel("Count")
plt.title("Sentiment Analysis Results")
plt.show()

# Save the figure
chart_path = os.path.join(output_dir, "sentiment_results.png")
plt.savefig(chart_path)
print(f"✅ Sentiment results chart saved at: {chart_path}")

# AWS S3 Upload
s3 = boto3.client("s3")
s3.upload_file(chart_path, "your-bucket-name", "sentiment_results.png")

# Download in Colab (if using Google Colab)
#files.download(chart_path)