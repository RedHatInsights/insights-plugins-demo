from demo.rules import check_rpmnew_files
from insights.core.plugins import make_response
from insights.tests import InputData, archive_provider
from insights.specs import Specs

DIR_HEADER = """
/etc:
total 2404
""".strip()

GOOD_TEST_CONTENT = """
drwxr-xr-x.  3 root root     4096 Mar 23 09:22 abrt
-rw-r--r--.  1 root root       16 Apr 15  2015 adjtime
-rw-r--r--.  1 root root     1518 Jun  8  2013 aliases
-rw-r--r--.  1 root root    12288 Mar 23 10:03 aliases.db
drwxr-xr-x.  2 root root     4096 Mar 23 09:21 alsa
drwxr-xr-x.  2 root root     4096 May  4 09:48 alternatives
-rw-------.  1 root root      541 Feb 24  2016 anacrontab
""".strip()

BAD_TEST_CONTENT = """
-rw-r--r--.  1 root root      348 Dec 10 01:48 koji.conf
drwxr-xr-x.  2 root root     4096 Dec 10 01:48 koji.conf.d
-rw-r--r--.  1 root root      771 Aug 26  2010 krb5.conf
drwxr-xr-x.  2 root root     4096 Nov  3  2016 krb5.conf.d
-rw-r--r--.  1 root root      590 Nov  3  2016 krb5.conf.rpmnew
-rw-r--r--.  1 root root     1128 Apr 29  2016 kshrc
-rw-r--r--.  1 root root      478 Mar 24 16:37 ksmtuned.conf
-rw-r--r--.  1 root root   145665 May 10 13:58 ld.so.cache
-rw-r--r--.  1 root root       28 Feb 28  2013 ld.so.conf
""".strip()


@archive_provider(check_rpmnew_files.check_rpmnew_files)
def integration_tests():
    # Test that should pass
    data = InputData("good_test_1")
    data.add(Specs.ls_etc, DIR_HEADER + GOOD_TEST_CONTENT)
    yield data, None

    # Test that should fail
    data = InputData("bad_test_1")
    data.add(Specs.ls_etc, DIR_HEADER + BAD_TEST_CONTENT)
    expected = make_response(
        check_rpmnew_files.ERROR_KEY,
        files=[{
            'rpmnew_file': 'krb5.conf.rpmnew',
            'rpmnew_date': 'Nov  3  2016',
            'rpmnew_size': 590,
            'original_file': 'krb5.conf',
            'original_date': 'Aug 26  2010',
            'original_size': 771,
        }]
    )
    yield data, expected
