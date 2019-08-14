from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.urls import reverse

from sputnik_ide.settings import PROJECTS_BASE_DIR
from SputnikIDE.models import Project, Version
from SputnikIDE.forms import Project_Form, Version_Loading, Project_Delete


def get_base_context(pagetitle=''):
    return {
        'pagetitle': pagetitle,
        'menu': [
            ('Главная', '/'),
            ('Проекты', '/projects/'),
        ],
        'admin_menu': [
           # ('Список пользователей', ''),
        ]
    }


def index(request):
    context = get_base_context('Главная')
    return render(request, 'index.html', context)


@login_required
def projects(request):
    context = get_base_context('Список проектов')
    context['projects'] = Project.objects.filter(author=request.user).values('id', 'name')

    for i in range(len(context['projects'])):
        last_version = Project.objects.get(id=context['projects'][i]['id']).version_set.order_by('-creation_time')
        if last_version.exists():
            last_version = last_version.first()
            context['projects'][i]['last_version'] = last_version.upload_time
            context['projects'][i]['upload_time'] = 'v' + str(last_version.get_number())

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
def version_editor(request, project_id, version_id=None):
    context = get_base_context('Project Editor')
    version = None

    if not Project.objects.filter(id=project_id).exists() or Project.objects.get(id=project_id).author != request.user:
        raise Http404

    if version_id is None:
        if Version.objects.filter(project_id=project_id).exists():
            version = Version.objects.filter(project_id=project_id).order_by('-creation_time').first()
        else:
            version = Version(project_id=project_id)
            version.init()
            version.save()

    elif not Version.objects.filter(id=version_id).exists() or \
            Version.objects.get(id=version_id).project_id != project_id or \
            Version.objects.get(id=version_id).project.author != request.user:
        raise Http404

    else:
        version = Version.objects.get(id=version_id)

    context['project_name'] = Project.objects.get(id=project_id).name
    context['project_id'] = project_id
    context['version_id'] = version.id
    context['version_number'] = version.get_number()
    context['version_code'] = version.get_code()

    versions = []
    for version in Project.objects.get(id=project_id).version_set.order_by('-upload_time'):
        versions.append({'id': version.id, 'name': 'v' + str(version.get_number()), 'upload_time': version.upload_time})
    context['versions'] = versions

    return render(request, 'version.html', context)


@login_required
def version_loading(request, project_id, version_id):
    def style(string: str):
        string = string.replace('\n', '<br>')
        string = string.replace(' ', '&nbsp;')
        string = string.replace(PROJECTS_BASE_DIR, '')
        return string

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
                version = Version(project_id=project_id)
                version.init()
                version.upload_time = timezone.now()
                version.write_code(form.cleaned_data['code'])
                version.save()
                context['redirect'] = True
                context['redirect_url'] = reverse('version', kwargs={'project_id': project_id, 'version_id': version.id})
                return JsonResponse(context)
            else:
                version.upload_time = timezone.now()
                version.write_code(form.cleaned_data['code'])
                context['saved'] = True

            context['build_required'] = form.cleaned_data['build']
            if form.cleaned_data['build']:
                out, err = version.build()
                context['build_out'] = style(out)
                context['build_err'] = style(err)

            context['run_required'] = form.cleaned_data['run']
            if form.cleaned_data['run']:
                out, err, returncode = version.run()

                context['run_out'] = style(out)
                context['run_err'] = style(err)
                context['returncode'] = -1 * returncode

            version.save()
            return JsonResponse(context)
        else:
            raise Http404
    else:
        raise Http404


@login_required
def project_delete(request, project_id):
    context = get_base_context('Удаление проекта')

    if not Project.objects.filter(id=project_id).exists() or Project.objects.get(id=project_id).author != request.user:
        raise Http404

    form = None

    if request.method == 'POST':
        form = Project_Delete(request.POST)
        if form.is_valid():
            Project.objects.get(id=project_id).delete()
            return redirect(reverse('projects'))
    else:
        form = Project_Delete()

    context['text'] = 'Вы уверены, что ходите удалить проект {}?'.format(Project.objects.get(id=project_id).name)
    # context['cancel_link'] = reverse('project', kwargs={'project_id':project_id})
    context['cancel_link'] = reverse('projects')
    context['form'] = form

    return render(request, 'project_delete.html', context)


@login_required
def version_delete(request, project_id, version_id):
    context = get_base_context('Удаление версии')

    if not Project.objects.filter(id=project_id).exists() or Project.objects.get(id=project_id).author != request.user:
        raise Http404

    if not Version.objects.filter(id=version_id).exists() or Version.objects.get(id=version_id).project_id != project_id:
        raise Http404

    form = None

    if request.method == 'POST':
        form = Project_Delete(request.POST)
        if form.is_valid():
            Version.objects.get(id=version_id).delete()
            return redirect(reverse('project', kwargs={'project_id': project_id}))
    else:
        form = Project_Delete()

    context['text'] = 'Вы уверены, что ходите удалить версию v{} проекта {}?'.format(Version.objects.get(id=version_id).get_number(), Project.objects.get(id=project_id).name)
    context['cancel_link'] = reverse('version', kwargs={'project_id': project_id, 'version_id': version_id})
    context['form'] = form

    return render(request, 'project_delete.html', context)
