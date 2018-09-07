"""
Pytest configuration. Add fixtures and wrappers for all test functions here.
"""
import pytest
import django
from django.conf import settings


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


def pytest_configure():
    settings.DEBUG = False
    django.setup()
