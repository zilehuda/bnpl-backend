from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.bnpl.choices import IntallmentStatusChoices, PaymentPlanStatusChoices
from apps.bnpl.models import Installment


@receiver(post_save, sender=Installment)
def update_payment_plan_status(sender, instance, **kwargs):
    payment_plan = instance.payment_plan

    total_installments = payment_plan.installments.count()
    paid_installments = payment_plan.installments.filter(
        status=IntallmentStatusChoices.paid.value
    ).count()
    if total_installments == paid_installments:
        payment_plan.status = PaymentPlanStatusChoices.paid.value
        payment_plan.save()
