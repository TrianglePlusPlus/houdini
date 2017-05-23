from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^activate/(?P<key>.+)$', views.activate, name='activate'),
    url(r'^logout/$', views.logout, name='logout'),
]
