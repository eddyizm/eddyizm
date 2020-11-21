from django.contrib import admin
from django import forms
from blog.models import BlogPost, Author, Category, MusicTrack
from django.forms import TextInput, Textarea
from django.db import models

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(MusicTrack)

# Added to get text area in admin area for blog post.         
class YourModelAdmin(admin.ModelAdmin):
        formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows':5,'cols':40, 'size':'20'})},
        #models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},
    }

admin.site.register(BlogPost, YourModelAdmin)    