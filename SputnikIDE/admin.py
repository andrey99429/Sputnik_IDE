from django.contrib.auth.decorators import login_required
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.shortcuts import redirect

from SputnikIDE.models import Project, Version


class MyAdminSite(AdminSite):
    def each_context(self, request):
        context = super(MyAdminSite, self).each_context(request)
        context['special_actions'] = [
            ('Удалить все проекты', 'clear_all_projects/')
        ]
        return context


admin_site = MyAdminSite(name='MyAdmin')
admin_site.register(Project)
admin_site.register(Version)
admin_site.register(User)


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


@login_required
def clear_all_projects_view(request):
    if request.user.is_superuser:
        for user in User.objects.filter(is_superuser=False):
            for project in Project.objects.filter(author=user):
                project.delete()
    return redirect('/admin/')


def clear_all_users():
    for user in User.objects.filter(is_superuser=False):
        for project in Project.objects.filter(author=user):
            project.delete()
        user.delete()
