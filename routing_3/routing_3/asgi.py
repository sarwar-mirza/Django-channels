"""
ASGI config for routing_3 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter                              # import routing
import app.routing                                               # Create Import routing(websocket)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'routing_3.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        app.routing.websocket_urlpatterns
    )
})
