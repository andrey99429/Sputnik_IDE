from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=50)
    dir_path = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.PROTECT)


class Version(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    dir_path = models.CharField(max_length=200)
    make_name = models.CharField(max_length=50)
    exec_name = models.CharField(null=True, max_length=50)
    upload_time = models.DateTimeField()
    compile_time = models.DateTimeField(null=True)
