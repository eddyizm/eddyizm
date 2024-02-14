from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from .forms import ContactForm
from django.core.paginator import Paginator
from django.core.mail import BadHeaderError
from django.db.models.query_utils import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render, render_to_response
from django.views.generic.list import ListView
from blog.models import *
from blog.ffe_utils import get_daily_q, get_random_q, send_message, update_FFE, get_FFE

# get current year for display in footer
year_var = datetime.now().strftime('%Y')

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
    paginator = Paginator(posts, 3);
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    return render_to_response('blog/category.html', 
        {'posts': posts, 'category': category,
        'recent_posts': recent_posts, 'year':year_var,
        'categories': categories, 'page_obj': page_obj})    


# search blog posts
def search_blogposts(request):
    if request.method =='GET':
        query = request.GET.get('q')
        posts = BlogPost.objects.filter(
          Q(title__icontains=query) | Q(body__icontains=query)  
        )
        recent_posts = BlogPost.objects.all()[:5];
        categories = Category.objects.all();
        results = posts.count();
        return render_to_response('blog/search_results.html', 
        {'posts': posts, 'recent_posts': recent_posts,
         'year':year_var, 'q': query, 'records': results,
        'categories': categories})    


def software(request):
    return render(
        request,
        'blog/software.html',
        {
            'title':'Software',
            'year' : year_var
        }
    )


def about(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print(f'form valid? : {form.is_valid()}')
        print({form.cleaned_data['subject']})
        if form.is_valid() and form.cleaned_data['subject'] == '':
            subject = "Website Inquiry" 
            body = {
			'from_email': form.cleaned_data['from_email'], 
			'message':form.cleaned_data['message'], }
            message = "\n".join(body.values())
            try:
                send_message(message) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("/about/?p=Success")

    form = ContactForm()
    success_post = request.GET.get('p')
    success_post = True if success_post == 'Success' else False
       
    return render(
        request,
        'blog/about.html',
        {
            'title':'About',
            'year' : year_var,
            'form': form,
            'thankyou': success_post,
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
    return JsonResponse(data, content_type='application/json', safe=False)     


def daily_q(request):
    data = get_daily_q(True)
    return JsonResponse(data, content_type='application/json', safe=False) 


# index for quotes
def quote_v(request):
    q = get_daily_q(False)
    return render_to_response(
        'blog/quote.html',
        {
            'title':'Daily Quotes', 'q' : q ,'year': year_var
        }
    )  


# flat file api
@csrf_exempt
def get_ffe_version(request):
    if request.method == 'POST':
        post_data = request.POST.dict()
        try: 
            if post_data['kt'] == '12345':
                print(f"Update version to: {post_data['version']}")
                update_FFE(post_data['version'], post_data['URL'])
                return JsonResponse({'message':'Successfully Updated'}, status=201)
            else:
                return JsonResponse({'message':'401 Unauthorized'}, status=401)
        except:
            return JsonResponse({'message': '401 Unauthorized'}, status=401)
    else: 
        data = get_FFE()
        return JsonResponse(data, content_type='application/json', safe=False)  
     