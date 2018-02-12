from django.db import models
from django import forms

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
 
    def __str__(self):
        return "%s (%s)" % (self.name, self.email)

class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, default='')

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    body = models.CharField(max_length=20000)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING,)
    tags = models.ManyToManyField(Tag)
    
    class Meta:
        ordering = ['-date',]

    def __str__(self):
         return self.title

