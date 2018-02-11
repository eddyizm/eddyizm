from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView

# Create your views here.
def blog(request):
    return render(
        request,
        'blog/blog.html',
        {
            'title':'Blog',
        }
    )
# class HomePageView(TemplateView):
#     def get(self, request, **kwargs):
#         return render(request, 'blog/index.html', context=None)

def podcasts(request):
    return render(
        request,
        'blog/podcasts.html',
        {
            'title':'Podcasts',
            #'message':'Your application description page.',
            #'year':datetime.now().year,
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