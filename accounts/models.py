from django.db import models
from django.contrib.auth.models import AbstractUser
from .constant import ROLE_CHOICES
# Create your models here.

class User(AbstractUser):
    
  
    
    role= models.CharField(max_length=50,choices=ROLE_CHOICES)
    is_verified= models.BooleanField(default=False)
    
    def __str__(self):
        return self.first_name