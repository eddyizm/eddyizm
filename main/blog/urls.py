from django.conf.urls import url
from django.views.generic.detail import DetailView
from blog import views

urlpatterns = [
    url(r'^$', views.blog, name='blog'),
    # this is probably not going to work. 
    url(r'^blog/(?P<id>[0-9]+)/', views.post_detail, name='post_detail'),   
    #url(r'^blog/(?P<pk>\d+)$', views.post_detail, name='post_detail'),   
    url(r'^blog/', views.blog_posts , name='blog_posts'),
    url(r'^podcasts/', views.podcasts, name='podcasts'),
    url(r'^projects/', views.projects, name='projects'),
    url(r'^about/', views.about, name='about'),
]

