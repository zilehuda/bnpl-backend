from django.db import models

from apps.bnpl.choices import IntallmentStatusChoices, PaymentPlanStatusChoices
from apps.bnpl.manager import PaymentPlanManager
from apps.users.models import User
from utils.db.models import BaseModel

# Create your models here.


class PaymentPlan(BaseModel):
    merchant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_plans"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plans")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_installments = models.PositiveIntegerField()
    start_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=PaymentPlanStatusChoices.choices,
        default=PaymentPlanStatusChoices.active,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PaymentPlanManager()

    @property
    def total_paid_installments(self):
        return self.installments.filter(status=IntallmentStatusChoices.paid).count()

    @property
    def total_overdue_installments(self):
        return self.installments.filter(status=IntallmentStatusChoices.late).count()


class Installment(BaseModel):
    payment_plan = models.ForeignKey(
        PaymentPlan, related_name="installments", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=IntallmentStatusChoices.choices,
        default=IntallmentStatusChoices.pending,
    )
