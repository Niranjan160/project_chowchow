from django.core.mail import send_mail
from django.conf import settings

def send_reject_email(name, register_no, email):
    subject = "Regarding fees receipt"
    message = f"Hi {name}({register_no}), Your receipt is not valid. Please reupload the receipt and the details."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
    print("Mail sent successfully")