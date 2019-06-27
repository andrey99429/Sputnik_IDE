import os
import datetime
from django.db import models
from subprocess import Popen, PIPE
from django.contrib.auth.models import User
from sputnik_ide.settings import PROJECTS_BASE_DIR


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

    @staticmethod
    def default_code_path():
        return PROJECTS_BASE_DIR + '/default.cpp'

    def get_number(self):
        return Version.objects.filter(project=self.project, creation_time__lt=self.creation_time).count() + 1

    def dir_path(self):
        return self.project.dir_path() + self.dir_name

    def code_path(self):
        return self.dir_path() + self.code_name

    def make_path(self):
        return self.dir_path() + self.make_name

    def exec_path(self):
        return self.dir_path() + self.exec_name

    def create_dir(self):
        if not os.path.isdir(self.dir_path()):
            os.mkdir(self.dir_path())

    def init(self):
        self.creation_time = datetime.datetime.now()
        self.dir_name = '/v' + str(self.get_number())
        self.code_name = '/main.cpp'
        self.make_name = '/Makefile'
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
        os.system('cp {} {}'.format(self.default_code_path(), self.code_path()))

    def get_code(self):
        with open(self.code_path(), 'r') as file:
            code = file.read()
            file.close()
            return code

    def write_code(self, code):
        with open(self.code_path(), 'w') as file:
            file.write(code)
            file.close()

    def build(self):
        process = Popen(args='gcc -o {} {} -lstdc++'.format(self.exec_path(), self.code_path()),
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
        out, err = process.communicate()
        return out, err


"""
Ex: Dialog (2-way) with a Popen()

p = subprocess.Popen('Your Command Here',
                 stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT,
                 stdin=PIPE,
                 shell=True,
                 bufsize=0)
p.stdin.write('START\n')
out = p.stdout.readline()
while out:
  line = out
  line = line.rstrip("\n")

  if "WHATEVER1" in line:
      pr = 1
      p.stdin.write('DO 1\n')
      out = p.stdout.readline()
      continue

  if "WHATEVER2" in line:
      pr = 2
      p.stdin.write('DO 2\n')
      out = p.stdout.readline()
      continue

    out = p.stdout.readline()

p.wait()
"""
