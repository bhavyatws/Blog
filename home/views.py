
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
from .helper import send_mail_registration
from django.db.models import Q
# Create your views here.
def home(request):
    blog=Blog.objects.all()
    
    # print(blog)
    # hello=Blog.objects.all()
    # print(hello.thumbnail.url)
    context={'blog':blog}
    return render(request,'blog.html',context)
def blogpost(request,slug):
    # blog=Blog.objects.filter(post_id=id)[0]#it fetch first of Post having same id
    blog=Blog.objects.filter(slug=slug).first()
    if blog.viewers == None:
            blog.viewers = ""
            blog.save()
    user=request.user
    if user.is_authenticated and user.first_name not in blog.viewers:
            # increment 
        blog.numViews += 1
        blog.save()
        # add username to viewers list
        blog.viewers+=user.first_name
        blog.save()
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
        try:
            if validate_email(email):
                pass
        except ValidationError as e:
            messages.success(request,'Please enter correct email')
            return redirect('/signin')
        # user = User.objects.get(email=email)
        # print(user)
        userpassword=request.POST.get('password')
        user=User.objects.filter(email=email).first()
        # if user is None:
        #     messages.success(request,'Email doesnot exist')
        #     return redirect('/signin')
        profile_obj=Profile.objects.filter(customer=user).first()
        if profile_obj is None:
            messages.success(request,'Please check for Your mail for verification')
            return redirect('/signin')
        if profile_obj.is_verified==True:
            user=authenticate(email=email,password=userpassword)
            if user is not None:
                login(request,user)
                messages.success(request,'Successfully logged in')
                return redirect('/')
            else:
                messages.error(request,'Invalid Credentials!!,Please try again')
                return redirect('/signin')
        else: 
            messages.success(request,'Account has not been verified')
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
        if User.objects.filter(email=email).first():
           messages.success(request,'Email has been taken')
           return redirect('/register')

        user=User.objects.create_user(email=email, password=password1,first_name=name)
        print(user)
        user.save()
        messages.success(request,'Account Created for ' + ' ' + name.title())
        auth_token=str(uuid.uuid4())
        profile_obj=Profile.objects.create(customer=user,auth_token=auth_token)
        # profile_obj.save(commit=False)
        # profile_obj.customer=email 
        profile_obj.save()
        send_mail_registration(email,auth_token)
        messages.success(request,'Verification link  has been sent')
        return redirect('/token-send')
    
    
        
    return render(request,'authentication/sign_up.html')


def success(request):
    messages.success(request,'Account Verified .You can login now')
    return render(request,'authentication/success.html')
def token_send(request):
    return render(request,'authentication/token_send.html')
def verify_account(request,auth_token):
    profile_obj=Profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified==True:
            messages.success(request,"Account already has been verified")
            return redirect('/signin')
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,"Account has been verified")
        return redirect('/signin')
    else:
        return HttpResponse('Token doesnot exist')
def addpost(request):
    if request.method == "POST":
        title=request.POST.get('title')
        description=request.POST.get('description')
        author=request.POST.get('user')
        user=User.objects.get(email=author)
        slug=title + '-' +author
        blog=Blog(title=title,description=description,author=user,slug=slug)
        blog.save()
        return redirect('/')
    return render(request,'addpost.html')
def updatepost(request,pk):
    queryset=Blog.objects.filter(post_id=pk)
    if queryset.exists():
        queryset=Blog.objects.filter(author=request.user).first()
        if request.method=='POST':
            title=request.POST.get('title')
            description=request.POST.get('description')
            author=request.POST.get('user')
            slug=title + '-' +author
            user=User.objects.get(email=author)
            blog=Blog(post_id=pk,title=title,description=description,slug=slug,author=user)
            blog.save()
            return redirect('/')
        date_created=queryset.date_created
        context={'queryset':queryset,'date_created':date_created}
        return render(request,'updatepost.html',context)
    else:
        return redirect('/')
   

def deletepost(request,pk):
    queryset=Blog.objects.filter(post_id=pk)
    if queryset.exists():
        queryset=Blog.objects.filter(author=request.user).first()
        if request.method=="POST":
            queryset.delete()
            return redirect('/')
        context={'blog':queryset}
        return render(request,'deletepost.html',context)
    else:
        return redirect('/')

def search(request):
    query=request.GET.get('query')
    blog=Blog.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))
    # print(blog)
    # hello=Blog.objects.all()
    # print(hello.thumbnail.url)
    context={'blog':blog}
    return render(request,'blog.html',context)
