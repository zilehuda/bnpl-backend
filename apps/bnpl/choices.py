from utils.choices.choices import BaseChoices


class PaymentPlanStatusChoices(BaseChoices):
    active = "active", "active"
    paid = "paid", "paid"


class IntallmentStatusChoices(BaseChoices):
    pending = "pending", "pending"
    paid = "paid", "paid"
    late = "late", "late"


class InstallmentTypeChoices(BaseChoices):
    upcoming = "upcoming", "upcoming"
    past = "past", "past"
