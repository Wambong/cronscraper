
import datetime

from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from prisma import Prisma
from .serializers import NewsSerializer
import asyncio

db = Prisma()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def connect_db():
    if not db.is_connected():
        await db.connect()

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

@api_view(['GET', 'POST'])
def news_feed(request):
    loop.run_until_complete(connect_db())  # Ensure Prisma is connected

    paginator = CustomPagination()  # Initialize paginator

    # Check if a search query is provided in the request
    ticker = request.GET.get('ticker', None)  # Get ticker from query parameters for GET requests
    if request.method == 'POST':
        # Read raw text from the request body for POST requests
        ticker = request.body.decode('utf-8').strip()

    if ticker:
        ticker = ticker.upper()
        # Filter news based on the ticker
        news = loop.run_until_complete(db.news.find_many(where={'ticker': ticker}, order={'date': 'desc'}))
    else:
        # Return all news when no ticker is provided
        news = loop.run_until_complete(db.news.find_many(order={'date': 'desc'}))

    # Apply pagination to the filtered news list (either all news or filtered by ticker)
    paginated_news = paginator.paginate_queryset(news, request)

    # Serialize the data
    serializer = NewsSerializer(paginated_news, many=True)

    # The search form should appear first in the response
    response_data = {
        "news": serializer.data,
        "search_form": {
            "message": "Use the search form to find news by ticker symbol.",
            "placeholder": "Enter a ticker symbol (e.g., BTC) and submit as raw text",
            "method": "POST",
            "example_input": "BTC",
            "endpoint": "/api/news/",
            "statistics_link": request.build_absolute_uri(reverse('news_statistics'))
        },
        "pagination": {
            "current_page": paginator.page.number if paginator.page else 1,
            "total_pages": paginator.page.paginator.num_pages if paginator.page else 1,
            "next_page": paginator.get_next_link(),
            "previous_page": paginator.get_previous_link()
        }

    }
    return paginator.get_paginated_response(response_data)





@api_view(['GET', 'POST'])
def news_statistics(request):
    """Returns statistics for a specific coin over a given period, with an input form for ticker, start_date, and end_date."""
    loop.run_until_complete(connect_db())  # Ensure Prisma is connected

    if request.method == 'GET':
        # Display input form for ticker, start_date, and end_date
        return Response({
            "message": "Please provide the ticker, start date, and end date to fetch the news statistics.",
            "form_fields": {
                "ticker": "Enter the coin's ticker symbol (e.g., BTC)",
                "start_date": "Enter the start date (format: YYYY-MM-DD)",
                "end_date": "Enter the end date (format: YYYY-MM-DD)",
                "news_feed_link": request.build_absolute_uri(reverse('news_feed'))
            },
            "method": "POST",
            "example_input": {
                "ticker": "BTC",
                "start_date": "2024-01-01",
                "end_date": "2024-01-10"
            }
        })

    if request.method == 'POST':
        # Extract the data from the POST body
        data = request.data
        ticker = data.get('ticker')
        ticker = ticker.upper()
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Validate required fields
        if not ticker or not start_date or not end_date:
            return Response({"error": "ticker, start_date, and end_date are required"}, status=400)

        try:
            # Parse the dates
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Query news data for the specific coin
        coin_news_data = loop.run_until_complete(db.news.find_many(
            where={
                'ticker': ticker,
                'date': {'gte': start_date, 'lte': end_date}
            }
        ))

        # Query news data for all coins within the same date range
        all_news_data = loop.run_until_complete(db.news.find_many(
            where={
                'date': {'gte': start_date, 'lte': end_date}
            }
        ))

        # Initialize dictionaries to accumulate statistics
        total_news_per_day = {}      # Total news per day for the selected coin
        sentiment_sum_per_day = {}   # Sum of sentiment per day for the selected coin
        news_count_per_day = {}      # Count of news per day for the selected coin
        total_news_all_coins = {}    # Total news count per day across all coins

        # Process news data for the selected coin
        for item in coin_news_data:
            day = item.date.strftime('%Y-%m-%d')
            total_news_per_day[day] = total_news_per_day.get(day, 0) + 1
            sentiment_sum_per_day[day] = sentiment_sum_per_day.get(day, 0) + item.sentiment
            news_count_per_day[day] = news_count_per_day.get(day, 0) + 1

        # Process news data for all coins
        for item in all_news_data:
            day = item.date.strftime('%Y-%m-%d')
            total_news_all_coins[day] = total_news_all_coins.get(day, 0) + 1

        # Prepare the statistics for the response
        stats = []
        for day in total_news_per_day:
            avg_sentiment = sentiment_sum_per_day[day] / news_count_per_day[day]
            total_news_on_day = total_news_all_coins.get(day, 1)  # Avoid division by zero
            news_ratio = total_news_per_day[day] / total_news_on_day  # Ratio of news per coin to total news

            stats.append({
                'date': day,
                'news_count': total_news_per_day[day],
                'average_sentiment': round(avg_sentiment, 2),
                'news_ratio': round(news_ratio, 4)  # Rounded for better readability
            })

        # Disconnect from the database
        loop.run_until_complete(db.disconnect())

        return Response(stats)