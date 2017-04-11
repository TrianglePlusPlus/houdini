from django.conf.urls import url

from . import views
from . import endpoints


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
    url(r'^login', endpoints.LoginEndpoint.as_view(), name='login_user'),
    url(r'^create_user', endpoints.CreateUserEndpoint.as_view(), name='create_user'),
]
