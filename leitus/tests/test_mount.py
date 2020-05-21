#
# Copyright (c) Robert Burrell Donkin 2020
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
from unittest import mock

from leitus import device

SAMPLE_OUTPUT = """
Filesystem                                       1K-blocks      Used Available Use% Mounted on
/dev/mapper/root                                  51480916  30205220  20751348  60% /
tmpfs                                              1527880      1804   1526076   1% /run
cgroup_root                                          10240         0     10240   0% /sys/fs/cgroup
dev                                                7620044         0   7620044   0% /dev
shm                                                7639388     73440   7565948   1% /dev/shm
/dev/mapper/crypt-tmp                             51606140     53132  48931568   1% /tmp
tmpfs                                              4194304         0   4194304   0% /var/tmp-portage/tmpfs
/dev/mapper/VolGroupArgosBlack1T-lvPortageBigTmp  20511356   2475500  16970896  13% /var/tmp-portage/notmpfs
/dev/mapper/VolGroupArgosBlack1T-lvBoinc          10190136   3799620   5849844  40% /var/lib/boinc
/dev/mapper/crypt-portageDistfiles                20509308  11996992   7447460  62% /usr/portage/distfiles
/dev/mapper/crypt-robDownloads                    20509308   9462556   9981896  49% /home/rob/Desktop/Downloads
/dev/mapper/crypt-leitusImages                    20509308  13827096   5617356  72% /var/lib/leitus
/dev/mapper/crypt-james                           28766332  14464592  12817456  54% /home/james
/dev/mapper/leitus-vanilla                        10239252    178224   9521176   2% /home/adam
tmpfs                                              1527876         8   1527868   1% /run/user/9007
tmpfs                                              1527876         0   1527876   0% /run/user/120
/dev/mapper/leitus-pike                           10253588   1945428   7767592  21% /home/sandy
/dev/mapper/music                                309504000 144641960 149117120  50% /home/rob/Music
tmpfs                                              1527876        20   1527856   1% /run/user/1002
tmpfs                                              1527876         0   1527876   0% /run/user/0
"""


@mock.patch('leitus.device.subprocess')
def test_list_df(mock_subprocess):
    mock_subprocess.check_output.return_value = SAMPLE_OUTPUT

    assert device.MountPoint.list() == ['vanilla', 'pike']


@mock.patch('leitus.device.subprocess')
def test_active_mount(mock_subprocess):
    mock_subprocess.check_output.return_value = SAMPLE_OUTPUT

    assert device.MountPoint.active("vanilla") == ['/home/adam']


@mock.patch('leitus.device.subprocess')
def test_inactive_mount(mock_subprocess):
    mock_subprocess.check_output.return_value = SAMPLE_OUTPUT

    assert device.MountPoint.active("bogus") == []


@mock.patch('leitus.device.subprocess')
def test_all_active(mock_subprocess):
    mock_subprocess.check_output.return_value = SAMPLE_OUTPUT

    assert device.MountPoint.all_active() == ['/home/adam', '/home/sandy']


@mock.patch('leitus.device.subprocess')
def test_umount_all(mock_subprocess):
    mock_subprocess.check_output.return_value = SAMPLE_OUTPUT

    device.MountPoint.umount_all()

    mock_subprocess.check_call.assert_has_calls([
        mock.call(
            [
                "umount",
                '/home/adam']
        ),
        mock.call(
            [
                "umount",
                '/home/sandy']
        )
    ])
