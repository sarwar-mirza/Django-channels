from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/sc/<str:routingGroupName>/', consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/<str:routingGroupName>/', consumers.MyAsyncConsumer.as_asgi()),
]