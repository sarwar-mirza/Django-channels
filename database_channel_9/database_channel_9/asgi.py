

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter         # import routing
import app.routing                                                 # create import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'database_channel_9.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        app.routing.websocket_urlpatterns
    )
})
