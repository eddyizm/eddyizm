from django.urls import re_path as url
from blog import views
from django.urls import path


urlpatterns = [
    url(r'^$', views.blog_posts, name='blog'),
    path('blog/<int:id>-<str:slug>/', views.post_detail, name='post_detail'),
    path("blog/c/<str:category>/", views.blog_category, name="blog_category"),
    url(r'^blog/', views.blog_posts, name='blog_posts'),
    url(r'^software/', views.software, name='software'),
    url(r'^about/', views.about, name='about'),
    url(r'^projects/chosenfewchildren/', views.cfc, name='chosenfewchildren'),
    url(r'^projects/', views.projects, name='projects'),
    url(r'^search/', views.search_blogposts, name='search_results'),
    # quotes app routes
    url(r'^quotes/random/', views.random_q, name='random'),
    url(r'^quotes/daily/', views.daily_q, name='daily'),
    url(r'^quotes/', views.quote_v, name='quotes'),
    # application api
    url(r'^api/v1/flat_file_version', views.get_ffe_version, name='ffe_version'),
    # dashboard
    url(r'^dashboard/', views.dashboard, name='dashboard'),
]
