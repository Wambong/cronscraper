import json
import asyncio
from datetime import datetime
from django.core.management.base import BaseCommand
from prisma import Prisma

DATA_FILE = r'C:\Users\User\Downloads\cronscraper\mock_news.json'


def load_mock_news():
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


async def store_news():
    db = Prisma()
    await db.connect()

    news_data = load_mock_news()
    for item in news_data:
        timestamp = datetime.utcfromtimestamp(item['date'])

        await db.news.create(
            data={
                'title': item['title'],
                'description': item['description'],
                'date': timestamp,
                'platform': item['platform'],
                'author': item['author'],
                'ticker': item['ticker'],
                'sentiment': item['sentiment']
            }
        )

    print("News data inserted successfully!")
    await db.disconnect()


class Command(BaseCommand):
    help = "Import mock news data into Prisma"

    def handle(self, *args, **kwargs):
        asyncio.run(store_news())
