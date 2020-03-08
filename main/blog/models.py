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
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.PROTECT)
    
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
    slug = models.SlugField()
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('slug', 'parent',)    #enforcing that there can not be two
        verbose_name_plural = "categories"       #categories under a parent with same 
                                                 #slug 

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.name]                  # post.  use __unicode__ in place of
                                                 # __str__ if you are using python 2
        k = self.parent                          

        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])
