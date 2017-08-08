"""
Report more than 50% swap memory in use.

Written by Paul Wayper

"""
from insights.core.plugins import make_response, rule
from insights.parsers.meminfo import MemInfo

ERROR_KEY = 'HIGH_SWAP_USAGE'
ERROR_MESSAGE = 'Swap usage over 50%, please check process memory usage'


@rule(requires=[MemInfo])
def high_swap_usage(local, shared):
    """
    Detect swap memory in use, and if the amount of swap free is less than
    half the total, and swap is actually in use (i.e. total swap > 0 Kb),
    then report a problem.
    """
    mem = shared[MemInfo]

    if mem.swap.total == 0:
        return

    # swap.used = swap.free + swap.cached
    # MemInfo reports all memory usage in bytes.
    if float(mem.swap.used) / float(mem.swap.total) > 0.5:
        return make_response(
            ERROR_KEY,
            message=ERROR_MESSAGE,
            swap_total=mem.swap.total,
            swap_free=mem.swap.free,
            swap_cached=mem.swap.cached,
        )
