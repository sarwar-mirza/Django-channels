
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter               # import routing
import app.routing                                                  # Create coustom routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'json_object_7.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        app.routing.websocket_urlpatterns
    )
})
