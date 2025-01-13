
from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100) 
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    score = models.IntegerField(default=1200)
# Create your models here.

def __str__(self):
        return self.username