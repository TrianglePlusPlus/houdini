from django.conf.urls import url

from . import views
from . import endpoints

urlpatterns = [
    url(r'^endpoints/login', endpoints.LoginEndpoint.as_view(), name='login_user_endpoint'),
    url(r'^endpoints/create_user', endpoints.CreateUserEndpoint.as_view(), name='create_user_endpoint'),
    url(r'^endpoints/activate_user', endpoints.ActivateUserEndpoint.as_view(), name='activate_user_endpoint'),
    url(r'^endpoints/regenerate_activation_key', endpoints.RegenerateActivationKeyEndpoint.as_view(), name='regenerate_activation_key_endpoint'),
    url(r'^endpoints/password_change', endpoints.PasswordChangeEndpoint.as_view(), name='password_change_endpoint'),
    url(r'^endpoints/password_reset', endpoints.PasswordResetEndpoint.as_view(), name='password_reset_endpoint'),
    url(r'^endpoints/password_set', endpoints.PasswordSetEndpoint.as_view(), name='password_set_endpoint'),
    url(r'^endpoints/role_add', endpoints.AddRoleEndpoint.as_view(), name='role_add_endpoint'),
    url(r'^endpoints/role_remove', endpoints.RemoveRoleEndpoint.as_view(), name='role_remove_endpoint'),
    url(r'^endpoints/role_check', endpoints.HasRoleEndpoint.as_view(), name='role_check_endpoint'),
]
