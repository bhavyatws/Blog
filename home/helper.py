from django.conf import settings
from django.core.mail import send_mail
def send_mail_registration(email,token):
    subject='Your account need to be verified to login'
    message=f'Paste the link to verify your account https://shahidblogapp.herokuapp.com/verify/{token}'
    # message=f'Paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)