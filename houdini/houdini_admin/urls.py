from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hierarchy$', views.hierarchy, name='hierarchy'),
    url(r'^applications$', views.applications, name='applications'),
    url(r'^applications/create$', views.create_application, name='create_application'),
    url(r'^applications/edit/(?P<pk>\d+)$', views.ApplicationUpdate.as_view(), name='edit_application'),
    url(r'^applications/delete/(\d+)$', views.delete_application, name='delete_application'),
    url(r'^users$', views.users, name='users'),
    url(r'^profiles$', views.profiles, name='profiles'),
    url(r'^roles$', views.roles, name='roles'),
    url(r'^roles/create$', views.create_role, name='create_role'),
    url(r'^roles/edit/(?P<pk>\d+)$', views.RoleUpdate.as_view(), name='edit_role'),
    url(r'^roles/delete/(\d+)$', views.delete_role, name='delete_role'),
    url(r'^permissions$', views.permissions, name='permissions'),
    url(r'^permissions/create$', views.create_permission, name='create_permission'),
    url(r'^permissions/edit/(?P<pk>\d+)$', views.PermissionUpdate.as_view(), name='edit_permission'),
    url(r'^permissions/delete/(\d+)$', views.delete_permission, name='delete_permission'),

    url(r'^login_test/$', views.login_test, name='login_test'),
    url(r'^role_test/$', views.role_test, name='role_test'),
    url(r'^permission_test/$', views.permission_test, name='permission_test'),
    url(r'^401/$', views.unauthorized_401, name='401'),
]