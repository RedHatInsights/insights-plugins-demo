from demo.rules import rsyslog_dropping_messages
from insights.core.plugins import make_response
from insights.tests import InputData, archive_provider

MESSAGES = """
Jun 15 13:36:36 example ntpd_intres[2719]: host name not found: ntp1.example.com
Jun 15 13:36:36 example ntpd_intres[2719]: host name not found: ntp2.example.com
Jun 15 13:45:17 example puppet-agent[16486]: Finished catalog run in 2.95 seconds
Jun 15 13:45:25 example kernel: type=1400 audit(1434393925.317:3998): avc:  denied  { append } for  pid=16900 comm="ping" path=2F616269776F726B2F646174612F6F70732F6C6F672F7265706F727465722E6C6F672E31202864656C6574656429 dev=dm-8 ino=20989802 scontext=system_u:system_r:ping_t:s0 tcontext=system_u:object_r:file_t:s0 tclass=file
Jun 15 13:52:39 example ntpd_intres[2719]: host name not found: ntp1.example.com
Jun 15 13:52:39 example ntpd_intres[2719]: host name not found: ntp2.example.com
Jun 15 14:00:01 example adclient[2006]: INFO  <fd:20 PAMIsUserAllowedAccess2 > audit User 'auditor' is authorized
Jun 15 14:00:01 example adclient[2006]: INFO  <fd:21 PAMIsUserAllowedAccess2 > audit User 'auditor' is authorized
Jun 15 14:00:01 example adclient[2006]: INFO  <fd:26 PAMIsUserAllowedAccess2 > audit User 'auditor' is authorized
Jun 15 14:00:01 example adclient[2006]: INFO  <fd:10 PAMIsUserAllowedAccess2 > audit User 'auditor' is authorized
"""

MESSAGES_WITH_FEW_DROPS = """
Jun 15 11:19:50 example sshd[25306]: Set /proc/self/oom_score_adj to 0
Jun 15 11:19:51 example sshd[25306]: Connection from 10.2.22.155 port 43873
Jun 15 11:19:51 example sshd[25306]: Postponed gssapi-with-mic for user from 10.2.22.155 port 43873 ssh2 [preauth]
Jun 15 11:19:51 example sshd[25306]: Authorized to user, krb5 principal user@EXAMPLE.COM (krb5_kuserok)
Jun 15 11:19:51 example adclient[2006]: INFO  <fd:10 PAMIsUserAllowedAccess2 > audit User 'user' is authorized
Jun 15 11:19:51 example sshd[25306]: Accepted gssapi-with-mic for user from 10.2.22.155 port 43873 ssh2
Jun 15 11:19:51 example rsyslogd-2177: imuxsock begins to drop messages from pid 25306 due to rate-limiting
Jun 15 11:19:51 example sshd[25308]: subsystem request for sftp by user user
Jun 15 11:19:59 example sshd[25308]: Received disconnect from 10.2.22.155: 11: disconnected by user
Jun 15 11:19:59 example rsyslogd-2177: imuxsock lost 12 messages from pid 25306 due to rate-limiting
Jun 15 11:20:27 example kernel: type=1400 audit(1434385227.015:3984): avc:  denied  { append } for  pid=26168 comm="ping" path=2F616269776F726B2F646174612F6F70732F6C6F672F7265706F727465722E6C6F672E31202864656C6574656429 dev=dm-8 ino=20989802 scontext=system_u:system_r:ping_t:s0 tcontext=system_u:object_r:file_t:s0 tclass=file
Jun 15 11:20:27 example kernel: type=1400 audit(1434385227.015:3985): avc:  denied  { read write } for  pid=26168 comm="ping" path="/abiwork/data/ops/reporter.pid" dev=dm-8 ino=20978602 scontext=system_u:system_r:ping_t:s0 tcontext=system_u:object_r:file_t:s0 tclass=file
Jun 15 11:20:36 example sshd[26399]: Set /proc/self/oom_score_adj to 0
Jun 15 11:20:36 example sshd[26399]: Connection from 10.2.22.183 port 42357
Jun 15 11:20:36 example sshd[26399]: Authorized to user, krb5 principal user@EXAMPLE.COM (krb5_kuserok)
Jun 15 11:20:36 example adclient[2006]: INFO  <fd:10 PAMIsUserAllowedAccess2 > audit User 'user' is authorized
Jun 15 12:48:49 example sshd[19922]: Accepted gssapi-with-mic for user from 10.2.22.155 port 45847 ssh2
Jun 15 12:48:49 example rsyslogd-2177: imuxsock begins to drop messages from pid 19922 due to rate-limiting
Jun 15 12:48:49 example sshd[19927]: subsystem request for sftp by user user
Jun 15 12:48:55 example sshd[19927]: Received disconnect from 10.2.22.155: 11: disconnected by user
Jun 15 12:48:55 example rsyslogd-2177: imuxsock lost 11 messages from pid 19922 due to rate-limiting
Jun 15 12:56:04 example adclient[2006]: INFO  <bg:bindingRefresh> base.bind.healing Lost connection to ldap2.example.com(GC). Running in disconnected mode: unlatch
Jun 15 12:56:04 example adclient[2006]: INFO  <bg:bindingRefresh> base.bind.healing Reconnected to ldap2.example.com(GC).  Running in connected mode.
Jun 15 13:00:01 example root: I am Alive
"""

