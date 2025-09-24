# Sentiment Analysis (Kafka → MongoDB → Chart)

This little project streams a few example social posts, scores their sentiment, saves the results to MongoDB, and shows a simple chart. You can later swap the sample data for live Twitter/Reddit data if you want.

- `Sentiment analysis 2.py` – produces sample messages to Kafka, consumes them, runs VADER sentiment, writes to MongoDB, and plots a chart (optionally uploads it to S3).
- `Chart Analysis.py` – reads sentiments from MongoDB and shows a bar chart.

## What you need
- Python 3.9+ (Windows)
- MongoDB running locally (`mongodb://localhost:27017`)
- Kafka + Zookeeper running locally (`localhost:9092`)
- (Optional) AWS account + S3 bucket for chart upload

## Install packages
Open PowerShell in the project folder:
`C:\Users\BHAGYA\Downloads\Sentiment-Analysis-main\Sentiment-Analysis-main`

```powershell
# Optional virtual environment
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Dependencies
pip install tweepy praw kafka-python pymongo pandas textblob vaderSentiment pyspark matplotlib seaborn dask boto3
```

Note: PySpark is imported but not needed for the basic run.

## Start services (Windows)
1) MongoDB
- Install MongoDB Community Server if you don’t have it.
- Start the MongoDB service so it’s listening on `localhost:27017`.

2) Kafka & Zookeeper
- Download and extract Kafka (e.g. `kafka_2.13-3.x`). Open PowerShell in that folder.

```powershell
# Window 1: Zookeeper
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties | cat
```

```powershell
# Window 2: Kafka broker
.\bin\windows\kafka-server-start.bat .\config\server.properties | cat
```

Create the topic (run once):
```powershell
.\bin\windows\kafka-topics.bat --create --topic social_media --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 | cat
```

## Run it
Back in the project folder PowerShell window:

```powershell
.\.venv\Scripts\Activate.ps1   # if you created a venv
py "Sentiment analysis 2.py"
```
What happens:
- 3 sample messages are produced to the `social_media` topic.
- The consumer scores sentiment (VADER) and saves docs to MongoDB: DB `social_data`, collection `tweets`.
- A bar chart pops up and is saved to `output/sentiment_results.png`.

Re-open the chart later (without re-streaming):
```powershell
py "Chart Analysis.py"
```

## Optional: live Twitter/Reddit
The script includes placeholders—currently it just sends sample data. To fetch live posts:
- In `Sentiment analysis 2.py`, replace your Twitter `API_KEY`, `API_SECRET`, `ACCESS_TOKEN`, `ACCESS_SECRET`.
- Replace Reddit `CLIENT_ID`, `CLIENT_SECRET`, `YOUR_APP`.

## Optional: upload to S3
If you want the saved chart uploaded to S3:
- Configure AWS credentials (env vars, credentials file, or AWS CLI).
- In `Sentiment analysis 2.py`, set your real bucket name instead of `your-bucket-name`.
- Or, comment out the S3 upload lines to skip it.

## Troubleshooting
- Kafka errors: ensure Zookeeper and Kafka are running and the `social_media` topic exists; broker is `localhost:9092`.
- MongoDB errors: make sure the service is running on `localhost:27017`.
- Missing packages: double‑check the venv is active, then re‑install.
- Empty chart: run `Sentiment analysis 2.py` first so MongoDB has data.
- S3 issues: verify credentials/permissions and bucket name.

## Notes
- Running multiple times will add more documents to MongoDB. Clear `social_data.tweets` if you want a fresh start while testing.
