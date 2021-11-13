from django.shortcuts import render

def error_404(request, exception):
   context = {}
   return render(request,'blog/404.html', context)

def error_500(request):
   context = {}
   return render(request,'blog/500.html', context)