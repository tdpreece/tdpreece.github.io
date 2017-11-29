from unittest import TestCase
from decimal import Decimal

from approvaltests import verify, verify_all_combinations
from approvaltests.reporters import GenericDiffReporterFactory

from repayment_calculator import get_weekly_repayment_amount


class TestGetWeeklyRepaymentAmountCharacterization(TestCase):
    def test_valid_inputs(self):
        duration = 3
        weekly_interest_rate = Decimal('0.05')
        principal = Decimal('1000.00')
        repayment = get_weekly_repayment_amount(principal, weekly_interest_rate, duration)
        reporter = GenericDiffReporterFactory().get('meld')
        verify(str(repayment), reporter=reporter)

    def test_input_combinations(self):
        principals = (Decimal('100.00'), Decimal('2000.00'), Decimal('3000.00'), )
        interest_rates = (-Decimal('0.01'), Decimal('0.0'), Decimal('0.01'), Decimal('0.05'), Decimal('0.1'), )
        durations = (0, 1, 2, 3, 4, 5, 10, 20, 31, 52, 53)
        reporter = GenericDiffReporterFactory().get('meld')
        verify_all_combinations(
            get_weekly_repayment_amount,
            input_arguments=(principals, interest_rates, durations),
            reporter=reporter
        )
