from insights.tests import integration, integrate
import pytest


def test_integration(module, comparison_func, input_data, expected):
    actual = integrate(input_data, module)
    comparison_func(actual, expected)


def pytest_generate_tests(metafunc):
    pattern = pytest.config.getoption("-k")
    integration.generate_tests(metafunc, test_integration, "demo.tests", pattern=pattern)
