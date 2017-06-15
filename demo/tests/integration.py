from insights.tests import integration
import pytest


def test_integration(module, test_func, input_data, expected):
    integration.integration_test(module, test_func, input_data, expected)


def pytest_generate_tests(metafunc):
    pattern = pytest.config.getoption("-k")
    integration.generate_tests(metafunc, test_integration, "demo.tests", pattern=pattern)
