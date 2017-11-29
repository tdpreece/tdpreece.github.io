"""Payment Calculator - legacy code

Assumes that the customer will make equal repayments for a given number of weeks.

Let p_x = principal at time x,
    r = 1 + weekly interest expressed as fraction (e.g. 5% -> 1.05),
    a = amount to repay each week.

Consider a loan repaid in 3 weekly installments:
p_1 = p_0 * r - a       (eq-1)
p_2 = p_1 * r - a       (eq-2)
p_3 = p_2 * r - a       (eq-3)
p_3 = 0                 (eq-4)

substituting eq-1 into eq-2,

p_2 = (p_0 * r - a)r - a  (eq-5)

substituting eq-5 into eq-3,

p_3 = [(p_0 * r - a)r - a] * r] - a

from eq-4,

0 = [(p_0 * r - a)r - a] * r - a

0 = [p_0 * r^2 - a * r -a] * r - a

0 = p_0 * r^3 - a * r^2 -a * r - a

0 = p_0 * r^3 -a * ( 1 + r + r^2)

a = p_0 * r^3 / ( 1 + r + r^2)

For the general case of n installments,

a = p_0 * r^n / [1 + r + r^2 + r^3 + ... + r^(n-1)]

"""
from decimal import Decimal, ROUND_DOWN


def get_weekly_repayment_amount(principal, weekly_interest_rate, duration_in_weeks):
    if duration_in_weeks < 1:
        raise Exception('Invalid input!')
    growth_rate = (Decimal('1.0') + weekly_interest_rate)

    denominator = (Decimal('1.0') - pow(growth_rate, duration_in_weeks + 1)) \
        / (Decimal('1.0') - growth_rate)

    numerator = principal * pow(growth_rate, duration_in_weeks)

    weekly_repayment = numerator/denominator

    return weekly_repayment.quantize(Decimal('.01'), rounding=ROUND_DOWN)
