from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/jwsc/<str:routingGroupName>/', consumers.MyJsonWebsocketConsumer.as_asgi()),
    path('ws/ajwsc/<str:routingGroupName>/', consumers.MyAsyncJsonWebsocketConsumer.as_asgi())
]