from sputnik_ide.settings import PROJECTS_BASE_DIR, DEFAULT_CODE_PATH
from subprocess import Popen, PIPE, TimeoutExpired
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
import os


class Project(models.Model):
    name = models.CharField(max_length=50)
    dir_name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def dir_path(self):
        return PROJECTS_BASE_DIR + self.dir_name

    def create_dir(self):
        if not os.path.isdir(self.dir_path()):
            os.mkdir(self.dir_path())

    def delete(self, using=None, keep_parents=False):
        for version in Version.objects.filter(project_id=self.id):
            version.delete()
        super().delete(using, keep_parents)
        os.rmdir(self.dir_path())


class Version(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    dir_name = models.CharField(max_length=100)
    code_name = models.CharField(max_length=50)
    make_name = models.CharField(max_length=50)
    exec_name = models.CharField(max_length=50)
    creation_time = models.DateTimeField()
    upload_time = models.DateTimeField(null=True)
    compile_time = models.DateTimeField(null=True)

    def get_number(self):
        return Version.objects.filter(project=self.project, creation_time__lt=self.creation_time).count() + 1

    def dir_path(self):
        return self.project.dir_path() + self.dir_name

    def code_path(self):
        return self.dir_path() + self.code_name

    def exec_path(self):
        return self.dir_path() + self.exec_name

    def create_dir(self):
        if not os.path.isdir(self.dir_path()):
            os.mkdir(self.dir_path())

    def init(self):
        self.creation_time = timezone.now()
        self.dir_name = '/v' + str(self.get_number())
        self.code_name = '/main.cpp'
        self.exec_name = '/exec'

        self.create_dir()
        self.default_code()

    def delete(self, using=None, keep_parents=False):
        for root, dirs, files in os.walk(self.dir_path(), topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.dir_path())

        super().delete(using, keep_parents)

    def default_code(self):
        os.system('cp {} {}'.format(DEFAULT_CODE_PATH, self.code_path()))

    def get_code(self):
        with open(self.code_path(), 'r') as file:
            code = file.read()
            file.close()
            return code

    def write_code(self, code):
        with open(self.code_path(), 'w') as file:
            file.write(code)
            file.close()

    build_cmd = 'cc -Wall -I. -fpic -g -O2 -rdynamic -lm -lschsat -lschsat-dev -ldl {} -o {}'

    def build(self):
        print(Version.build_cmd.format(self.code_path(), self.exec_path()))
        process = Popen(args=Version.build_cmd.format(self.code_path(), self.exec_path()),
                        stdout=PIPE,
                        stderr=PIPE,
                        universal_newlines=True,
                        shell=True)
        out, err = process.communicate()
        return out, err

    def run(self):
        process = Popen(args='{}'.format(self.exec_path()),
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE,
                        universal_newlines=True,
                        shell=True)
        # process.stdin.write('')
        try:
            out, err = process.communicate(timeout=300)
        except TimeoutExpired:
            process.kill()
            out, err = process.communicate()

        return out, err, process.returncode
