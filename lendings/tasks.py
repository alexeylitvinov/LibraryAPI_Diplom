import datetime

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from lendings.models import Lending


@shared_task
def send_email_task():
    today = timezone.now().today().date()
    send_date = today + datetime.timedelta(days=1)
    lendings = Lending.objects.filter(return_date__date=send_date, active=True)
    email_list = []
    for lending in lendings:
        email_list.append(lending.user.email)
    if email_list:
        send_mail(
            'Библиотека: Срок возврата книг',
            'Срок возврата книги истекает завтра',
            EMAIL_HOST_USER,
            email_list
        )
