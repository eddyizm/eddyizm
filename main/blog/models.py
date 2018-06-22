from django.db import models
from django import forms

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
 
    def __str__(self):
        return "%s (%s)" % (self.name, self.email)

# class Tag(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.CharField(max_length=255, null=True, default='')

#     def __str__(self):
#         return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    body = models.CharField(max_length=20000)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING,)
    #tags = models.ManyToManyField(Tag)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.PROTECT)
    
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
