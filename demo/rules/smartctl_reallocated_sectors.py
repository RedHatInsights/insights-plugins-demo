"""
Detect Reallocated Sectors above zero in `smartctl -a` output.

Written by Paul Wayper

"""
from insights.core.plugins import make_response, rule
from insights.parsers.smartctl import SMARTctl

ERROR_KEY = 'SMARTCTL_REALLOCATED_SECTORS'


@rule(requires=[SMARTctl])
def smartctl_reallocated_sectors(local, shared):
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
    for drive in shared[SMARTctl]:
        if 'Reallocated_Sector_Ct' not in drive.attributes:
            return

        realloc_sector_ct = drive.attributes['Reallocated_Sector_Ct']['raw_value']
        if not realloc_sector_ct.isdigit():
            # We don't know what to do if this isn't a number.
            return
        if int(realloc_sector_ct) > 0:
            return make_response(
                ERROR_KEY,
                device=drive.device,
                reallocated_sectors=int(realloc_sector_ct)
            )
