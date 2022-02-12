import email
import imp
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.forms import ValidationError

from .models import *
# Create your views here.
def home(request):
    blog=Blog.objects.all()
    print(request.user)
    # print(blog)
    # hello=Blog.objects.all()
    # print(hello.thumbnail.url)
    context={'blog':blog}
    return render(request,'blog.html',context)
def blogpost(request,id):
    blog=Blog.objects.filter(post_id=id)[0]#it fetch first of Post having same id
    print(blog)
    context={'blog':blog}
    return render(request,'blog_post.html',context)

def sign_in(request):
    if request.method=="POST":
        email=request.POST.get('email')
        # user = User.objects.get(email=email)
        # print(user)
        userpassword=request.POST.get('password')
        # print(email,userpassword)
        user=authenticate(email=email,password=userpassword)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully logged in')
            return redirect('/')
        else:
            messages.error(request,'Invalid Credentials!!,Please try again')
            return redirect('/signin')
        
    context={}
    return render(request,'authentication/login.html',context)
def sign_out(request):
    if request.method == "POST":
        logout(request)
        messages.success(request,'Successfully Logout')
        return redirect('/signin')
    return redirect('/')
def sign_up(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        # print(username,userpassword)
        
        # if not username.isalnum():
        #     messages.success(request,'Username character must alpha-numeric')
        #     return redirect('register')
        if len(name)<5:
            messages.success(request,'Username character must be greater than 5')
            return redirect('register')
       
        try:
            if validate_email(email):
                pass
        except ValidationError as e:
            messages.success(request,'Please enter correct email')
            return redirect('register')
        if password1!=password2:
            messages.success(request,'Password must be same')
            return redirect('register')
       

        user=User.objects.create_user(email=email, password=password1,first_name=name)
        print(user)
        user.save()
        messages.success(request,'Account Created for ' + ' ' + name.title())
        return redirect('/')
    
    
        
    return render(request,'authentication/sign_up.html')


