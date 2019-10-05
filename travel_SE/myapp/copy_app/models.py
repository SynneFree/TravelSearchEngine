from django.db import models
from django import forms

# Create your models here.
class User(models.Model): 
    username = models.CharField(max_length=128,primary_key=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
 
    def __str__(self):
        return self.name
 
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'


