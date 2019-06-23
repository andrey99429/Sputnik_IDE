from django.apps import AppConfig


class SputnikIDEConfig(AppConfig):
    name = 'SputnikIDE'

    def ready(self):
        from django.contrib.auth.models import User
        if User.objects.filter(is_superuser=True).count() == 0:
            user = User.objects.create_superuser('admin', 'mail@mail.com', 'admin')
            user.first_name = 'Администратор'
            user.save()
            print('Admin created')

        from sputnik_ide.settings import PROJECTS_BASE_DIR
        import os
        if not os.path.isdir(PROJECTS_BASE_DIR):
            os.mkdir(PROJECTS_BASE_DIR)