As part of the terms of reference, it is required to implement the logic of collecting, processing and API for issuing news on the cryptocurrency market. To do this, it is necessary: 

1. Create a cron job that pulls up the result of parsing news sites for one news item (mock data is attached) and writes them to the database.
2. Implement API methods

2.1.  News feed (see UI)

2.2 News statistics for a specific coin for a given period (the number of news per day, the ratio of news per coin to the total number of coins per day, the average sentiment per day). 

The implementation details (database schemas, API method signatures, and so on), additional functionality, and so on remain within your assumptions. However, if you still have questions or are unclear, please write! 

Stack: python, django and Prisma

# Cryptocurrency News Aggregator

This project implements a cryptocurrency news aggregation system with automated data collection and API endpoints for news retrieval and statistics.

## Features

- Automated news collection via cron jobs
- REST API endpoints for:
  - News feed with filtering capabilities
  - Coin-specific news statistics
  - Sentiment analysis results
- Database storage using Prisma
- Built with Python and Django

## Prerequisites

- Python 3.8+
- Node.js (for Prisma)
- PostgreSQL

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/cryptocurrency-news-aggregator.git
cd cryptocurrency-news-aggregator
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```
3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Set up Prisma:

```bash
npx prisma generate
npx prisma migrate dev
```
## Running the Project

1. Start the Django development server:

```bash
python manage.py runserver
```

2. Set up the cron job:

```bash
python manage.py crontab add
```

## API Endpoints

### News Feed

```bash
GET /api/news/
```
Query parameters:
- `coin`: Filter by cryptocurrency (e.g., BTC, ETH)
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)
### News Statistics

```bash
GET /api/news/statistics/
```

Query parameters:
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)

Response includes:
- Daily news count
- News ratio per coin
- Average daily sentiment

## Project Structure

git config user.name "wambong"