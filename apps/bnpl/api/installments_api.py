from datetime import datetime

from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bnpl.choices import InstallmentTypeChoices, IntallmentStatusChoices
from apps.bnpl.models import Installment
from apps.bnpl.serializers import InstallmentRetrieveSerializer
from apps.bnpl.services.installment_service import InstallmentPlanService
from apps.bnpl.tasks import remind_payment
from utils import swagger_fields
from utils.permissions import IsMerchantUser, IsNormalUser
from utils.response.resp import APIResponse


class InstallmentPlanAPIView(APIView):
    permission_classes = [IsMerchantUser]

    @swagger_auto_schema(
        tags=["Installment Plan"],
        manual_parameters=[
            swagger_fields.number_of_installments,
            swagger_fields.total_amount,
            swagger_fields.start_date,
        ],
    )
    def get(self, request):
        total_amount = request.query_params.get("total_amount")
        number_of_installments = request.query_params.get("number_of_installments")
        start_date = request.query_params.get("start_date")

        if any(
            [
                not total_amount,
                not number_of_installments,
                not start_date,
            ]
        ):
            return Response(APIResponse.get_response(data=[]))

        total_amount = float(total_amount)
        number_of_installments = int(number_of_installments)
        start_date = datetime.strptime(
            start_date, "%Y-%m-%d"
        )  # Expecting date like "2025-05-01"

        service = InstallmentPlanService()

        installments = service.get_installment_plan(
            total_amount, number_of_installments, start_date
        )

        data = {
            "installments": installments,
        }
        return Response(APIResponse.get_response(data=data))


class InstallmentPayAPIView(APIView):
    permission_classes = [IsNormalUser]

    @swagger_auto_schema(tags=["installments"])
    @transaction.atomic
    def post(self, request, installment_id):
        installment = Installment.objects.get(
            id=installment_id, payment_plan__user=request.user
        )

        if not installment:
            return Response(
                APIResponse.get_response(message="Installment not found"), status=404
            )

        if installment.status == IntallmentStatusChoices.paid.value:
            return Response(
                APIResponse.get_response(message="Installment already paid"), status=400
            )

        installment.status = IntallmentStatusChoices.paid.value
        installment.paid_at = datetime.now()
        installment.save()

        return Response(
            APIResponse.get_response(message="Payment proceed successfully")
        )


class UserInstallmentsAPIView(ListAPIView):
    permission_classes = [IsNormalUser]
    serializer_class = InstallmentRetrieveSerializer

    def get_queryset(self):
        queryset = Installment.objects.filter(payment_plan__user=self.request.user)

        # Get the 'due_status' query parameter
        installment_type = self.request.query_params.get("installment_type")

        # Filter by upcoming or past installments
        if installment_type == InstallmentTypeChoices.upcoming.value:
            queryset = queryset.filter(due_date__gte=datetime.now()).order_by(
                "due_date"
            )
        elif installment_type == InstallmentTypeChoices.past.value:
            queryset = queryset.filter(due_date__lt=datetime.now()).order_by("due_date")

        return queryset

    @swagger_auto_schema(
        tags=["installments"], manual_parameters=[swagger_fields.installment_type]
    )
    def get(self, request, *args, **kwargs):
        remind_payment()
        return super().get(request, *args, **kwargs)
