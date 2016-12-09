from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hierarchy$', views.hierarchy, name='hierarchy'),
    url(r'^applications$', views.applications, name='applications'),
    url(r'^users$', views.users, name='users'),
    url(r'^profiles$', views.profiles, name='profiles'),
    url(r'^roles$', views.roles, name='roles'),
    url(r'^permissions$', views.permissions, name='permissions'),
]
