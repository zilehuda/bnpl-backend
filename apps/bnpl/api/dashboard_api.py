# apps/bnpl/views.py

from django.db.models import Sum
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.bnpl.choices import IntallmentStatusChoices, PaymentPlanStatusChoices
from apps.bnpl.models import Installment, PaymentPlan
from utils.response.resp import APIResponse


class MerchantMetricsAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user  # Get the authenticated user (merchant)

        # Calculate Total Revenue
        total_revenue = (
            Installment.objects.filter(
                payment_plan__merchant=user,
                status=IntallmentStatusChoices.paid,
            ).aggregate(Sum("amount"))["amount__sum"]
            or 0
        )
        # Calculate total overdue plans form installment and make plan unique
        total_overdue_plans = (
            Installment.objects.filter(
                status=IntallmentStatusChoices.late.value,
                payment_plan__merchant=user,
            )
            .values("payment_plan")
            .distinct()
            .count()
        )

        # calculate success rate
        total_completed_plans = PaymentPlan.objects.filter(
            merchant=user,
            status=PaymentPlanStatusChoices.paid.value,
        ).count()
        total_plans = PaymentPlan.objects.filter(
            merchant=user,
        ).count()
        success_rate = (
            (total_completed_plans / total_plans) * 100 if total_plans > 0 else 0
        )
        success_rate = round(success_rate, 2)

        data = {
            "total_revenue": total_revenue,
            "overdue_plans": total_overdue_plans,
            "success_rate": success_rate,
        }

        return Response(APIResponse.get_response(data=data))
