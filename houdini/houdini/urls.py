from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^endpoints/', include('core.urls')),
    url(r'^', include('client.urls')),
]
