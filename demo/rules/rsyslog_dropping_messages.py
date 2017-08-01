"""
Is rsyslog dropping messages?  If so, inform the user over what time, how
many messages, and what processes are being dropped.  Then recommend a
setting for the SystemLogRateLimitBurst that would allow it to cope with this
many messages at once.

Written by Paul Wayper

"""
from insights.core.plugins import make_response, rule
from insights.parsers.messages import Messages
from insights.parsers.rsyslog_conf import RsyslogConf

import re

ERROR_KEY = 'RSYSLOG_DROPPING_MESSAGES'


def find_dropped_messages(log):
    """
    This is called as a scanner in Messages, rather than a condition.

    We collect two things: the process names corresponding to their IDs, and
    the drop messages for statistical tallying.
    """
    process_name_of = {}
    drops_by_process = {}
    # Jun 15 13:52:39 example ntpd_intres[2719]: host name not found: ntp2.example.com
    proc_re = re.compile(r'(?P<pname>\w+)\[(?P<pid>\d+)\]:')
    # Jun 15 11:19:59 example rsyslogd-2177: imuxsock lost 1 messages from pid 25306 due to rate-limiting
    limit_re = re.compile(r'imuxsock lost (?P<count>\d+) messages from pid (?P<pid>\d+) due to rate-limiting')
    for line in log.lines:
        parts = line.split(None, 5)
        if len(parts) < 6:
            continue
        dropmatch = limit_re.search(parts[5])
        if dropmatch:
            pid, count = dropmatch.group('pid', 'count')
            # Try to match the process by name, but fall back to PID.  We
            # may not have seen a line with this process name yet.
            pname = process_name_of.get(pid, pid)
            if pname not in drops_by_process:
                drops_by_process[pname] = {'count': 0, 'lines': 0, 'max': 0}
            count = int(count)
            drops_by_process[pname]['count'] += count
            drops_by_process[pname]['lines'] += 1
            if drops_by_process[pname]['max'] < count:
                drops_by_process[pname]['max'] = count
        procmatch = proc_re.search(parts[4])
        if procmatch:
            pid, name = procmatch.group('pid', 'pname')
            process_name_of[pid] = name
            # Maybe this PID has already been dropped before we knew its name?
            # If so, move the tallies across or merge the two tallies together.
            # E.g. sshd starts up new processes but we want to account for all
            # the sshd messages being dropped.  Likewise, sometimes the log
            # might start after the process has finished logging, so we get
            # the drop message before we've had a chance to resolve the PID
            # to a name.
            if pid in drops_by_process:
                if name in drops_by_process:
                    # Merge
                    drops_by_process[name]['count'] += drops_by_process[pid]['count']
                    drops_by_process[name]['lines'] += drops_by_process[pid]['lines']
                    if drops_by_process[name]['max'] < drops_by_process[pid]['max']:
                        drops_by_process[name]['max'] = drops_by_process[pid]['max']
                else:
                    # Move
                    drops_by_process[name] = drops_by_process[pid]
                # Remove record based on process ID
                del drops_by_process[pid]
    return drops_by_process


Messages.scan('dropped_messages', find_dropped_messages)


def find_rate_limiting_params(conf):
    """
    Try to determine the 'SystemLogRateLimitInterval' and
    'SystemLogRateLimitBurst' parameters.  They default to 5 seconds for the
    interval and 200 messages for the burst rate.
    """
    if hasattr(conf, 'config_items') and hasattr(conf, 'config_val'):
        # New style RsyslogConf object - get data directly
        print "Burst:", conf.config_val('SystemLogRateLimitBurst', '200')
        return (
            int(conf.config_val('SystemLogRateLimitInterval', '5')),
            int(conf.config_val('SystemLogRateLimitBurst', '200'))
        )

    # Old style RsyslogConf object - search through the lines
    conf_re = re.compile(r'\$(?P<param>SystemLogRateLimit(?:Interval|Burst))\s+(?P<value>\d+)')
    config_vals = {}
    for line in conf.data:
        match = conf_re.search(line)
        if match:
            config_vals[match.group('param')] = match.group('value')
    return (
        int(config_vals.get('SystemLogRateLimitInterval', '5')),
        int(config_vals.get('SystemLogRateLimitBurst', '200'))
    )


@rule(requires=[Messages, RsyslogConf])
def rsyslog_dropping_messages(local, shared):
    """
    Use the file_dropped_messages scan to pick up if any
    """
    msgs = shared[Messages]
    drops_by_process = msgs.dropped_messages
    print "got drops:", drops_by_process

    # If we have an empty dict, because no messages were dropped, skip out now.
    if not drops_by_process:
        return

    # Try to determine the defaults for rate limiting from the configuration
    # file
    interval, limit = find_rate_limiting_params(shared[RsyslogConf])
    max_burst = max(p['max'] for p in drops_by_process.values())
    print "max_burst:", max_burst, "limit:", limit
    if max_burst <= limit:
        # Simple logic - do not recommend reducing the burst lines
        return

    return make_response(
        ERROR_KEY,
        drops_by_process=drops_by_process,
        current_interval=interval,
        current_limit=limit,
        new_limit=max_burst,
        new_config="$SysLogRateLimitBurst {m}".format(m=max_burst),
    )
