from django.conf.urls import url

from . import views
from . import endpoints


urlpatterns = [
    url(r'^endpoints/login', endpoints.LoginEndpoint.as_view(), name='login_user'),
    url(r'^endpoints/logout', endpoints.LogoutEndpoint.as_view(), name='logout_user'),
    url(r'^endpoints/create_user', endpoints.CreateUserEndpoint.as_view(), name='create_user'),
]
