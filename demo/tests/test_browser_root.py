from demo.rules import browser_root as rule
from insights.core.plugins import make_response
from insights.tests import InputData, archive_provider
from insights.specs import Specs


ERROR_KEY = 'BROWSER_ROOT'

PS_AUXCWW_LINES = '''
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
postgres 18626  0.0  0.1 617460  4636 ?        Ss   13:59   0:00 postmaster
root     18678  2.8  0.1 100388  3980 ?        Ss   14:01   0:00 sshd
sherr    18681  0.4  0.0 100388  1820 ?        S    14:01   0:00 sshd
sherr    18682  0.6  0.0 108440  1984 pts/0    Ss   14:01   0:00 bash
{0}
sherr    18699  0.0  0.0 110232  1164 pts/0    R+   14:01   0:00 ps
'''.strip()

PS_BAD_1 = 'root 18681  0.4  0.0 100388  1820 ?        S    14:01   0:00 firefox'
PS_BAD_2 = 'root 18681  0.4  0.0 100388  1820 ?        S    14:01   0:00 chrome'
PS_BAD_3 = 'root 18681  0.4  0.0 100388  1820 ?        S    14:01   0:00 chrome-sandbox'
PS_BAD_4 = 'root 18681  0.4  0.0 100388  1820 ?        S    14:01   0:00 chromium-browser'
PS_BAD_5 = PS_BAD_1 + '\n' + PS_BAD_2
PS_BAD_6 = PS_BAD_1 + '\n' + PS_BAD_2 + '\n' + PS_BAD_2
PS_BAD_7 = 'root 18681  0.4  0.0 100388  1820 ?        S    14:01   0:00 chromium-browse'
PS_BAD_8 = PS_BAD_4 + '\n' + PS_BAD_7
PS_GOOD_1 = 'sherr 18681  0.4  0.0 100388  1820 ?        S    14:01   0:00 firefox'
PS_GOOD_2 = 'root 18681  0.4  0.0 100388  1820 ?        S    14:01   0:00 xfsalloc'
PS_MISSING = ''

PS_TESTS = [
    (PS_AUXCWW_LINES.format(PS_BAD_1), make_response(ERROR_KEY, browsers=['firefox'])),
    (PS_AUXCWW_LINES.format(PS_BAD_2), make_response(ERROR_KEY, browsers=['chrome'])),
    (PS_AUXCWW_LINES.format(PS_BAD_3), make_response(ERROR_KEY,
                                                     browsers=['chrome-sandbox'])),
    (PS_AUXCWW_LINES.format(PS_BAD_4), make_response(ERROR_KEY,
                                                     browsers=['chromium-browser'])),
    (PS_AUXCWW_LINES.format(PS_BAD_5), make_response(ERROR_KEY,
                                                     browsers=['chrome', 'firefox'])),
    (PS_AUXCWW_LINES.format(PS_BAD_6), make_response(ERROR_KEY,
                                                     browsers=['chrome', 'firefox'])),
    (PS_AUXCWW_LINES.format(PS_BAD_7), make_response(ERROR_KEY,
                                                     browsers=['chromium-browser'])),
    (PS_AUXCWW_LINES.format(PS_BAD_8), make_response(ERROR_KEY,
                                                     browsers=['chromium-browser'])),
    (PS_AUXCWW_LINES.format(PS_GOOD_1), None),
    (PS_AUXCWW_LINES.format(PS_GOOD_2), None),
    (PS_AUXCWW_LINES.format(PS_MISSING), None),
]


@archive_provider(rule.report)
def integration_tests():
    for i, v in enumerate(PS_TESTS):
        input_value, output_value = v
        yield InputData(i).add(Specs.ps_auxcww, input_value), output_value
