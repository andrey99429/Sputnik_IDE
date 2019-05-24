from django.db import models


class Program(models.Model):
    name = models.CharField(max_length=150)
    dir_path = models.CharField(null=True, max_length=50)
    exec_path = models.CharField(null=True, max_length=50)
    upload_time = models.DateTimeField()
