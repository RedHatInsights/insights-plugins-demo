"""
Test whether 'localhost' is defined in the /etc/hosts file.

By default the ``/etc/hosts`` file defines 'localhost' and variants thereof.
Many programs expect this to resolve, and if it is not in 127.0.0.0/8 for
IPv4 or equal to ::1 for IPv6, the system may have problems.

Written by Paul Wayper
"""
from insights.core.plugins import make_response, rule
from insights.parsers.hosts import Hosts

ERROR_KEY = 'LOCALHOST_IN_HOSTS'
MESSAGE = 'localhost not found in /etc/hosts'


@rule(requires=[Hosts])
def localhost_in_hosts(local, shared):
    """
    If 'localhost' is not in the set of host names, then inform the user.
    """
    hosts = shared[Hosts]

    if 'localhost' not in hosts.all_names:
        return make_response(
            ERROR_KEY,
            message=MESSAGE,
            hosts_defined=hosts.all_names,
        )
