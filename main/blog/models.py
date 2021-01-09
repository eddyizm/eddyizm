from django.db import models
from django import forms
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
 
    def __str__(self):
        return "%s (%s)" % (self.name, self.email)

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    body = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING,)
    slug = models.SlugField(
        default='',
        editable=False,
        max_length=100
    )
    categories = models.ManyToManyField('Category', related_name='posts')
    
    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        
        return reverse('post_detail', kwargs={'slug': self.slug, 'id':self.id})

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)        
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['-date',]

    def __str__(self):
         return self.title

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
        verbose_name_plural = "categories"      
                                                
    def __str__(self):                          
        return self.name
        

class MusicTrack(models.Model):
    artist = models.CharField(max_length=64)
    album = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    dataURL = models.URLField()

    def __str__(self):
        return "%s-%s-%s-%s" % (self.id, self.title, self.artist, self.album)