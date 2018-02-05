from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
 
    def __str__(self):
        return "%s (%s)" % (self.name, self.email)
 
class Post(models.Model):
    title = models.CharField(max_length=64)
    date = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING,)
    body = models.TextField()
 
    def __str__(self):
        return "%s (%s)" % (self.title, self.author.name)
