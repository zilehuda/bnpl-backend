from django.contrib import admin

from apps.bnpl.models import Installment, PaymentPlan

# Register your models here.
admin.site.register(PaymentPlan)
admin.site.register(Installment)
