"""
Detect Reallocated Sectors above zero in `smartctl -a` output.

Written by Paul Wayper

"""
from insights.core.plugins import make_response, rule
from insights.parsers.smartctl import SMARTctl

ERROR_KEY = 'SMARTCTL_REALLOCATED_SECTORS'
MESSAGE = 'Drives reporting reallocated sectors - the drives may fail soon'


@rule([SMARTctl])
def smartctl_reallocated_sectors(smart_data):
    """
    Report problems if the device has an Attributes section (SAN devices
    don't, for example), and the Reallocated Sector Count raw value is
    greater than zero.  The 'Attributes' property is always a dictionary, so
    we can just check for whether the drive reports a reallocated sector
    count.
    """
    # The shared data from the SMARTctl parser is a list of devices, because
    # the spec is based on the combination of a CommandSpec that uses a
    # matched pattern, and a PatternSpec.  Both of these reeturn multiple
    # drive information objects in a list, so we have to iterate across that:
    drive_data = {}
    for drive in smart_data:
        if 'Reallocated_Sector_Ct' not in drive.attributes:
            continue

        realloc_sector_ct = drive.attributes['Reallocated_Sector_Ct']['raw_value']
        if not realloc_sector_ct.isdigit():
            # We don't know what to do if this isn't a number.
            continue
        if int(realloc_sector_ct) > 0:
            drive_data[drive.device] == int(realloc_sector_ct)

    if drive_data:
        return make_response(
            ERROR_KEY,
            message=MESSAGE,
            drive_data=drive_data,
        )
