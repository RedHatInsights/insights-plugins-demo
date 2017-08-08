from demo.rules import high_swap_usage
from insights.core.plugins import make_response
from insights.tests import InputData, archive_provider

SWAP_MEMORY_OK = """
MemTotal:        8062472 kB
MemFree:         5742024 kB
Buffers:           11284 kB
Cached:          1757700 kB
SwapCached:            0 kB
Active:          1107052 kB
Inactive:         895348 kB
Active(anon):     213128 kB
Inactive(anon):    21600 kB
Active(file):     893924 kB
Inactive(file):   873748 kB
Unevictable:           0 kB
Mlocked:               0 kB
SwapTotal:      10305532 kB
SwapFree:       10305532 kB
Dirty:              9852 kB
Writeback:             0 kB
AnonPages:        233568 kB
Mapped:            94344 kB
Shmem:              1160 kB
Slab:             226680 kB
SReclaimable:     197528 kB
SUnreclaim:        29152 kB
KernelStack:        3568 kB
PageTables:        12572 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:    14336768 kB
Committed_AS:     430420 kB
VmallocTotal:   34359738367 kB
VmallocUsed:      159692 kB
VmallocChunk:   34359576196 kB
HardwareCorrupted:     0 kB
AnonHugePages:    165888 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
DirectMap4k:       10240 kB
DirectMap2M:     8378368 kB
"""

SWAP_MEMORY_HIGH_USAGE = """
MemTotal:        3717184 kB
MemFree:           36248 kB
Buffers:           16828 kB
Cached:           296764 kB
SwapCached:       550700 kB
Active:          2721016 kB
Inactive:         823064 kB
Active(anon):    2656440 kB
Inactive(anon):   574192 kB
Active(file):      64576 kB
Inactive(file):   248872 kB
Unevictable:           0 kB
Mlocked:               0 kB
SwapTotal:       4194296 kB
SwapFree:         969012 kB
Dirty:               568 kB
Writeback:             0 kB
AnonPages:       3135780 kB
Mapped:            18524 kB
Shmem:               144 kB
Slab:              79696 kB
SReclaimable:      29460 kB
SUnreclaim:        50236 kB
KernelStack:        1616 kB
PageTables:        15252 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:     6052888 kB
Committed_AS:    1593504 kB
VmallocTotal:   34359738367 kB
VmallocUsed:       17816 kB
VmallocChunk:   34359711028 kB
HardwareCorrupted:     0 kB
AnonHugePages:         0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
DirectMap4k:     3932160 kB
DirectMap2M:           0 kB
"""

NO_SWAP_MEMORY = """
MemTotal:        7539940 kB
MemFree:         2077596 kB
Buffers:          273900 kB
Cached:          3729908 kB
SwapCached:            0 kB
Active:          3319708 kB
Inactive:        1647152 kB
Active(anon):     966748 kB
Inactive(anon):    77972 kB
Active(file):    2352960 kB
Inactive(file):  1569180 kB
Unevictable:           0 kB
Mlocked:               0 kB
SwapTotal:             0 kB
SwapFree:              0 kB
Dirty:             42884 kB
Writeback:             0 kB
AnonPages:        962908 kB
Mapped:           123756 kB
Shmem:             81664 kB
Slab:             398448 kB
SReclaimable:     362456 kB
SUnreclaim:        35992 kB
KernelStack:        3024 kB
PageTables:        30148 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:     3769968 kB
Committed_AS:    2192500 kB
VmallocTotal:   34359738367 kB
VmallocUsed:       26248 kB
VmallocChunk:   34359708596 kB
HardwareCorrupted:     0 kB
AnonHugePages:    555008 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
DirectMap4k:        6144 kB
DirectMap2M:     7858176 kB
"""


@archive_provider(high_swap_usage)
def integration_tests():
    # Test that should pass
    data = InputData("swap_usage_ok")
    data.add('meminfo', SWAP_MEMORY_OK)
    yield data, []

    data = InputData("no_swap_in_use")
    data.add('meminfo', NO_SWAP_MEMORY)
    yield data, []

    # Test that should fail
    data = InputData("swap_usage_high")
    data.add('meminfo', SWAP_MEMORY_HIGH_USAGE)
    # Remember, all values reported by MemInfo are in bytes
    expected = make_response(
        high_swap_usage.ERROR_KEY,
        message=high_swap_usage.ERROR_MESSAGE,
        swap_total=4194296 * 1024,
        swap_free=969012 * 1024,
        swap_cached=550700 * 1024,
    )
    yield data, [expected]
