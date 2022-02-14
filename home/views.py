import email
import imp
from turtle import pos
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.forms import ValidationError
from .templatetags import extra_filter
from .models import *
import uuid
# Create your views here.
def home(request):
    blog=Blog.objects.all()
    print(request.user)
    # print(blog)
    # hello=Blog.objects.all()
    # print(hello.thumbnail.url)
    context={'blog':blog}
    return render(request,'blog.html',context)
def blogpost(request,slug):
    # blog=Blog.objects.filter(post_id=id)[0]#it fetch first of Post having same id
    blog=Blog.objects.filter(slug=slug).first()
    comment=BlogComment.objects.filter(blog=blog,parent=None)
    replies=BlogComment.objects.filter(blog=blog).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.comment_id not in replyDict.keys():
            replyDict[reply.parent.comment_id]=[reply]
        else: 
            replyDict[reply.parent.comment_id].append(reply)
    # print(replyDict)
    context={'blog':blog,'comment':comment,'replyDict':replyDict}
    return render(request,'blog_post.html',context)
def CommentPost(request,slug):
    if request.method=="POST":
        comment=request.POST.get('comment')
        user=request.user
        post_id=request.POST.get("post_id")
        blog=Blog.objects.get(post_id=post_id)
        parentSno=request.POST.get("parentSno")
        print(parentSno)
        if parentSno=="":
            comment=BlogComment(comment=comment,blog=blog,user=user)
            comment.save()
            messages.success(request,'Your comment has been posted successfully!')
        else:
            parent=BlogComment.objects.get(comment_id=parentSno)
            reply=BlogComment(comment=comment,blog=blog,user=user,parent=parent)
            reply.save()
            messages.success(request,'Your reply has been posted successfully!')
    return redirect(f'/blog-post/{blog.slug}')


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
        profile_obj=Profile.objects.create_user(token=str(uuid.uuid4()))
        profile_obj.save(commit=False)
        user=User.objects.get(email=email)
        profile_obj.save(user=user)
        profile_obj.save()
        return redirect('/token-send')
    
    
        
    return render(request,'authentication/sign_up.html')


def success(request):
    return render(request,'authentication/success.html')
def token_send(request):
    return render(request,'authentication/token_send.html')