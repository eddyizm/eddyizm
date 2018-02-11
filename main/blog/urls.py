# howdy/urls.py
from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.blog, name='blog'),
    url(r'^blog/', views.blog , name='blog'),
    url(r'^podcasts/', views.podcasts, name='podcasts'),
    url(r'^projects/', views.projects, name='projects'),
    url(r'^about/', views.about, name='about'),
]

