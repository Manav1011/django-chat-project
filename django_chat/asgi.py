"""
ASGI config for django_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import django


from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.sessions import SessionMiddlewareStack
import accounts.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chat.settings')
django.setup()

django_asgi_app = get_asgi_application()
app=ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        SessionMiddlewareStack(
            URLRouter(
                accounts.routing.websocket_urlpatterns
            )
        )
    )
})


