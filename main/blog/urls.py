# howdy/urls.py
from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^podcasts/', views.podcasts, name='podcasts'),
]

