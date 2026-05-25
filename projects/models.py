from django.db import models
from django.conf import settings
from  categories.models import Category
# Create your models here.

class Project(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='projects')

    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    budget = models.DecimalField(max_digits=10,decimal_places=2)

    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title