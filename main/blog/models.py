from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image


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
    image = models.ImageField(upload_to='images/%Y/%m/', blank=True, null=True)
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
        if self.image:
            super().save(*args, **kwargs)
            new_width = 800
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                new_height =  int(new_width * img.height/img.width)
                img.thumbnail((new_width, new_height), Image.ANTIALIAS)
                cropped = img.crop((0,200,new_width, new_height))
                cropped.save(self.image.path)

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