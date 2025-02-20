from rest_framework import serializers
from datetime import datetime
from prisma import Prisma

db = Prisma()

class NewsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    date = serializers.DateTimeField()
    platform = serializers.CharField()
    author = serializers.CharField()
    ticker = serializers.CharField()
    sentiment = serializers.FloatField()
