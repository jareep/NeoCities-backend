from .dynamic_consumer import DynamicConsumer
from django.urls import path

dynamic_consumer_urls = [
    path('ws/api/dynamic_data/<sessionKey>/', DynamicConsumer)
]
