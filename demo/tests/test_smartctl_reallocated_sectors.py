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
smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.10.0-514.10.2.el7.x86_64] (local build)
Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Device Model:     INTEL SSDSC2BB150G7
Serial Number:    PHDV64130020150MGN
LU WWN Device Id: 5 5cd2e4 14d4debe0
Firmware Version: N2010101
User Capacity:    150,039,945,216 bytes [150 GB]
Sector Sizes:     512 bytes logical, 4096 bytes physical
Rotation Rate:    Solid State Device
Device is:        Not in smartctl database [for details use: -P showall]
ATA Version is:   ACS-3 (unknown minor revision code: 0x006d)
SATA Version is:  SATA 3.1, 6.0 Gb/s (current: 6.0 Gb/s)
Local Time is:    Tue Aug  1 10:16:36 2017 EDT
SMART support is: Available - device has SMART capability.
SMART support is: Enabled

=== START OF READ SMART DATA SECTION ===
SMART overall-health self-assessment test result: PASSED

General SMART Values:
Offline data collection status:  (0x00) Offline data collection activity
                                        was never started.
                                        Auto Offline Data Collection: Disabled.
Self-test execution status:      (   0) The previous self-test routine completed
                                        without error or no self-test has ever
                                        been run.
Total time to complete Offline
data collection:                (    0) seconds.
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
recommended polling time:        (   2) minutes.
Conveyance self-test routine
recommended polling time:        (   2) minutes.
SCT capabilities:              (0x003d) SCT Status supported.
                                        SCT Error Recovery Control supported.
                                        SCT Feature Control supported.
                                        SCT Data Table supported.

SMART Attributes Data Structure revision number: 1
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  5 Reallocated_Sector_Ct   0x0032   099   099   000    Old_age   Always       -       4
  9 Power_On_Hours          0x0032   100   100   000    Old_age   Always       -       4394
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       20
170 Unknown_Attribute       0x0033   099   099   010    Pre-fail  Always       -       0
171 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       4
172 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       0
174 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       13
175 Program_Fail_Count_Chip 0x0033   100   100   010    Pre-fail  Always       -       189500766412
183 Runtime_Bad_Block       0x0032   100   100   000    Old_age   Always       -       0
184 End-to-End_Error        0x0033   100   100   090    Pre-fail  Always       -       0
187 Reported_Uncorrect      0x0032   100   100   000    Old_age   Always       -       0
190 Airflow_Temperature_Cel 0x0022   066   055   000    Old_age   Always       -       34 (Min/Max 30/45)
192 Power-Off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       13
194 Temperature_Celsius     0x0022   100   100   000    Old_age   Always       -       34
197 Current_Pending_Sector  0x0012   100   100   000    Old_age   Always       -       0
199 UDMA_CRC_Error_Count    0x003e   100   100   000    Old_age   Always       -       0
225 Unknown_SSD_Attribute   0x0032   100   100   000    Old_age   Always       -       44898
226 Unknown_SSD_Attribute   0x0032   100   100   000    Old_age   Always       -       450
227 Unknown_SSD_Attribute   0x0032   100   100   000    Old_age   Always       -       76
228 Power-off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       263641
232 Available_Reservd_Space 0x0033   099   099   010    Pre-fail  Always       -       0
233 Media_Wearout_Indicator 0x0032   100   100   000    Old_age   Always       -       0
234 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       0
241 Total_LBAs_Written      0x0032   100   100   000    Old_age   Always       -       44898
242 Total_LBAs_Read         0x0032   100   100   000    Old_age   Always       -       144156
243 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       144361

SMART Error Log Version: 1
No Errors Logged

SMART Self-test log structure revision number 1
No self-tests have been logged.  [To run self-tests, use: smartctl -t]


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


@archive_provider(smartctl_reallocated_sectors)
def integration_tests():
    # Test that should pass
    data = InputData("good_test_1")
    data.add('smartctl', GOOD_TEST_CONTENT, path="sos_commands/ata/smartctl_-a_.dev.sdd")
    yield data, []

    # Test that should fail
    data = InputData("bad_test_1")
    data.add('smartctl', BAD_TEST_CONTENT, path="sos_commands/ata/smartctl_-a_.dev.sda")
    expected = make_response(
        smartctl_reallocated_sectors.ERROR_KEY,
        device='/dev/sda',
        reallocated_sectors=4
    )
    yield data, [expected]
