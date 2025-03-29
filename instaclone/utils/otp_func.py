from django.core.cache import cache
import pyotp
from django.core.mail import send_mail
from instaclone.settings import EMAIL_HOST_USER

def send_otp_func(user_name:str, user_email:str):
    totp = pyotp.TOTP(pyotp.random_base32())
    otp = totp.now()

    cache.set(f'otp_{user_email}', otp, timeout=300)

    send_mail(
        f'{user_name},your OTP Code',
        f'Your OTP code is: {otp}',
        EMAIL_HOST_USER,
        [user_email],
        fail_silently=True
    )

