
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter              # import routing
import app.routing                                              # Create import routing
from channels.auth import AuthMiddlewareStack                  # authentication

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jsonWebSocket_Consumer_13.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            app.routing.websocket_urlpatterns
        )
    )
})
