# mark installment to late if due date is passed
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from apps.bnpl.choices import IntallmentStatusChoices
from apps.bnpl.models import Installment


@shared_task
def mark_installments_as_late():
    """
    Mark installments as late if the due date has passed.
    """
    now = timezone.now()

    installments = Installment.objects.filter(due_date__lt=now).filter(
        status=IntallmentStatusChoices.pending.value
    )
    installments.update(
        status=IntallmentStatusChoices.late.value,
    )


@shared_task
def remind_payment():
    """
    Send reminder for payment 3 days before the due date.
    """
    now = timezone.now()
    target_date = now + timedelta(days=3)
    installments = Installment.objects.filter(due_date=target_date)
    for installment in installments:
        send_mail(
            subject="Payment Reminder",
            message="Your instalment is due in 3 days",
            recipient_list=[installment.payment_plan.user.email],
            fail_silently=False,
            from_email=settings.DEFAULT_FROM_EMAIL,
        )
