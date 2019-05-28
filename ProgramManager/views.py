import os
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from ProgramManager.models import Project, Version, User
from ProgramManager.forms import FileLoading
from program_manager.settings import BASE_DIR
from ProgramManager.BuildRun import BuildRun


def get_base_context(pagetitle):
    return {
        'pagetitle': pagetitle,
        'menu': [
            ('', 'Главная'),
            ('/projects/', 'Проекты'),
        ],
        'admin_menu': [
            ('', 'Список пользователей'),
        ]
    }


def index(request):
    context = get_base_context('Главная')
    return render(request, 'index.html', context)


@login_required
def projects(request):
    context = get_base_context('Список проектов')
    return render(request, 'projects.html', context)


@login_required
def version(request, project_id, version_id=None):
    context = get_base_context('IDE')
    return render(request, 'version.html', context)


"""
if request.method == 'POST':
    form = FileLoading(request.POST, request.FILES)
    if form.is_valid():
        file_path = BASE_DIR + '/temp.cpp'
        exec_path = BASE_DIR + '/temp'
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(exec_path):
            os.remove(exec_path)

        with open(file_path, 'wb+') as destination:
            for chuck in request.FILES['file'].chunks():
                destination.write(chuck)

        br = BuildRun(file_path, exec_path)
        out, err = br.build()
        context['build'] = 'out:<br>{}<br>err:<br>{}'.format(out, err.replace('\n', '<br>'))
        out, err = br.run()
        context['run'] = 'out:<br>{}<br>err:<br>{}'.format(out, err)
    else:
        print('is not valid')
else:
    context['form'] = FileLoading()
return render(request, 'index.html', context)
"""