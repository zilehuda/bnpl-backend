from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.bnpl.choices import IntallmentStatusChoices
from apps.bnpl.models import Installment, PaymentPlan
from apps.bnpl.serializers import PaymentPlanCreateSerializer, PaymentPlanListSerializer
from apps.bnpl.services.installment_service import InstallmentPlanService
from apps.users.models import User
from utils.permissions import IsMerchantUser
from utils.response.resp import APIResponse


class PaymentPlanListCreateAPI(ListAPIView):
    serializer_class = PaymentPlanListSerializer

    """
    API View for listing and creating Payment Plans
    """

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsMerchantUser()]
        return super().get_permissions()

    def get_queryset(self):
        plans = PaymentPlan.objects.get_plans_for_user(self.request.user)
        return plans

    @swagger_auto_schema(tags=["plans"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["plans"],
        request_body=PaymentPlanCreateSerializer,
    )
    @transaction.atomic
    def post(self, request):
        serializer = PaymentPlanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email = serializer.validated_data.pop("user_email")
        user = User.objects.get(email=user_email)
        plan = PaymentPlan.objects.create(
            **serializer.validated_data,
            user=user,
            merchant=request.user,
        )

        # Auto-generate installments based on the payment plan
        total_amount = plan.total_amount
        num_installments = plan.number_of_installments
        start_date = plan.start_date

        installment_plan_service = InstallmentPlanService()
        installments = installment_plan_service.get_installment_plan(
            total_amount,
            num_installments,
            start_date,
        )

        for installment in installments:
            Installment.objects.create(
                payment_plan=plan,
                amount=installment["amount"],
                due_date=installment["due_date"],
                status=IntallmentStatusChoices.pending.value,
            )

        return Response(
            APIResponse.get_response(
                message="Payment plan created successfully",
            )
        )
