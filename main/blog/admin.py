from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django import forms

from blog.models import BlogPost, Tag

admin.site.register(BlogPost)
admin.site.register(Tag)
