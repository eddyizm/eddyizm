from django.contrib import admin
from django.urls import re_path, include
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    re_path(r'^admin/', admin.site.urls, name='admin-site'),
    re_path(r'^', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = views.error_404
handler500 = views.error_500

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

