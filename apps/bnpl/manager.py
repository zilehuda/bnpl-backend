from django.db import models


class PaymentPlanManager(models.Manager):
    def get_plans_for_user(self, user):
        """
        Returns the payment plans based on the user type (merchant or normal user).
        """
        if user.is_merchant:
            return self.filter(merchant=user)
        return self.filter(user=user)
