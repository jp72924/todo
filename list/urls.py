from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.task_create, name='task_create'),
    path('<int:id>/mark/', views.task_mark, name='task_mark'),
    path('<int:id>/delete/', views.task_delete, name='task_delete'),
]
