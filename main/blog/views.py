from datetime import datetime

from cachetools import TTLCache
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import BadHeaderError
from django.db.models.query_utils import Q
from django.http import JsonResponse, HttpResponseServerError
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt


from .forms import ContactForm
from blog.models import BlogPost, Category, MusicTrack
from blog.ffe_utils import get_daily_q, get_random_q, send_message, update_FFE, get_FFE


cache = TTLCache(maxsize=128, ttl=60 * 60 * 2)
year_var = datetime.now().strftime('%Y')


def post_detail(request, id, slug):
    response = cache.get(id)
    if response is not None:
        print(f'Found post detail in cache: {id}')
    else:
        post = BlogPost.objects.get(pk=id, slug=slug)
        posts = BlogPost.objects.all()[:5]
        categories = Category.objects.all()
        for cat in post.categories.all():
            if cat.name == 'Photography':
                check_cat = True
                break
            else:
                check_cat = False
        response = render(
            request,
            'blog/post.html',
            {
                'post': post,
                'posts': posts,
                'slug': slug,
                'year': year_var,
                'categories': categories,
                'hide_thumb': check_cat
            })
        cache[id] = response
    response["Cache-Control"] = "public, max-age=518400"
    return response


def blog(request):
    response = render(
        request,
        'blog/blog.html',
        {
            'title': 'Blog',
            'year': year_var
        }
    )
    response["Cache-Control"] = "public, max-age=600"
    return response


def blog_posts(request):
    posts = BlogPost.objects.all().order_by('-date')[:3]
    recent_posts = BlogPost.objects.all()[:5]
    categories = Category.objects.all()
    response = render(
        request,
        'blog/blog.html',
        {
            'posts': posts,
            'recent_posts': recent_posts,
            'year': year_var,
            'categories': categories
        })
    response["Cache-Control"] = "public, max-age=600"
    return response


def blog_category(request, category):
    response = cache.get(category)
    if response is not None:
        print(f'category response found in cache: {category}')
    else:
        posts = BlogPost.objects.filter(categories__name__contains=category)
        recent_posts = BlogPost.objects.all()[:5]
        categories = Category.objects.all()
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        response = render(
            request,
            'blog/category.html',
            {
                'posts': posts,
                'category': category,
                'recent_posts': recent_posts,
                'year': year_var,
                'categories': categories,
                'page_obj': page_obj
            })
        cache[category] = response
    response["Cache-Control"] = "public, max-age=600"
    return response

# search blog posts
def search_blogposts(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        response = cache.get(query)
        if response is not None:
            print(f'found query in cache: {query}')
        else:
            posts = BlogPost.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            )
            recent_posts = BlogPost.objects.all()[:5]
            categories = Category.objects.all()
            results = posts.count()
            response = render(
                request,
                'blog/search_results.html',
                {
                    'posts': posts,
                    'recent_posts': recent_posts,
                    'year': year_var,
                    'q': query,
                    'records': results,
                    'categories': categories
                })
            cache[query] = response
        response["Cache-Control"] = "public, max-age=21600"
        return response


def software(request):
    response = render(
        request,
        'blog/software.html',
        {
            'title': 'Software',
            'year': year_var
        }
    )
    response["Cache-Control"] = "public, max-age=21600"
    return response


def about(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print(f'form valid? : {form.is_valid()}')
        print({form.cleaned_data['subject']})
        if form.is_valid() and form.cleaned_data['subject'] == '':
            subject = "Website Inquiry"
            body = {
                'from_email': form.cleaned_data['from_email'],
                'message': form.cleaned_data['message'],
            }
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
            'title': 'About',
            'year': year_var,
            'form': form,
            'thankyou': success_post,
        }
    )


def projects(request):
    response = render(
        request,
        'blog/projects.html',
        {
            'title': 'Projects',
            'year': year_var
        }
    )
    response["Cache-Control"] = "public, max-age=21600"
    return response


@login_required(login_url=settings.ADMIN_URL)
def dashboard(request):
    file = f'{settings.STATIC_ROOT}blog/report.html'
    with open(file) as report:
        response = HttpResponse(report.readlines())
        return response


def cfc(request):
    ''' cfc music player '''
    tracks = MusicTrack.objects.all()
    response = render(
        request,
        'blog/cfc.html',
        {
            'title': 'Chosen Few Children',
            'year': year_var,
            'tracks': tracks
        }
    )
    response["Cache-Control"] = "public, max-age=21600"
    return response


# json views for quotes app
def random_q(request):
    data = get_random_q()
    response = JsonResponse(data, content_type='application/json', safe=False)
    response["Cache-Control"] = "public, max-age=600"
    return response


def daily_q(request):
    daily_quote_cache_key = str(datetime.now().date())
    data = cache.get(daily_quote_cache_key)
    if data is not None:
        print(f'Found daily quote key in cache: {daily_quote_cache_key}')
    else:
        data = get_daily_q()
        data['dateSent'] = daily_quote_cache_key
        cache[daily_quote_cache_key] = data
    response = JsonResponse(data, content_type='application/json', safe=False)
    response["Cache-Control"] = "public, max-age=21600"
    return response


# flat file api
# @csrf_exempt
# def get_ffe_version(request):
#     ''' DEPRECATED '''
#     if request.method == 'POST':
#         post_data = request.POST.dict()
#         try:
#             if post_data['kt'] == settings.FFE_KEY:
#                 print(f"Update version to: {post_data['version']}")
#                 update_FFE(post_data['version'], post_data['URL'])
#                 return JsonResponse({'message': 'Successfully Updated'}, status=201)
#             else:
#                 return JsonResponse({'message': '401 Unauthorized'}, status=401)
#         except HttpResponseServerError:
#             return JsonResponse({'message': '401 Unauthorized'}, status=401)
#     else:
#         data = get_FFE()
#         return JsonResponse(data, content_type='application/json', safe=False)
