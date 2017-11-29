import re

import requests

CREDIT_BUREAU_URL = 'https://credit-bureau-example.com/credit-report/'


def get_credit_report(full_name, address):
    pattern = (
        r'^\s*(?P<house_number>\d+).*'
        r'(?P<postcode>([a-zA-Z]{1,2}\d[a-zA-Z]) \d[a-zA-Z]{2})\s*$'
    )
    matches = re.match(pattern, address)
    params = {
        'name': full_name,
        'house_number': matches.group('house_number'),
        'postcode': matches.group('postcode')
    }
    response = requests.get(CREDIT_BUREAU_URL, params=params)
    return response.content
