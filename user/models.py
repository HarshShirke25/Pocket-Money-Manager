from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

class MonthlyTotal(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE)
    mincome = models.BigIntegerField(default=0,editable=True)
    left = models.BigIntegerField(default=0)
    date = models.DateField(editable=True)
    daily_limit = models.BigIntegerField(default=0,editable=True)
    def __str__(self):
        return self.user.username
    
class List(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,default=True)
    name = models.CharField(max_length=100)
    
class Expenses(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,default=True)
    list_n = models.ForeignKey(to=List,on_delete=models.CASCADE,default=True)
    expense = models.CharField(max_length=100,default=False)
    cost = models.BigIntegerField(editable=True)
    created_at = models.DateTimeField()
    
    def __str__(self):
        return self.user.username
    
class WishList(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,default=True)
    wish = models.CharField(max_length=100)
    exp = models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.user.username
    
    
    
    
    
     
    
    
    
    
