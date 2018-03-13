from demo.rules import localhost_in_hosts
from insights.core.plugins import make_response
from insights.tests import InputData, archive_provider
from insights.specs import Specs

HOSTS_WITH_LOCALHOST = """
127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4
::1 localhost localhost.localdomain localhost6 localhost6.localdomain6
# The same IP address can appear more than once, with different names
127.0.0.1 fte.example.com

10.0.0.1 nonlocal.example.com nonlocal2.fte.example.com
10.0.0.2 other.host.example.com # Comments at end of line are ignored
"""

HOSTS_WITHOUT_LOCALHOST = """
# The hosts file can define 127.0.0.1 as a name, but this is not localhost
127.0.0.1 fte.example.com

10.0.0.1 nonlocal.example.com nonlocal2.fte.example.com
"""


@archive_provider(localhost_in_hosts.localhost_in_hosts)
def integration_tests():
    # Test that should pass
    data = InputData("localhost_in_hosts")
    data.add(Specs.hosts, HOSTS_WITH_LOCALHOST)
    yield data, None

    # Test that should fail
    data = InputData("localhost_not_in_hosts")
    data.add(Specs.hosts, HOSTS_WITHOUT_LOCALHOST)
    expected = make_response(
        localhost_in_hosts.ERROR_KEY,
        message=localhost_in_hosts.MESSAGE,
        hosts_defined=set({'fte.example.com', 'nonlocal.example.com',
                           'nonlocal2.fte.example.com'})
    )
    yield data, expected
