from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('delete_all', views.delete_all, name='delete_all'),
    path('delete', views.delete, name='delete'),
]
