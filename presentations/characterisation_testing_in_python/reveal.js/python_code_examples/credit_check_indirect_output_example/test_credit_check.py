from unittest import TestCase

from approvaltests import verify_all_combinations
from approvaltests.reporters import GenericDiffReporterFactory
from mock import patch

from credit_check import CREDIT_BUREAU_URL, get_credit_report


class TestGetCreaditReportCharacterization(TestCase):
    def test_address_parsing(self):
        addresses = ('19 Long Lane, London EC1A 9PL', '11 Pilgrim St, London EC4V 6RN',
        '20-22 Great Titchfield Street London W1W 8BE',)

        reporter = GenericDiffReporterFactory().get('meld')
        verify_all_combinations(
            function_under_test, input_arguments=(addresses,), reporter=reporter
        )

def function_under_test(address):
    with patch('credit_check.requests') as m:
        get_credit_report('Tim Preece', address)
        call_args_list = m.get.call_args_list
    return call_args_list
