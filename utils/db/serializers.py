from rest_framework import serializers

from apps.users.models import User


class UserIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
        )
