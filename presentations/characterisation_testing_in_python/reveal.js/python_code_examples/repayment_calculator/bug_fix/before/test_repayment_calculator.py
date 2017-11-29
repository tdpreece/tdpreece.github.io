import unittest
from unittest import TestCase
from decimal import Decimal

from approvaltests import verify_all_combinations
from approvaltests.reporters import GenericDiffReporterFactory

from repayment_calculator import get_weekly_repayment_amount


class TestGetWeeklyRepaymentAmountCharacterization(TestCase):

    def test_input_combinations_for_positive_interest_rates(self):
        principals = (Decimal('100.00'), Decimal('2000.00'), Decimal('3000.00'), )
        interest_rates = (Decimal('0.01'), Decimal('0.05'), Decimal('0.1'), )
        durations = (0, 1, 2, 3, 4, 5, 10, 20, 31, 52, 53)
        reporter = GenericDiffReporterFactory().get('meld')
        verify_all_combinations(
            get_weekly_repayment_amount,
            input_arguments=(principals, interest_rates, durations),
            reporter=reporter
        )


if __name__ == "__main__":
    unittest.main()
