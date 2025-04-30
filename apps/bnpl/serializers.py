from django.utils import timezone
from rest_framework import serializers

from apps.bnpl.models import Installment, PaymentPlan
from apps.users.models import User
from utils.db.serializers import UserIdNameSerializer


class InstallmentRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = ["id", "amount", "due_date", "status", "payment_plan"]


class PaymentPlanListSerializer(serializers.ModelSerializer):
    installments = InstallmentRetrieveSerializer(many=True, read_only=True)
    total_paid_installments = serializers.IntegerField()
    total_overdue_installments = serializers.IntegerField()
    # use UserIdNameSerializer for merchant and user
    merchant = UserIdNameSerializer()
    user = UserIdNameSerializer()

    class Meta:
        model = PaymentPlan
        fields = "__all__"


class PaymentPlanCreateSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField()

    class Meta:
        model = PaymentPlan
        fields = [
            "user_email",
            "total_amount",
            "start_date",
            "number_of_installments",
        ]

    def validate_user_email(self, value):
        try:
            User.objects.get(email=value, is_merchant=False)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def validate_start_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return value
