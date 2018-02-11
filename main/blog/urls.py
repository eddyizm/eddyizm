from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.blog, name='blog'),
    url(r'^blog/', views.blog_posts , name='blog_posts'),
    url(r'^podcasts/', views.podcasts, name='podcasts'),
    url(r'^projects/', views.projects, name='projects'),
    url(r'^about/', views.about, name='about'),
]

