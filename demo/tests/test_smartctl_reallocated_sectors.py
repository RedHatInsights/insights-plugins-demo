from demo.rules import smartctl_reallocated_sectors
from insights.core.plugins import make_response
from insights.tests import InputData, archive_provider

GOOD_TEST_CONTENT = """
smartctl 5.43 2012-06-30 r3573 [x86_64-linux-2.6.32-642.3.1.el6.x86_64] (local build)
Copyright (C) 2002-12 by Bruce Allen, http://smartmontools.sourceforge.net

=== START OF INFORMATION SECTION ===
Device Model:     INTEL SSDSC2BB120G6R
Serial Number:    PHWA605500GM120CGN
LU WWN Device Id: 5 5cd2e4 04c6fd620
Firmware Version: G201DL29
User Capacity:    120,034,123,776 bytes [120 GB]
Sector Sizes:     512 bytes logical, 4096 bytes physical
Device is:        Not in smartctl database [for details use: -P showall]
ATA Version is:   8
ATA Standard is:  ACS-3 (unknown minor revision code: 0x006d)
Local Time is:    Mon Jan 23 18:36:44 2017 GMT
SMART support is: Available - device has SMART capability.
SMART support is: Enabled

=== START OF READ SMART DATA SECTION ===
SMART overall-health self-assessment test result: PASSED

General SMART Values:
Offline data collection status:  (0x02) Offline data collection activity
                                        was completed without error.
                                        Auto Offline Data Collection: Disabled.
Self-test execution status:      (   0) The previous self-test routine completed
                                        without error or no self-test has ever
                                        been run.
Total time to complete Offline
data collection:                (    2) seconds.
Offline data collection
capabilities:                    (0x79) SMART execute Offline immediate.
                                        No Auto Offline data collection support.
                                        Suspend Offline collection upon new
                                        command.
                                        Offline surface scan supported.
                                        Self-test supported.
                                        Conveyance Self-test supported.
                                        Selective Self-test supported.
SMART capabilities:            (0x0003) Saves SMART data before entering
                                        power-saving mode.
                                        Supports SMART auto save timer.
Error logging capability:        (0x01) Error logging supported.
                                        General Purpose Logging supported.
Short self-test routine
recommended polling time:        (   1) minutes.
Extended self-test routine
recommended polling time:        (  60) minutes.
Conveyance self-test routine
recommended polling time:        (  60) minutes.
SCT capabilities:              (0x003d) SCT Status supported.
                                        SCT Error Recovery Control supported.
                                        SCT Feature Control supported.
                                        SCT Data Table supported.

SMART Attributes Data Structure revision number: 1
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x000e   130   130   039    Old_age   Always       -       4294967295
  5 Reallocated_Sector_Ct   0x0033   100   100   001    Pre-fail  Always       -       0
  9 Power_On_Hours          0x0032   100   100   000    Old_age   Always       -       4828
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       4003
 13 Read_Soft_Error_Rate    0x001e   113   100   000    Old_age   Always       -       1069446856703
179 Used_Rsvd_Blk_Cnt_Tot   0x0033   100   100   010    Pre-fail  Always       -       0
180 Unused_Rsvd_Blk_Cnt_Tot 0x0032   100   100   000    Old_age   Always       -       3206
181 Program_Fail_Cnt_Total  0x003a   100   100   000    Old_age   Always       -       0
182 Erase_Fail_Count_Total  0x003a   100   100   000    Old_age   Always       -       0
184 End-to-End_Error        0x0032   100   100   000    Old_age   Always       -       0
194 Temperature_Celsius     0x0022   100   100   000    Old_age   Always       -       30
195 Hardware_ECC_Recovered  0x0032   100   100   000    Old_age   Always       -       0
198 Offline_Uncorrectable   0x0010   100   100   000    Old_age   Offline      -       0
199 UDMA_CRC_Error_Count    0x003e   100   100   000    Old_age   Always       -       0
201 Soft_Read_Error_Rate    0x0033   100   100   010    Pre-fail  Always       -       124788806046
202 Data_Address_Mark_Errs  0x0027   100   100   000    Pre-fail  Always       -       0
226 Load-in_Time            0x0032   100   100   000    Old_age   Always       -       102400
227 Torq-amp_Count          0x0032   100   100   000    Old_age   Always       -       0
228 Power-off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       3783524142
233 Media_Wearout_Indicator 0x0032   100   100   000    Old_age   Always       -       16271
245 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       0

SMART Error Log Version: 1
No Errors Logged

SMART Self-test log structure revision number 1
Num  Test_Description    Status                  Remaining  LifeTime(hours)  LBA_of_first_error
# 1  Short offline       Completed without error       00%        16         -
# 2  Extended offline    Completed without error       00%        14         -

SMART Selective self-test log data structure revision number 1
 SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS
    1        0        0  Not_testing
    2        0        0  Not_testing
    3        0        0  Not_testing
    4        0        0  Not_testing
    5        0        0  Not_testing
Selective self-test flags (0x0):
  After scanning selected spans, do NOT read-scan remainder of disk.
If Selective self-test is pending on power-up, resume after 0 minute delay.

"""

