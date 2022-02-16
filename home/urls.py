from unicodedata import name
from django.urls import path,include
from . import views


urlpatterns = [
    
    path('',views.home,name="home"),
    path('blog-post/<str:slug>/',views.blogpost,name="blog"),
    path('add-post/',views.addpost,name="addpost"),
    path('delete-post/<int:pk>',views.deletepost,name="delete_post"),
    path('updatepost/<int:pk>',views.updatepost,name="update_post"),
    path('search/',views.search,name="search"),
    path('post-comment/<str:slug>',views.CommentPost,name="postcomment"),
    path('signin/',views.sign_in,name="signin"),
#     path('update-task/<str:pk>/',views.updateTask,name="update"),
#     path('delete-task/<str:pk>/',views.deleteTask,name="delete_task"),
#     path('login/',views.sign_in,name="login"),
    path('logout/',views.sign_out,name="logout"),
    path('register/',views.sign_up,name="register"),
    path('success/',views.success,name="success"),
    path('token-send/',views.token_send,name="token_send"),
    path('verify/<auth_token>',views.verify_account,name="verify"),
    

]
