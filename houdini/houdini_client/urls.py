from django.conf.urls import url
from django.contrib.auth.views import password_change

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^activate/(?P<key>.+)$', views.activate, name='activate'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    # url(r'^password_reset/$', password_reset, {'template_name': 'houdini_client/password_reset.html'}, name='password_reset'),
]
