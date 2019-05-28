# Generated by Django 2.2.1 on 2019-05-28 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('dir_name', models.CharField(max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dir_name', models.CharField(max_length=100)),
                ('make_name', models.CharField(max_length=50)),
                ('exec_name', models.CharField(max_length=50, null=True)),
                ('upload_time', models.DateTimeField()),
                ('compile_time', models.DateTimeField(null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ProgramManager.Project')),
            ],
        ),
    ]
