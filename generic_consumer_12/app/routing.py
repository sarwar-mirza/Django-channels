from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/wsc/<str:routingGroupName>/', consumers.MyWebsocketConsumer.as_asgi()),           # Ex-o1(websocket SyncConsumer)
    path('ws/wac/<str:routingGroupName>/', consumers.MyAsyncWebsocketConsumer.as_asgi()),      # Ex-02(Async Websocket Consumer)
]