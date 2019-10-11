from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

import SputnikIDE.consumers as consumers
application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    path('project/<int:project_id>/version/<int:version_id>/run/', consumers.ConsoleConsumer)
                ]
            )
        )
    )
})
