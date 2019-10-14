from SputnikIDE.models import Project, Version
"""
import asyncio.subprocess
import asyncio
"""
import socketserver
import socket
import json

"""
path('project/<int:project_id>/version/<int:version_id>/run/', consumers.ConsoleConsumer)
"""

if __name__ == '__main__':
    print(Project.objects.all())

"""
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
            asyncio.get_event_loop().run_until_complete(self.run_subprocess(version))

        await self.send({
            'type': 'websocket.close'
        })

    async def run_subprocess(self, version):
        process = await asyncio.create_subprocess_shell(Version.run_cmd.format(version.exec_path()),
                                                        stdin=asyncio.subprocess.PIPE,
                                                        stdout=asyncio.subprocess.PIPE,
                                                        stderr=asyncio.subprocess.PIPE,
                                                        )
        is_done = False
        print('before loop')
        while not is_done:
            line = await process.stdout.readline()
            if line == '':
                is_done = True

            data = {'line': line.replace(b'\n', b'<br>')}
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps(data)
            })

        data = {'returncode': process.returncode}
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(data)
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
"""