BAD_TEST_CONTENT = """
smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.10.0-514.26.1.el7.x86_64] (local build)
Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Model Family:     Western Digital Caviar Green (AF, SATA 6Gb/s)
Device Model:     WDC WD20EARX-00PASB0
Serial Number:    WD-WMAZA6913949
LU WWN Device Id: 5 0014ee 206a9fd73
Firmware Version: 51.0AB51
User Capacity:    2,000,398,934,016 bytes [2.00 TB]
Sector Sizes:     512 bytes logical, 4096 bytes physical
Device is:        In smartctl database [for details use: -P show]
ATA Version is:   ATA8-ACS (minor revision not indicated)
SATA Version is:  SATA 3.0, 6.0 Gb/s (current: 6.0 Gb/s)
Local Time is:    Tue Sep 26 09:12:51 2017 AEST
SMART support is: Available - device has SMART capability.
SMART support is: Enabled

=== START OF READ SMART DATA SECTION ===
SMART overall-health self-assessment test result: PASSED

General SMART Values:
Offline data collection status:  (0x82) Offline data collection activity
                                        was completed without error.
                                        Auto Offline Data Collection: Enabled.
Self-test execution status:      (   0) The previous self-test routine completed
                                        without error or no self-test has ever
                                        been run.
Total time to complete Offline
data collection:                (40200) seconds.
Offline data collection
capabilities:                    (0x7b) SMART execute Offline immediate.
                                        Auto Offline data collection on/off support.
                                        Suspend Offline collection upon new
                                        command.
                                        Offline surface scan supported.
                                        Self-test supported.
                                        Offline surface scan supported.
                                        Self-test supported.
                                        Conveyance Self-test supported.
                                        Selective Self-test supported.
SMART capabilities:            (0x0003) Saves SMART data before entering
                                        power-saving mode.
                                        Supports SMART auto save timer.
Error logging capability:        (0x01) Error logging supported.
                                        General Purpose Logging supported.
Short self-test routine
recommended polling time:        (   2) minutes.
Extended self-test routine
recommended polling time:        ( 387) minutes.
Conveyance self-test routine
recommended polling time:        (   5) minutes.
SCT capabilities:              (0x3035) SCT Status supported.
                                        SCT Feature Control supported.
                                        SCT Data Table supported.

SMART Attributes Data Structure revision number: 16
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x002f   200   200   051    Pre-fail  Always       -       12
  3 Spin_Up_Time            0x0027   173   170   021    Pre-fail  Always       -       6350
  4 Start_Stop_Count        0x0032   100   100   000    Old_age   Always       -       87
  5 Reallocated_Sector_Ct   0x0033   197   197   140    Pre-fail  Always       -       144
  7 Seek_Error_Rate         0x002e   200   198   000    Old_age   Always       -       0
  9 Power_On_Hours          0x0032   070   070   000    Old_age   Always       -       22009
 10 Spin_Retry_Count        0x0032   100   253   000    Old_age   Always       -       0
 11 Calibration_Retry_Count 0x0032   100   253   000    Old_age   Always       -       0
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       84
192 Power-Off_Retract_Count 0x0032   200   200   000    Old_age   Always       -       61
193 Load_Cycle_Count        0x0032   001   001   000    Old_age   Always       -       2551803
194 Temperature_Celsius     0x0022   127   092   000    Old_age   Always       -       23
196 Reallocated_Event_Count 0x0032   151   151   000    Old_age   Always       -       49
197 Current_Pending_Sector  0x0032   200   200   000    Old_age   Always       -       0
198 Offline_Uncorrectable   0x0030   200   200   000    Old_age   Offline      -       0
199 UDMA_CRC_Error_Count    0x0032   200   200   000    Old_age   Always       -       3
200 Multi_Zone_Error_Rate   0x0008   200   200   000    Old_age   Offline      -       2

SMART Error Log Version: 1
No Errors Logged

SMART Self-test log structure revision number 1
Num  Test_Description    Status                  Remaining  LifeTime(hours)  LBA_of_first_error
# 1  Short offline       Completed without error       00%     18211         -

SMART Selective self-test log data structure revision number 1
 SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS
    1        0        0  Not_testing
    2        0        0  Not_testing
    3        0        0  Not_testing
    4        0        0  Not_testing
    5        0        0  Not_testing
Selective self-test flags (0x0):
  After scanning selected spans, do NOT read-scan remainder of disk.
If Selective self-test is pending on power-up, resume after 0 minute delay.

"""


@archive_provider(smartctl_reallocated_sectors.smartctl_reallocated_sectors)
def integration_tests():
    # Test that should pass
    data = InputData("No drive errors")
    data.add('smartctl', GOOD_TEST_CONTENT, path="sos_commands/ata/smartctl_-a_.dev.sdd")
    yield data, []

    # Test that should fail
    data = InputData("Reallocated sectors")
    data.add('smartctl', BAD_TEST_CONTENT, path="sos_commands/ata/smartctl_-a_.dev.sda")
    expected = make_response(
        smartctl_reallocated_sectors.ERROR_KEY,
        device='/dev/sda',
        reallocated_sectors=144
    )
    yield data, [expected]
