import unittest
from unittest import TestCase

from decimal import Decimal

from repayment_calculator import get_weekly_repayment_amount


class TestGetWeeklyRepaymentAmountCharacterization(TestCase):
    def test(self):
        duration = 3
        weekly_interest_rate = Decimal('0.05')
        principal = Decimal('1000.00')
        repayment = get_weekly_repayment_amount(principal, weekly_interest_rate, duration)
        self.assertEqual(repayment, '???')

    def test_when_duration_is_zero(self):
        duration = 0
        weekly_interest_rate = Decimal('0.05')
        principal = Decimal('1000.00')
        get_weekly_repayment_amount(principal, weekly_interest_rate, duration)


if __name__ == '__main__':
    unittest.main()
