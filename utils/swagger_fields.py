from drf_yasg import openapi

from apps.bnpl.choices import InstallmentTypeChoices

number_of_installments = openapi.Parameter(
    "number_of_installments",
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    required=False,
)
total_amount = openapi.Parameter(
    "total_amount",
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    required=False,
)

start_date = openapi.Parameter(
    "start_date",
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    required=False,
)

due_date = openapi.Parameter(
    "due_date",
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    required=False,
)

installment_type = openapi.Parameter(
    "installment_type",
    openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    required=False,
    enum=InstallmentTypeChoices.keys(),
)
