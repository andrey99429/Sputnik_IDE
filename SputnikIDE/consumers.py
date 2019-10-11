from SputnikIDE.models import Project, Version
from channels.db import database_sync_to_async
from channels import consumer


class ConsoleConsumer(consumer.AsyncConsumer):
    async def websocket_connect(self, event):
        user = self.scope['user']
        project_id = self.scope['url_route']['kwargs']['project_id']
        version_id = self.scope['url_route']['kwargs']['version_id']

        version: Version = await self.get_version(user, project_id, version_id)

        await self.send({
            'type': 'websocket.accept'
        })

        if version is not None:
            process = await version.create_process()

            await self.send({
                'type': 'websocket.send',
                'text': 'p{} v{}'.format(project_id, version_id)
            })

        await self.send({
            'type': 'websocket.close'
        })

    @database_sync_to_async
    def get_version(self, user, project_id, version_id):
        if not Project.objects.filter(id=project_id).exists() or \
                Project.objects.get(id=project_id).author != user:
            return None

        if not Version.objects.filter(id=version_id).exists() or \
                Version.objects.get(id=version_id).project_id != project_id:
            return None

        return Version.objects.get(id=version_id)

    async def websocket_receive(self, event):
        # print('received', event)
        pass

    async def websocket_disconnect(self, event):
        # print('disconnected', event)
        pass
