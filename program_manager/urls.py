from django.urls import path
from django.contrib.auth import views as auth_views
import ProgramManager.views as views

urlpatterns = [
    path('', views.index),
    path('login/', auth_views.LoginView.as_view(extra_context=views.get_base_context('Вход')), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('projects/', views.projects),
    path('project/<int:project_id>/', views.version),
    path('project/<int:project_id>/version/<int:version_id>', views.version),
]
