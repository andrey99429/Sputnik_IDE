from django.contrib.auth import views as auth_views
from django.urls import path
import SputnikIDE.views as views
from SputnikIDE.admin import admin_site
import SputnikIDE.admin as admin_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(extra_context=views.get_base_context('Вход')), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('projects/', views.projects, name='projects'),
    path('project/new/', views.project_edit, name='project_new'),
    path('project/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:project_id>/delete/', views.project_delete, name='project_delete'),

    path('project/<int:project_id>/', views.version_editor, name='project'),
    path('project/<int:project_id>/version/<int:version_id>/', views.version_editor, name='version'),
    path('project/<int:project_id>/version/<int:version_id>/load/', views.version_loading, name='version_loading'),
    path('project/<int:project_id>/version/<int:version_id>/delete/', views.version_delete, name='version_delete'),

    path('admin/', admin_site.urls, name='admin_console'),
    path('admin/clear_all_projects/', admin_views.clear_all_projects_view)
]
