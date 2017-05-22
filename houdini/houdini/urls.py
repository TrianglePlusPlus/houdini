from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('houdini_server.urls')),
    url(r'^', include('houdini_client.urls')),
]
