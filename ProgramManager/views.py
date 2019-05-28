import os
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from ProgramManager.models import Project, Version, User
from ProgramManager.forms import Project_Form
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
def project_edit(request, project_id=None):
    context = get_base_context('')
    form = None

    if request.method == 'POST':
        form = Project_Form(request.POST)
        if form.is_valid():
            pass
        else:
            pass

    else:
        form = Project_Form()
        if project_id is None:
            context['pagetitle'] = 'Создание проекта'
            context['submit_title'] = 'Создать'
        else:
            context['pagetitle'] = 'Редактирование проекта'
            context['submit_title'] = 'Сохранить'
            if Project.objects.filter(id=project_id).exists():
                form.initial['name'] = Project.objects.get(id=project_id).name
            else:
                raise Http404

    context['form'] = form
    return render(request, 'project_edit.html', context)


@login_required
def project_delete(request, project_id):
    context = get_base_context('Удаление проекта')
    return render(request, 'project_delete.html', context)


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