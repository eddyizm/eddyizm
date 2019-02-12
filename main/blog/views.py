from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
import json
from blog.models import *
from blog.quotes import get_random_q, get_daily_q

# Create your views here.
def post_detail(request, id):
    post = BlogPost.objects.get(pk = id);
    posts = BlogPost.objects.all()[:5];
    return render_to_response('blog/post.html', {'post' : post, 'posts' : posts})

def blog(request):
    return render(
        request,
        'blog/blog.html',
        {
            'title':'Blog',
        }
    )

def blog_posts(request):
    posts = BlogPost.objects.all().order_by('-date')[:3];
    recent_posts = BlogPost.objects.all()[:5];
    return render_to_response('blog/blog.html', {'posts' : posts, 'recent_posts': recent_posts })


def podcasts(request):
    return render(
        request,
        'blog/podcasts.html',
        {
            'title':'Podcasts',
        }
    )
def about(request):
    return render(
        request,
        'blog/about.html',
        {
            'title':'About',
        }
    )

def projects(request):
    return render(
        request,
        'blog/projects.html',
        {
            'title':'Projects',
        }
    )    

# json views for quotes app
def random_q(request):
    data = get_random_q()
    return HttpResponse(data, content_type='application/json')     

def daily_q(request):
    data = get_daily_q(True)
    return HttpResponse(data, content_type='application/json')     

# index for quotes

# def blog_posts(request):
#     posts = BlogPost.objects.all().order_by('-date')[:3];
#     recent_posts = BlogPost.objects.all()[:5];
#     return render_to_response('blog/blog.html', {'posts' : posts, 'recent_posts': recent_posts })

def quote_v(request):
    q = get_daily_q(False)
    return render_to_response(
        'blog/quote.html',
        {
            'title':'Daily Quotes', 'q' : q
        }
    )  