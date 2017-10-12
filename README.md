# Houdini

Remote User SSO Auth Platform for Django

## Features

- SSO platform that authenticates against remote server using [JSON Web Tokens][jwt]
- Remote auth server with Bootstrap admin panel
     * **Applications**: register your client apps with the auth server, including the auth server itself
     * **Roles**: assign permissions to roles and roles to Users; create inheritance hierarchies of roles
     * **Permissions**: create permissions and use them to restrict views
- Client app that can be installed in any Django project
- Decorators to be used in client app, implemented in a custom AuthBackend
     * `@login_required`
     * `@role_required`
     * `@permission_required`
- Built-in features:
     * Login
     * Logout
     * Register
     * Activate User
     * Change Password
     * Reset Password
- Optionally authenticate over HTTPS *(highly recommended)*

**Note: a child Role inherits its parents' Permissions, but cannot authenticate as a parent Role under @role_required**

## Setup

### Server Setup

``` python
# TODO: this section
# includes:
#  - email settings
#  - ACCOUNT_ACTIVATION_TIME, PASSWORD_RESET_TIME
#  - self-signed SSL Cert if you want it
```

### Client Setup

Start by adding `houdini_client` to `INSTALLED_APPS` in your project settings:
``` python
INSTALLED_APPS = [
    ...
    'houdini_client',
]
```

Include `houdini_client` in your main url config:
``` python
urlpatterns = [
    ...
    url(r'^', include('houdini_client.urls')),
]
```

Create an Application in the Houdini admin panel, and add the app's key and secret as well as the Houdini server URL to your settings. It is recommended that you use a config file not stored in the repository that saves these as environment variables:
``` python
HOUDINI_KEY = os.getenv('app_key') # e.g., 'a72bb6e0-46f7-11e7-a919-92ebcb67fe33'
HOUDINI_SECRET = os.getenv('app_secret') # e.g., '7bc68ac4-f597-4b21-a767-56de87d85aed'
HOUDINI_SERVER = os.getenv('houdini_server') # e.g., 'https://www.myhoudiniserver.com'
```

Add these to settings:
``` python
from datetime import timedelta
TIME_TO_LIVE = timedelta(weeks=1) # choose how long accounts should stay logged in
ISO_8601 = "%Y-%m-%dT%H:%M:%S"
```

Setup the necessary auth backend in settings:
``` python
AUTH_USER_MODEL = 'core.User' # your User model here
AUTHENTICATION_BACKENDS = ['houdini_client.auth_backend.RemoteServerAuthBackend']
```

Replace Django's built-in middleware with houdini_client's in settings:
``` diff
MIDDLEWARE = [
    ...
-   'django.contrib.auth.middleware.AuthenticationMiddleware',
+   'houdini_client.middleware.AuthenticationMiddleware',
]
```

Make sure your project's `settings.AUTH_USER_MODEL` has a required `email` (strongly recommended that it is `USERNAME_FIELD`). For example:
``` python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'email'
```

Extend client templates from your base template, if you have one:
``` html
{% extends 'your_app/base.html' %}
{% block content %}

<h3>Activate your account</h3>

...

{% endblock %}
```

If you want, you can also modify `houdini_client/views.py` and the `houdini_client` templates to further customize authentication.

## HTTPS

In order to enable HTTPS, follow [these instructions][django-https].

While in development, you will also have to do this:

 1. Create a self-signed SSL Cert (for example, [here is a tutorial][nginx-self-cert] on doing that with Vagrant and nginx)
 2. Disable python requests verification. For example, in `houdini_client/views.py`, this:
 ``` python
 r = requests.post(
     settings.HOUDINI_SERVER + "/endpoints/password_reset",
     data={
         "app_key": settings.HOUDINI_KEY,
         "jwt_string": jwt_string
 })
 ```
Will be replaced with this:
 ``` python
 r = requests.post(
     settings.HOUDINI_SERVER + "/endpoints/password_reset",
     cert=settings.SSL_DEV_CERT_KEY, # wherever you want to store the path to your self-signed cert
     verify=False,
     data={
         "app_key": settings.HOUDINI_KEY,
         "jwt_string": jwt_string
 })
 ```
 3. After you set `verify=False` on a request, you will also have to disable urllib3 warnings so that your requests still go through, maybe in `manage.py`:
 ``` python
 import requests
 from requests.packages.urllib3.exceptions import InsecureRequestWarning
 requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 ```
 4. Depending on your browser, you maybe have to bypass a warning and allow it to continue to your now "unsafe" site as well as enable loading unsafe scripts if you have any content still being served over HTTP

**Remember to revert all of this when you are no longer using self-signed certs!!**

## Support

 - Any bugs you find in Houdini, please feel free to [report here][issue].
 - You are also welcome to email it@thecorp.org with questions.

## License

  The code is available at the [TrianglePlusPlus][tpp] [Github project][home] under the [MIT license][license].

   [jwt]: https://jwt.io/introduction/
   [django-https]: https://docs.djangoproject.com/en/1.11/topics/security/#ssl-https
   [nginx-self-cert]: https://switchcaseblog.wordpress.com/2016/02/22/creating-a-self-signed-ssl-for-local-development-with-vagrant-nginx/
   [tpp]: https://github.com/triangleplusplus
   [home]: https://github.com/triangleplusplus/houdini
   [issue]: https://github.com/triangleplusplus/houdini/issues
   [license]: http://revolunet.mit-license.org
