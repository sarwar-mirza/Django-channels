from django.urls import path
from . import views

urlpatterns = [
    path('', views.websocketview, name='webhandler'),
]