MESSAGES_WITH_MANY_DROPS = """
Mar 27 03:18:15 arqopasp35 rsyslogd: [origin software="rsyslogd" swVersion="5.8.10" x-pid="1870" x-info="http://www.rsys
log.com"] rsyslogd was HUPed
Mar 27 03:18:16 arqopasp35 rsyslogd-2177: imuxsock lost 241 messages from pid 55082 due to rate-limiting
Mar 27 03:18:19 arqopasp35 rsyslogd-2177: imuxsock begins to drop messages from pid 55082 due to rate-limiting
Mar 27 03:18:21 arqopasp35 pulp: pulp.server.db.connection:INFO: Attempting Database connection with seeds = localhost:27017
Mar 27 03:18:21 arqopasp35 pulp: pulp.server.db.connection:INFO: Connection Arguments: {'max_pool_size': 10}
Mar 27 03:18:21 arqopasp35 pulp: pulp.server.db.connection:INFO: Database connection established with: seeds = localhost:27017, name = pulp_database
Mar 27 03:18:22 arqopasp35 rsyslogd-2177: imuxsock lost 245 messages from pid 55082 due to rate-limiting
Mar 27 03:18:25 arqopasp35 rsyslogd-2177: imuxsock begins to drop messages from pid 55082 due to rate-limiting
Mar 27 03:18:25 arqopasp35 pulp: pulp.server.db.connection:INFO: Attempting Database connection with seeds = localhost:27017
Mar 27 03:18:25 arqopasp35 pulp: pulp.server.db.connection:INFO: Connection Arguments: {'max_pool_size': 10}
Mar 27 03:18:25 arqopasp35 pulp: pulp.server.db.connection:INFO: Database connection established with: seeds = localhost:27017, name = pulp_database
Mar 27 03:18:26 arqopasp35 pulp: pulp.plugins.loader.manager:INFO: Loaded plugin yum_clone_distributor for types: rpm,srpm,drpm,erratum,distribution,package_category,package_group
Mar 27 03:18:27 arqopasp35 pulp: pulp.plugins.loader.manager:INFO: Loaded plugin nodes_http_distributor for types: node
Mar 27 03:18:27 arqopasp35 puppet-master[48226]: Starting Puppet master version 3.6.2
Mar 27 03:18:27 arqopasp35 pulp: pulp.plugins.loader.manager:INFO: Loaded plugin puppet_distributor for types: puppet_module
Mar 27 03:18:27 arqopasp35 pulp: pulp.plugins.loader.manager:INFO: Loaded plugin puppet_file_distributor for types: puppet_module
Mar 27 03:18:27 arqopasp35 pulp: pulp.plugins.loader.manager:INFO: Loaded plugin puppet_install_distributor for types: puppet_module
Mar 27 03:18:28 arqopasp35 rsyslogd-2177: imuxsock lost 239 messages from pid 55082 due to rate-limiting
Mar 27 03:18:28 arqopasp35 pulp: pulp.plugins.loader.manager:INFO: Loaded plugin yum_distributor for types: rpm,srpm,drpm,erratum,package_group,package_category,distribution,yum_repo_metadata_file
Mar 27 03:18:28 arqopasp35 pulp: pulp.plugins.loader.manager:INFO: Loaded plugin export_distributor for types: rpm,srpm,drpm,erratum,distribution,package_category,package_group
Mar 27 03:18:28 arqopasp35 pulp: pulp.plugins.loader.manager:INFO: Loaded plugin iso_distributor for types: iso
Mar 27 03:18:28 arqopasp35 pulp: pulp.plugins.loader.manager:INFO: Loaded plugin group_export_distributor for types: rpm,srpm,drpm,erratum,distribution,package_category,package_group
"""


