from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'blog/index.html', context=None)

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
