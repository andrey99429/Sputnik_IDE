from django.apps import AppConfig


class ProgrammanagerConfig(AppConfig):
    name = 'ProgramManager'

    def ready(self):
        from django.contrib.auth.models import User
        if User.objects.filter(is_superuser=True).count() == 0:
            user = User.objects.create_superuser('admin', 'mail@mail.com', 'admin')
            user.first_name = 'Администратор'
            user.save()
            print('Admin created')
