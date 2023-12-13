
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter              # Import routing
import app.routing                                                      # Create import routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'generic_consumer_11.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        app.routing.websocket_urlpatterns
    )
})