RSYSLOG_CONF_DEFAULT_LIMITS = """
:fromhost-ip, regex, "10.0.0.[0-9]" /tmp/my_syslog.log
$ModLoad imtcp
$InputTCPServerRun 10514
$template SpiceTmpl,"%TIMESTAMP%.%TIMESTAMP:::date-subseconds% %syslogtag% %syslogseverity-text%:%msg:::sp-if-no-1st-sp%%msg:::drop-last-lf%\\n"
$WorkDirectory /var/opt/rsyslog # where to place spool files
"""


RSYSLOG_CONF_LOW_BURST = """
:fromhost-ip, regex, "10.0.0.[0-9]" /tmp/my_syslog.log
$ModLoad imtcp
$SystemLogRateLimitBurst 10
"""


@archive_provider(rsyslog_dropping_messages.rsyslog_dropping_messages)
def integration_tests():
    # Test that should pass
    data = InputData("good_test_1")
    data.add('messages', MESSAGES)
    data.add('rsyslog.conf', RSYSLOG_CONF_DEFAULT_LIMITS)
    yield data, []

    data = InputData("good_test_2")
    data.add('messages', MESSAGES_WITH_FEW_DROPS)
    data.add('rsyslog.conf', RSYSLOG_CONF_DEFAULT_LIMITS)
    yield data, []

    # Test that should fail
    data = InputData("bad_default_limit_high_drops")
    data.add('messages', MESSAGES_WITH_MANY_DROPS)
    data.add('rsyslog.conf', RSYSLOG_CONF_DEFAULT_LIMITS)
    expected = make_response(
        rsyslog_dropping_messages.ERROR_KEY,
        drops_by_process={'55082': {'count': 725, 'max': 245, 'lines': 3}},
        current_interval=5,
        current_limit=200,
        new_limit=245,
        new_config="$SysLogRateLimitBurst {m}".format(m=245),
    )
    yield data, [expected]

    data = InputData("bad_low_limit_high_drops")
    data.add('messages', MESSAGES_WITH_MANY_DROPS)
    data.add('rsyslog.conf', RSYSLOG_CONF_LOW_BURST)
    expected = make_response(
        rsyslog_dropping_messages.ERROR_KEY,
        drops_by_process={'55082': {'count': 725, 'max': 245, 'lines': 3}},
        current_interval=5,
        current_limit=10,
        new_limit=245,
        new_config="$SysLogRateLimitBurst {m}".format(m=245),
    )
    yield data, [expected]

    data = InputData("bad_low_limit_few_drops")
    data.add('messages', MESSAGES_WITH_FEW_DROPS)
    data.add('rsyslog.conf', RSYSLOG_CONF_LOW_BURST)
    expected = make_response(
        rsyslog_dropping_messages.ERROR_KEY,
        drops_by_process={'sshd': {'count': 23, 'max': 12, 'lines': 2}},
        current_interval=5,
        current_limit=10,
        new_limit=12,
        new_config="$SysLogRateLimitBurst {m}".format(m=12),
    )
    yield data, [expected]
