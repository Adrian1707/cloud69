from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_stack', views.new_stack, name='new_stack'),
    path('create_stack', views.create_stack, name='create_stack'),
]
