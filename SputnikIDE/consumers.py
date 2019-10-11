import asyncio
from channels import consumer


class ConsoleConsumer(consumer.AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        await self.send({
            'type': 'websocket.accept'
        })

        project_id = self.scope["url_route"]["kwargs"]["project_id"]
        version_id = self.scope["url_route"]["kwargs"]["version_id"]

        await asyncio.sleep(1)
        await self.send({
            'type': 'websocket.send',
            'text': 'p{} v{}'.format(project_id, version_id)
        })

    async def websocket_receive(self, event):
        print('received', event)

    async def websocket_disconnect(self, event):
        print('disconnected', event)
