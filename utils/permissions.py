from rest_framework.permissions import BasePermission


class IsMerchantUser(BasePermission):
    """
    Allows access only to merchant users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_merchant
        )


class IsNormalUser(BasePermission):
    """
    Allows access only to users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and not request.user.is_merchant
        )
