from django.core.mail import send_mail


def send_welcome_mail(email, user_name):
    subject = "Welcome"
    message = f"Welcome {user_name}!this is seller account"
    from_email = "cspc186@gmail.com"
    list = [email]
    send_mail(subject, message, from_email, list)


def send_otp_mail(email, otp):
    subject = "OTP Code"
    message = f"your otp code is {otp}."
    send_mail(subject, message, 'cspc186@gmail.com', [email])
