"""
ASGI config for consumers_2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter         # import routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consumers_2.settings')

application = ProtocolTypeRouter({               # custom application
    'http': get_asgi_application(),
    
})
