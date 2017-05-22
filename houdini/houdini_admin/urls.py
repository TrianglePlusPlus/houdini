from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login_test/$', views.login_test, name='login_test'),
    url(r'^role_test/$', views.role_test, name='role_test'),
    url(r'^permission_test/$', views.permission_test, name='permission_test'),
    url(r'^401/$', views.unauthorized_401, name='401'),
]
