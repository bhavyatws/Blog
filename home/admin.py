from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy  as _
from .models import *
# Register your models here.
from django.contrib.auth import get_user_model
class CustomUserAdmin(UserAdmin):
    '''Define admin model for custom User with no username field'''
    fieldsets = (
        (None, {
            "fields": (
                'email','password'
            ),
        
        }),
    )
    
admin.site.register(get_user_model())
admin.site.register(Blog)