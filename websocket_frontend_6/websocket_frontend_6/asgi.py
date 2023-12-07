
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter         # import routing
import app.routing                                          # custom import routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websocket_frontend_6.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        app.routing.websocket_urlpatterns
    )
})
