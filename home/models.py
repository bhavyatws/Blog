import imp
from operator import mod
from tabnanny import verbose
from django.db import models
from django.db import models

from django.contrib.auth.models import BaseUserManager,PermissionsMixin,AbstractBaseUser
from django.forms import EmailField


# Create your models here.
#Create your customuser model here
class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError('Password must be provided')
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self,email,password,**extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,**extra_fields)
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email,password,**extra_fields)

#Create your user model here

class User(AbstractBaseUser,PermissionsMixin):
    #AbstractBaseUser has password,last_login,is_active by default
    # username=None
    email=models.EmailField(db_index=True,unique=True,max_length=254)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    is_staff=models.BooleanField(default=False)#must need,otherwise you will not able to login
    is_active=models.BooleanField(default=False)#must need,otherwise you will not able to login
    is_superuser=models.BooleanField(default=False)#This is inherited Permissions
    objects=CustomUserManager()
    # EMAIL_FIELD='email'
    USERNAME_FIELD='email'
    REQUIRED_FIELD = []
    class Meta:
        verbose_name='user'
        verbose_name_plural='users'

class Blog(models.Model):
    author=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    post_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100,null=True)
    description=models.CharField(max_length=100,null=True)
    thumbnail=models.ImageField(default="userprofile.png",upload_to='upload/',null=True)
    date_created=models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.title
# class Comment(models.Model):  
#     owner=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
#     title=models.CharField(max_length=200)
#     complete=models.BooleanField(default=False)
#     created_date=models.DateTimeField(auto_now_add=True)
#     due=models.DateTimeField(auto_now=False,auto_now_add=False,null=False,blank=True)
#     def __str__(self):
#         return self.title

