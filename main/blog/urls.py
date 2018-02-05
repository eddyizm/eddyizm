# howdy/urls.py
from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
]
'''
from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
]
'''
