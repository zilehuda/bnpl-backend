import random
from datetime import date, timedelta
from decimal import Decimal

import factory
from factory import SubFactory

from apps.bnpl.choices import IntallmentStatusChoices, PaymentPlanStatusChoices
from apps.users.factories import UserFactory

from .models import Installment, PaymentPlan


class PaymentPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentPlan

    merchant = SubFactory(UserFactory)
    user = SubFactory(UserFactory)
    total_amount = factory.LazyFunction(lambda: Decimal(random.uniform(100, 1000)))
    number_of_installments = factory.Iterator([3, 6, 12])
    start_date = factory.LazyFunction(lambda: date.today())
    status = factory.Iterator(PaymentPlanStatusChoices.choices)


class InstallmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Installment

    payment_plan = SubFactory(PaymentPlanFactory)
    amount = factory.LazyFunction(lambda: Decimal(random.uniform(10, 100)))
    due_date = factory.LazyFunction(
        lambda: date.today() + timedelta(days=random.randint(30, 90))
    )
    paid_at = factory.LazyFunction(lambda: None)  # or set to a random date if you want
    status = factory.Iterator(IntallmentStatusChoices.choices)
