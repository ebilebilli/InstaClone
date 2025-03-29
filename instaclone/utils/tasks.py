from django.core.mail import send_mail
from instaclone.settings import EMAIL_HOST_USER

def send_mail_func(user_name:str, user_email:str):
    send_mail(
        f'{user_name}, your account created successfully.',
        'Welcome to InstaClone',
        EMAIL_HOST_USER,
        [user_email],
        fail_silently=True     

    )