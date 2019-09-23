from django.apps import AppConfig


class SputnikIDEConfig(AppConfig):
    name = 'SputnikIDE'

    def ready(self):
        from sputnik_ide.settings import PROJECTS_BASE_DIR, DEFAULT_CODE_PATH
        import os
        if not os.path.isdir(PROJECTS_BASE_DIR):
            raise FileExistsError('Folder {} doesn\'t exists!'.format(PROJECTS_BASE_DIR))

        if not os.path.exists(DEFAULT_CODE_PATH):
            raise FileExistsError('File {} doesn\'t exists!'.format(DEFAULT_CODE_PATH))

        print('\n{} is loading...'.format(self.name))
        SputnikIDEConfig.initial()
        print()

    @staticmethod
    def initial():
        SputnikIDEConfig.create_admin('pi', 'prettysecret', 'dabrameshin@hse.ru', 'Администратор', 'Системы')
        SputnikIDEConfig.create_user('user', 'sputnik', 'student@edu.hse.ru', 'Пользоавтель', 'Системы')

    @staticmethod
    def create_admin(username, password, email, first_name, last_name):
        from django.contrib.auth.models import User

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            print('Admin with username "{}" created.'.format(username))
        else:
            print('User with username "{}" is already created.'.format(username))

    @staticmethod
    def create_user(username, password, email, first_name, last_name):
        from django.contrib.auth.models import User

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            print('User with username "{}" created.'.format(username))
        else:
            print('User with username "{}" is already created.'.format(username))

    @staticmethod
    def clear_all_users():
        from django.contrib.auth.models import User
        from SputnikIDE.models import Project

        for user in User.objects.filter(is_superuser=False):
            for project in Project.objects.filter(author=user):
                project.delete()
            user.delete()
