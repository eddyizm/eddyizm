from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django import forms

from blog.models import Blog, Tag

admin.site.register(Blog)
admin.site.register(Tag)
