from django.urls import path

from apps.bnpl.api.dashboard_api import MerchantMetricsAPIView
from apps.bnpl.api.installments_api import (
    InstallmentPayAPIView,
    InstallmentPlanAPIView,
    UserInstallmentsAPIView,
)
from apps.bnpl.api.plans_api import PaymentPlanListCreateAPI

urlpatterns = [
    path("plans/", PaymentPlanListCreateAPI.as_view(), name="plans_api"),
    path("installment-plans/", InstallmentPlanAPIView.as_view()),
    path(
        "installments/<int:installment_id>/pay/",
        InstallmentPayAPIView.as_view(),
        name="installment_pay_api",
    ),
    path("users/installments/", UserInstallmentsAPIView.as_view()),
    path(
        "merchant/metrics/", MerchantMetricsAPIView.as_view(), name="merchant-metrics"
    ),
]
