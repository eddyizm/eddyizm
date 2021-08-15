from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
import json
from datetime import datetime
from blog.models import *
from blog.quotes import get_random_q, get_daily_q

# get current year for display in footer
year_var = datetime.now().strftime('%Y')

# Create your views here.
def post_detail(request, id, slug):
    query_pk_and_slug = True
    post = BlogPost.objects.get(pk = id, slug=slug);
    posts = BlogPost.objects.all()[:5];
    categories = Category.objects.all();
    for cat in post.categories.all():
        if cat.name == 'Photography':
            check_cat = True
            break
        else: 
            check_cat = False

    print(f'show_thumb: {check_cat}') 
    return render_to_response('blog/post.html', 
    {'post' : post, 'posts' : posts, 'slug':slug, 'year':year_var, 'categories': categories, 'hide_thumb': check_cat })

def blog(request):
    return render(
        request,
        'blog/blog.html',
        {
            'title':'Blog',
            'year' : year_var
        }
    )

def blog_posts(request):
    posts = BlogPost.objects.all().order_by('-date')[:3];
    recent_posts = BlogPost.objects.all()[:5];
    categories = Category.objects.all();
    return render_to_response('blog/blog.html', 
    {'posts' : posts, 'recent_posts': recent_posts, 'year':year_var, 'categories': categories })


def blog_category(request, category):
    posts = BlogPost.objects.filter(categories__name__contains=category)
    recent_posts = BlogPost.objects.all()[:5];
    categories = Category.objects.all();
    return render_to_response('blog/category.html', 
        {'posts': posts, 'category': category,'recent_posts': recent_posts, 'year':year_var, 'categories': categories })    


def podcasts(request):
    return render(
        request,
        'blog/podcasts.html',
        {
            'title':'Podcasts',
            'year' : year_var
        }
    )

def about(request):
    return render(
        request,
        'blog/about.html',
        {
            'title':'About',
            'year' : year_var
        }
    )

def projects(request):
    return render(
        request,
        'blog/projects.html',
        {
            'title':'Projects',
            'year' : year_var
        }
    )    

# cfc music player
def cfc(request):
    tracks = MusicTrack.objects.all()
    return render(
        request,
        'blog/cfc.html',
        {
            'title':'Chosen Few Children',
            'year' : year_var,
            'tracks': tracks
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
def quote_v(request):
    q = get_daily_q(False)
    return render_to_response(
        'blog/quote.html',
        {
            'title':'Daily Quotes', 'q' : q ,'year': year_var
        }
    )  