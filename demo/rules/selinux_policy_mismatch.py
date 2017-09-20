"""
SELinux policy mismatch
=======================
If SELinux is used and in enforcing mode, then 'selinux-policy' RPM version should match
'selinux-policy-X' RPM version where X is used SELinux type.

It is possible to force updates on either of 'selinux-policy' and 'selinux-policy-X' packages,
and have their versions in inconsistent state. That would make SELinux act in an unexpected way.

Written by Stanislav Kontar
"""

from insights import make_response, rule
from insights.parsers.installed_rpms import InstalledRpms
from insights.parsers.selinux_config import SelinuxConfig
from insights.parsers.sestatus import SEStatus

ERROR_KEY = 'SELINUX_POLICY_MISMATCH'


@rule(requires=[SEStatus, SelinuxConfig, InstalledRpms])
def report(local, shared):
    selinux_enabled = shared[SEStatus].data['selinux_status'] == 'enabled'
    selinux_enforcing = shared[SEStatus].data['current_mode'] == 'enforcing'
    selinux_type = shared[SelinuxConfig].data.get('SELINUXTYPE')

    if selinux_type is None:
        return

    policy_rpm = shared[InstalledRpms].get_max('selinux-policy')
    policy_type_rpm = shared[InstalledRpms].get_max('selinux-policy-{}'.format(selinux_type))

    if policy_rpm is None or policy_type_rpm is None:
        return

    mismatching_policies = (policy_rpm.version != policy_type_rpm.version or
                            policy_rpm.release != policy_type_rpm.release)

    if selinux_enabled and selinux_enforcing and mismatching_policies:
        return make_response(ERROR_KEY,
                             policy_rpm=policy_rpm.nvr,
                             policy_type_rpm=policy_type_rpm.nvr,
                             policy_type=selinux_type)
