from django.urls import path

from .views import news_feed, news_statistics

urlpatterns = [
    path('news/', news_feed, name='news_feed'),
    path('news/statistics/', news_statistics, name='news_statistics'),
]

