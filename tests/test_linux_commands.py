import string

import pytest
import logging
from datetime import datetime

logging.getLogger()


def test_logon_period(tests_client, data):
    logon_period = datetime.fromisoformat(data.current_date) - datetime.fromisoformat(data.last_login)
    assert logon_period.days <= 365, F"time from last login is more than a year: {logon_period.days}"


def test_is_sata(data):
    assert data.disk_type.lower() == 'sata', F"disk is: {data.disk_type}"


param_data = [(letter, 'valid') for letter in string.ascii_uppercase + string.ascii_lowercase]


# a parameterized test - the easier way
@pytest.mark.slow
@pytest.mark.parametrize("param, expected", param_data)
def test_cat_options1(param, expected, tests_client):
    logging.info(F"running test_cat_options with 'cat -{param}")
    res = tests_client.get_cmd_output(F"cat -{param} test")
    test_result = 'invalid' if 'invalid' in res else 'valid'
    assert test_result == expected, F"cat option -{param} is not {expected}"


# a parameterized test - while using a json input conf file
@pytest.mark.slow
def test_cat_options2(tests_client, test_data):
    logging.info(F"running test_cat_options with 'cat {test_data['cat option']}")
    res = tests_client.get_cmd_output(F"cat {test_data['cat option']} test")
    test_result = 'invalid' if 'invalid' in res else 'valid'
    assert test_data['expected'] == test_result, F"cat option {test_data['cat option']} is not valid"


