from insights.tests import InputData, archive_provider, integrate
from demo.rules import selinux_policy_mismatch as rule


SESTATUS_OK = '''
Current mode:                   enforcing
SELinux status:                 enabled
'''.strip()

SESTATUS_DISABLED = '''
Current mode:                   enforcing
SELinux status:                 disabled
'''.strip()

SESTATUS_PERMISSIVE = '''
Current mode:                   permissive
SELinux status:                 enabled
'''.strip()

POLICY_1 = '''
selinux-policy-3.13.1-102.el7_3.13.noarch
'''.strip()

POLICY_2 = '''
selinux-policy-3.14.1-102.el7_3.13.noarch
'''.strip()

POLICY_3 = '''
selinux-policy-3.13.5-106.el7_3.13.noarch
'''.strip()

POLICY_4 = '''
selinux-policy-3.13.5-106.el7_3.18.noarch
'''.strip()

POLICY_TYPE_1 = '''
selinux-policy-{}-3.13.1-102.el7_3.13.noarch
'''.strip()

POLICY_TYPE_2 = '''
selinux-policy-{}-3.14.1-102.el7_3.13.noarch
'''.strip()

POLICY_TYPE_3 = '''
selinux-policy-{}-3.13.5-106.el7_3.13.noarch
'''.strip()

POLICY_TYPE_4 = '''
selinux-policy-targeted-3.13.5-106.el7_3.18.noarch
'''.strip()

SELINUX_CONFIG = '''
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of these three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE={}
'''.strip()

MATCHING = [
    (POLICY_1, POLICY_TYPE_1, 'targeted', 'targeted'),
    (POLICY_2, POLICY_TYPE_2, 'minimum', 'minimum'),
    (POLICY_3, POLICY_TYPE_3, 'targeted', 'targeted'),
    (POLICY_4, POLICY_TYPE_4, 'mls', 'mls'),
]

NON_MATCHING = [
    (POLICY_1, POLICY_TYPE_4, 'targeted', 'targeted'),
    (POLICY_2, POLICY_TYPE_3, 'minimum', 'minimum'),
    (POLICY_3, POLICY_TYPE_2, 'minimum', 'minimum'),
    (POLICY_4, POLICY_TYPE_1, 'targeted', 'targeted'),
]

INVALID = [
    (POLICY_1, POLICY_TYPE_1, 'targeted', 'minimum'),
    (POLICY_2, POLICY_TYPE_2, 'minimum', 'mls'),
    (POLICY_3, POLICY_TYPE_3, 'targeted', 'minimum'),
    (POLICY_4, POLICY_TYPE_4, 'mls', 'minimum'),
]


tests = []


def test_valid_selinux():
    for first, second, policy_type, selinux_type in MATCHING:
        second = second.format(policy_type)
        input_data = InputData()
        input_data.add('sestatus', SESTATUS_OK)
        input_data.add('installed-rpms', first + '\n' + second)
        input_data.add('selinux-config', SELINUX_CONFIG.format(selinux_type))
        response = integrate(input_data, rule)
        assert response == []
        tests.append((input_data, response))


def test_nonmatching_selinux():
    for first, second, policy_type, selinux_type in NON_MATCHING:
        second = second.format(policy_type)
        input_data = InputData()
        input_data.add('sestatus', SESTATUS_OK)
        input_data.add('installed-rpms', first + '\n' + second)
        input_data.add('selinux-config', SELINUX_CONFIG.format(selinux_type))
        response = integrate(input_data, rule)
        assert 'policy_rpm' in response[0]
        assert 'policy_type_rpm' in response[0]
        assert 'policy_type' in response[0]
        assert response[0]['policy_rpm'] == first[:first.rfind('.')]
        assert response[0]['policy_type_rpm'] == second[:second.rfind('.')]
        assert response[0]['policy_type'] == policy_type
        tests.append((input_data, response))


def test_invalid_selinux():
    for first, second, policy_type, selinux_type in INVALID:
        second = second.format(policy_type)
        input_data = InputData()
        input_data.add('sestatus', SESTATUS_OK)
        input_data.add('installed-rpms', first + '\n' + second)
        input_data.add('selinux-config', SELINUX_CONFIG.format(selinux_type))
        response = integrate(input_data, rule)
        assert response == []
        tests.append((input_data, response))


def test_invalid_type():
    for first, second, policy_type, selinux_type in MATCHING + NON_MATCHING + INVALID:
        second = second.format(policy_type)
        input_data = InputData()
        input_data.add('sestatus', SESTATUS_OK)
        input_data.add('installed-rpms', first + '\n' + second)
        input_data.add('selinux-config', '')
        response = integrate(input_data, rule)
        assert response == []
        tests.append((input_data, response))


def test_noselinux():
    for first, second, policy_type, selinux_type in MATCHING + NON_MATCHING + INVALID:
        second = second.format(policy_type)
        input_data = InputData()
        input_data.add('sestatus', SESTATUS_DISABLED)
        input_data.add('installed-rpms', first + '\n' + second)
        input_data.add('selinux-config', SELINUX_CONFIG.format(selinux_type))
        response = integrate(input_data, rule)
        assert response == []
        tests.append((input_data, response))

        input_data = InputData()
        input_data.add('sestatus', SESTATUS_PERMISSIVE)
        input_data.add('installed-rpms', first + '\n' + second)
        input_data.add('selinux-config', SELINUX_CONFIG.format(selinux_type))
        response = integrate(input_data, rule)
        assert response == []
        tests.append((input_data, response))


@archive_provider(rule.report)
def integration_tests():
    test_valid_selinux()
    test_nonmatching_selinux()
    test_invalid_selinux()
    test_invalid_type()
    test_noselinux()
    for inp, out in tests:
        yield inp, out
