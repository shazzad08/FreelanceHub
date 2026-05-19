from django.db import models
#from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100,unique=True,null=True,blank=True)
    

    def __str__(self):
        return self.name
    