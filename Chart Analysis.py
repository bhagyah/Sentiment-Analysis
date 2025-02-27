import matplotlib.pyplot as plt
import seaborn as sns
import pymongo
import pandas as pd

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["social_data"]
collection = db["tweets"]

# Load data from MongoDB
df = pd.DataFrame(list(collection.find({}, {"_id": 0, "sentiment": 1})))

# Ensure there is data
if df.empty:
    print("No sentiment data found in MongoDB.")
else:
    # Count occurrences of each sentiment
    sentiment_counts = df["sentiment"].value_counts()

    # Plot sentiment analysis results
    plt.figure(figsize=(8, 6))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="viridis")
    plt.xlabel("Sentiment Category")
    plt.ylabel("Count")
    plt.title("Sentiment Analysis Results")

    # Display the chart (No saving, just showing)
    plt.show()
