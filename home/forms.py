import imp
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
import datetime

class UserRegisterForm(forms.Form, UserCreationForm):

    username = forms.CharField(max_length=20)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(2017, 1900, -1)))
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    # def clean_date_of_birth(self):
    #     '''
    #     Only accept users aged 13 and above
    #     '''
    #     userAge = 13
    #     dob = self.cleaned_data.get('date_of_birth')
    #     today = date.today()
    #     if (dob.year + userAge, dob.month, dob.day) > (today.year, today.month, today.day):
    #         raise forms.ValidationError('Users must be aged {} years old and above.'.format(userAge))
    #     return dob

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user has already registered using this email')
        return email

    def clean_password2(self):
        '''
        we must ensure that both passwords are identical
        '''
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords must match')
        return password2
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')