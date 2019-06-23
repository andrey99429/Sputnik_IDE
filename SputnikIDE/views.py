from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.urls import reverse

from SputnikIDE.models import Project, Version, User
from SputnikIDE.forms import Project_Form, Version_Loading


def get_base_context(pagetitle=''):
    return {
        'pagetitle': pagetitle,
        'menu': [
            ('Главная', '/'),
            ('Проекты', '/projects/'),
        ],
        'admin_menu': [
            ('Список пользователей', ''),
        ]
    }


def index(request):
    context = get_base_context('Главная')
    return render(request, 'index.html', context)


@login_required
def projects(request):
    context = get_base_context('Список проектов')
    context['projects'] = Project.objects.all()
    return render(request, 'projects.html', context)


@login_required
def project_edit(request, project_id=None):
    context = get_base_context()

    if project_id is None:
        context['pagetitle'] = 'Создание проекта'
        context['submit_title'] = 'Создать'
    else:
        context['pagetitle'] = 'Редактирование проекта'
        context['submit_title'] = 'Сохранить'
    form = None

    if request.method == 'POST':
        form = Project_Form(request.POST)
        if form.is_valid():
            if project_id is None:
                project = Project.objects.create(
                    name=form.cleaned_data['name'],
                    author=request.user
                )
                project.dir_name = '/proj' + str(project.id)
                project.create_dir()
                project.save()
                return redirect(reverse('projects'))
            else:
                if Project.objects.filter(id=project_id).exists():
                    project = Project.objects.get(id=project_id)
                    project.name = form.cleaned_data['name']
                    project.save()
                    return redirect(reverse('projects'))
                else:
                    raise Http404

    else:
        form = Project_Form()
        if project_id is not None:
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
def version_editor(request, project_id, version_id=None):
    context = get_base_context('IDE')

    if not Project.objects.filter(id=project_id).exists() or Project.objects.get(id=project_id).author != request.user:
        raise Http404

    if version_id is None:
        if Version.objects.filter(project_id=project_id).exists():
            version = Version.objects.order_by('-creation_time').first()
            version_id = version.id
        else:
            version = Version(project_id=project_id)
            version.init()
            version.save()
            version_id = version.id

    elif not Version.objects.filter(id=version_id).exists() or \
            Version.objects.get(id=version_id).project_id != project_id or \
            Version.objects.get(id=version_id).project.author != request.user:
        raise Http404

    version = Version.objects.get(id=version_id)
    code = version.get_code()
    context['project_id'] = project_id
    context['version_id'] = version_id
    context['version_code'] = code

    return render(request, 'version.html', context)


@login_required
def version_loading(request, project_id, version_id):
    if not Project.objects.filter(id=project_id).exists() or Project.objects.get(id=project_id).author != request.user:
        raise Http404

    if not Version.objects.filter(id=version_id).exists() or \
            Version.objects.get(id=version_id).project_id != project_id or \
            Version.objects.get(id=version_id).project.author != request.user:
        raise Http404

    if request.method == 'POST':
        form = Version_Loading(request.POST)
        if form.is_valid():
            version = Version.objects.get(id=version_id)
            context = {}
            if form.cleaned_data['new_version']:
                pass
            else:
                version.write_code(form.cleaned_data['code'])
                context['saved'] = True
            if form.cleaned_data['build']:
                out, err = version.build()
                context['build_out'] = out
                context['build_err'] = err
            if form.cleaned_data['run']:
                out, err = version.run()
                context['run_out'] = out
                context['run_err'] = err
            return JsonResponse(context)
        else:
            raise Http404
    else:
        raise Http404


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
