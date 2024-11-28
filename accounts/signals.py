from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User


@receiver(post_save, sender=User)
def send_activate_email(sender, instance, created, **kwargs):
    if not created and instance.is_active:
        subject = "Account activate"
        message = f"Dear Sir & Mam / {instance.username},Your Account is Activated Please Login Now "
        from_email = "cspc186@gmail.com"
        list = [instance.email]
        send_mail(subject, message, from_email, list)
