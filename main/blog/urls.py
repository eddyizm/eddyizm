from django.conf.urls import url
from django.views.generic.detail import DetailView
from blog import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.blog_posts, name='blog'),
    path('blog/<int:id>-<str:slug>/', views.post_detail, name='post_detail'),
    url(r'^blog/', views.blog_posts , name='blog_posts'),
    url(r'^podcasts/', views.podcasts, name='podcasts'),
    url(r'^projects/', views.projects, name='projects'),
    url(r'^about/', views.about, name='about'),
    url(r'^chosenfewchildren/', views.cfc, name='chosenfewchildren'),
    # quotes app routes
    url(r'^quotes/random/', views.random_q , name='random'),
    url(r'^quotes/daily/', views.daily_q , name='daily'),
    url(r'^quotes/', views.quote_v , name='quotes'),
]

