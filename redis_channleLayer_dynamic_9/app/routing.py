from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/sc/<str:usergroup>/', consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/<str:usergroup>/', consumers.MyAsyncConsumer.as_asgi()),
    
]