from dateutil.relativedelta import relativedelta


class InstallmentPlanService:
    """
    Service to calculate an installment plan.
    """

    def get_installment_plan(self, total_amount, number_of_installments, start_date):
        """
        Calculate installments based on total amount, number of installments, and start date.
        :param total_amount: Total amount to split
        :param number_of_installments: How many installments
        :param start_date: Starting date for the installments
        :return: List of installments with their due dates
        """
        installments = []
        amount_per_installment = total_amount / number_of_installments

        for i in range(number_of_installments):
            due_date = self.calculate_due_date(start_date, i + 1)
            installments.append(
                {
                    "amount": round(amount_per_installment, 2),
                    "due_date": due_date,  # Only keep date part
                    "status": "Pending",  # Initially, all installments are 'Pending'
                }
            )

        return installments

    def calculate_due_date(self, start_date, months):
        """
        Calculate due date for each installment.
        Adds (months + 1) months to the start_date.
        """
        return start_date + relativedelta(months=months)
