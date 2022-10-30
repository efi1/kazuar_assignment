"""Shared fixtures."""
import json
import os
from pathlib import Path # being used in func: pytest_addoption
from pytest import fixture
from tests import settings
from src.utils.utils import dict_to_obj
import src.utils.create_json_data as create_json_data
from src.clients.tests_client import TestsClient

settings_items = [i for i in settings.__dir__() if not i.startswith('_')]
test_cat_options_path = eval(settings.params_test_path)


def pytest_addoption(parser):
    for item in settings_items:
        try:
            value = eval(getattr(settings, item))
        except (SyntaxError, NameError, TypeError, ZeroDivisionError):
            value = getattr(settings, item)
        parser.addoption(F"--{item}", action='store', default=value)


@fixture(scope="session")
def tests_data(request):
    data = dict()
    for item in settings_items:
        data[item] = request.config.getoption(F"--{item}")
    return dict_to_obj(data)


@fixture(scope="session")
def tests_client(tests_data):
    tests_client = TestsClient(tests_data)
    tests_client.open_page
    yield tests_client
    tests_client.client_tear_down


def del_json_file(tests_data):
    if os.path.exists(tests_data.target_file):
        os.remove(tests_data.target_file)


def load_json_data(tests_data):
    with open(tests_data.target_file) as file:
        data = json.loads(file.read())
    return dict_to_obj(data)


@fixture(scope="session")
def data(tests_client, tests_data):
    del_json_file(tests_data)
    create_json_data.create_json_data(tests_client, tests_data)
    return load_json_data(tests_data)


def load_test_params(path):
    with open(path) as file:
        data = json.loads(file.read())
    return data


@fixture(params=load_test_params(test_cat_options_path))
def test_data(request):
    data = request.param
    return data





