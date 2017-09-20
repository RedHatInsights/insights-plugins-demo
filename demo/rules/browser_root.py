"""
Web browser running as root user
================================
Web browsers should not be running as the root user. There's not a good reason to do it, and it
increases how dangerous browser / plugin flaws are.

Written by Stanislav Kontar
"""

from insights.core.plugins import make_response, rule, condition
from insights.parsers.ps import PsAuxcww

ERROR_KEY = 'BROWSER_ROOT'

# ps auxcww has a 15-char limit for process name. Check both 'chromium-browse' and
# 'chromium-browser' to be sure
CHECKED_BROWSERS = frozenset(['firefox', 'chrome', 'chrome-sandbox',
                              'chromium-browser', 'chromium-browse'])


@condition(requires=[PsAuxcww])
def check_running_browsers(local, shared):
    """
    Returns list of running browser processes.
    """
    return [p for p in shared[PsAuxcww] if p["COMMAND"] in CHECKED_BROWSERS]


@rule(requires=[check_running_browsers])
def check_services_running(local, shared):
    """
    Collect all running browser processes, if any of them is ran by root user, issue warning.
    """
    running_browsers = shared[check_running_browsers]
    running_browsers_as_root = set(p["COMMAND"] for p in running_browsers if p["USER"] == "root")

    if 'chromium-browse' in running_browsers_as_root:
        # ps auxcww has a 15-char limit for process name. Convert
        # 'chromium-browse' to 'chromium-browser' just in case.
        running_browsers_as_root.remove('chromium-browse')
        running_browsers_as_root.add('chromium-browser')

    if running_browsers_as_root:
        return make_response(ERROR_KEY, browsers=sorted(running_browsers_as_root))
