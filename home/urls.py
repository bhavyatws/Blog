from unicodedata import name
from django.urls import path,include
from . import views


urlpatterns = [
   
    path('',views.home,name="home"),
    path('blog-post/<int:id>',views.blogpost,name="blog"),
    path('signin',views.sign_in,name="signin"),
#     path('update-task/<str:pk>/',views.updateTask,name="update"),
#     path('delete-task/<str:pk>/',views.deleteTask,name="delete_task"),
#     path('login/',views.sign_in,name="login"),
    path('logout/',views.sign_out,name="logout"),
    path('register/',views.sign_up,name="register"),
    # path('accounts/', include('allauth.urls')),
    # path('account/',views.account,name="account"),
    # path('lock/',views.lock,name="lock"),
    # path('unlock/',views.unlock,name="lock"),

]
