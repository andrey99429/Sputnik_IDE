from django.urls import path
import ProgramManager.views as views

urlpatterns = [
    path('', views.index),
]
