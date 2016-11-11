from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^applications$', views.applications, name='applications'),
    url(r'^directories$', views.directories, name='directories'),
    url(r'^users$', views.users, name='users'),
    url(r'^roles$', views.roles, name='roles'),
    url(r'^permissions$', views.permissions, name='permissions'),
]
