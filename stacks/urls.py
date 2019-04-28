from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.new, name='new'),
    path('create', views.create, name='create'),
    path('update', views.update, name='update'),
    path('delete', views.delete, name='delete'),
]
