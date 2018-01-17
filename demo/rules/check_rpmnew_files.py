"""
Find files with the 'rpmnew' extension in the /etc directory and suggest to
the user that they check and remove them.

Written by Paul Wayper

"""
from insights.core.plugins import make_response, rule
from insights.parsers.ls_etc import LsEtc

ERROR_KEY = 'CHECK_RPMNEW_FILES'


@rule([LsEtc])
def check_rpmnew_files(etc):
    """
    Find all files that end with '.rpmnew'.  Then check to see if they have
    an equivalent file without the '.rpmnew' extension.  Record the size and
    date of each pair.  Report any found.
    """
    rpmnew_files = []
    for f in etc.files_of('/etc'):
        if not f.endswith('.rpmnew'):
            continue
        orig_name = f[:-7]  # remove .rpmnew
        # Ignore missing?  Or should we warn?
        if not etc.dir_contains('/etc', orig_name):
            continue
        rpmnew_file = etc.dir_entry('/etc', f)
        orig_file = etc.dir_entry('/etc', orig_name)
        rpmnew_files.append({
            'rpmnew_file': f,
            'rpmnew_date': rpmnew_file['date'],
            'rpmnew_size': rpmnew_file['size'],
            'original_file': orig_name,
            'original_date': orig_file['date'],
            'original_size': orig_file['size'],
        })

    if rpmnew_files:
        return make_response(
            ERROR_KEY,
            files=rpmnew_files
        )
