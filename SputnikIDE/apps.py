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
        import SputnikIDE.admin as admin
        admin.create_admin('pi', 'prettysecret', 'dabrameshin@hse.ru', 'Администратор', 'Системы')
        admin.create_user('user', 'sputnik', 'student@edu.hse.ru', 'Пользователь', 'Системы')
