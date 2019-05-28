import os
from django.db import models
from django.contrib.auth.models import User
from program_manager.settings import PROJECTS_BASE_DIR


class Project(models.Model):
    name = models.CharField(max_length=50)
    dir_name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def dir_path(self):
        return PROJECTS_BASE_DIR + self.dir_name

    def create_dir(self):
        if not os.path.isdir(self.dir_path()):
            os.mkdir(self.dir_path())


class Version(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    dir_name = models.CharField(max_length=100)
    make_name = models.CharField(max_length=50)
    exec_name = models.CharField(null=True, max_length=50)
    upload_time = models.DateTimeField()
    compile_time = models.DateTimeField(null=True)
