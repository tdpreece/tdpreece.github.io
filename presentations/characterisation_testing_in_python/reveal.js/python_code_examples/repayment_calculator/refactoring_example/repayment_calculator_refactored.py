"""Payment Calculator - refactored for improved performance.



"""
from decimal import Decimal, ROUND_DOWN


def get_weekly_repayment_amount(principal, weekly_interest_rate, duration_in_weeks):
    if duration_in_weeks < 1:
        raise Exception('Invalid input!')
    growth_rate = (Decimal('1.0') + weekly_interest_rate)

-   denominator = Decimal('0.0')
-   for t in range(0, duration_in_weeks):
-       denominator += pow(growth_rate, t)
+   denominator = (Decimal('1.0') - pow(growth_rate, duration_in_weeks)) \
+       / (Decimal('1.0') - growth_rate)

    numerator = principal * pow(growth_rate, duration_in_weeks)

    weekly_repayment = numerator/denominator

    return weekly_repayment.quantize(Decimal('.01'), rounding=ROUND_DOWN)
