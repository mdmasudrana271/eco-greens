from django.db import models
from django.contrib.auth.models import User
from . constant import Account_type

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    account_type=models.CharField(choices=Account_type,default='Buyer',max_length=30)
    mobile_no=models.CharField(max_length=12,null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)