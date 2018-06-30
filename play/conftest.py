"""
Pytest configuration. Add fixtures and wrappers for all test functions here.
"""
import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
