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

from leitus import filesystem

SAMPLE_NAME = "music"
SAMPLE_COMMAND = ["dumpe2fs", "-h", "/dev/mapper/music"]

SAMPLE_OUTPUT = """
dumpe2fs 1.45.5 (07-Jan-2020)
Filesystem volume name:   music
Last mounted on:          /home/rob/Music
Filesystem UUID:          d646cbfc-8814-4c40-b8a2-3cd418d4033d
Filesystem magic number:  0xEF53
Filesystem revision #:    1 (dynamic)
Filesystem features:      has_journal ext_attr resize_inode dir_index filetype extent flex_bg sparse_super large_file 
Filesystem flags:         signed_directory_hash 
Default mount options:    user_xattr acl
Filesystem state:         clean
Errors behavior:          Continue
Filesystem OS type:       Linux
Inode count:              19660800
Block count:              78642688
Reserved block count:     3932134
Free blocks:              41215510
Free inodes:              19639803
First block:              0
Block size:               4096
Fragment size:            4096
Reserved GDT blocks:      1005
Blocks per group:         32768
Fragments per group:      32768
Inodes per group:         8192
Inode blocks per group:   512
Flex block group size:    16
Filesystem created:       Fri Apr 10 12:00:58 2015
Last mount time:          Mon Apr 27 08:56:51 2020
Last write time:          Mon Apr 27 08:57:19 2020
Mount count:              2049
Maximum mount count:      -1
Last checked:             Fri Apr 10 12:00:58 2015
Check interval:           0 (<none>)
Lifetime writes:          228 GB
Reserved blocks uid:      0 (user root)
Reserved blocks gid:      0 (group root)
First inode:              11
Inode size:               256
Required extra isize:     28
Desired extra isize:      28
Journal inode:            8
Default directory hash:   half_md4
Directory Hash Seed:      574762dc-d8ca-4711-a33a-7e2802a0e262
Journal backup:           inode blocks
Journal features:         journal_incompat_revoke
Journal size:             128M
Journal length:           32768
Journal sequence:         0x0000cc56
Journal start:            0
"""

TUNED_OUTPUT = """
Last mounted on:          /home/rob/Videos
Filesystem UUID:          2e067b03-693b-49a5-ab61-d9e87e9dddb5
Filesystem magic number:  0xEF53
Filesystem revision #:    1 (dynamic)
Filesystem features:      has_journal ext_attr resize_inode dir_index filetype needs_recovery extent 64bit flex_bg sparse_super large_file huge_file dir_nlink extra_isize
Filesystem flags:         signed_directory_hash 
Default mount options:    user_xattr acl
Filesystem state:         clean
Errors behavior:          Continue
Filesystem OS type:       Linux
Inode count:              3815552
Block count:              976753873
Reserved block count:     48837693
Free blocks:              163837403
Free inodes:              3810953
First block:              0
Block size:               4096
Fragment size:            4096
Group descriptor size:    64
Reserved GDT blocks:      1024
Blocks per group:         32768
Fragments per group:      32768
Inodes per group:         128
Inode blocks per group:   8
Flex block group size:    16
Filesystem created:       Fri Oct  6 20:00:01 2017
Last mount time:          Mon Apr 27 18:51:05 2020
Last write time:          Mon Apr 27 18:51:05 2020
Mount count:              4
Maximum mount count:      30
Last checked:             Sun Apr 26 09:45:01 2020
Check interval:           2592000 (1 month)
Next check after:         Tue May 26 09:45:01 2020
Lifetime writes:          3178 GB
Reserved blocks uid:      0 (user root)
Reserved blocks gid:      0 (group root)
First inode:              11
Inode size:               256
Required extra isize:     32
Desired extra isize:      32
Journal inode:            8
Default directory hash:   half_md4
Directory Hash Seed:      f6295615-c371-4ad5-991a-f3e2fc8c2256
Journal backup:           inode blocks
Journal features:         journal_incompat_revoke journal_64bit
Journal size:             128M
Journal length:           32768
Journal sequence:         0x00011839
Journal start:            0
"""


@mock.patch('leitus.filesystem.subprocess')
def test_tune_interval_call(mock_subprocess):
    filesystem.ExtFileSystem.tune_interval(SAMPLE_NAME, interval=33)

    mock_subprocess.check_call.assert_has_calls([
        mock.call(
            [
                "tune2fs",
                "-i 33",
                "/dev/mapper/music"]
        )
    ])


@mock.patch('leitus.filesystem.subprocess')
def test_tune_count_call(mock_subprocess):
    filesystem.ExtFileSystem.tune_count(SAMPLE_NAME, count=77)

    mock_subprocess.check_call.assert_has_calls([
        mock.call(
            [
                "tune2fs",
                "-c 77",
                "/dev/mapper/music"]
        )
    ])


@mock.patch('leitus.filesystem.subprocess')
def test_headers_call(mock_subprocess):
    filesystem.ExtFileSystem.headers(SAMPLE_NAME)

    mock_subprocess.check_output.assert_has_calls([
        mock.call(SAMPLE_COMMAND, universal_newlines=True)
    ])


@mock.patch('leitus.filesystem.subprocess')
def test_headers_output(mock_subprocess):
    mock_subprocess.check_output.return_value = SAMPLE_OUTPUT

    assert filesystem.ExtFileSystem.headers(SAMPLE_NAME).raw == SAMPLE_OUTPUT


def test_is_check_interval_set_when_unset():
    assert filesystem.FileSystemHeaders(SAMPLE_OUTPUT).is_check_interval_set == False


def test_is_max_count_set_when_unset():
    assert filesystem.FileSystemHeaders(SAMPLE_OUTPUT).is_max_count_set == False


def test_is_check_interval_set_when_set():
    assert filesystem.FileSystemHeaders(TUNED_OUTPUT).is_check_interval_set == True


def test_is_max_count_set_when_set():
    assert filesystem.FileSystemHeaders(TUNED_OUTPUT).is_max_count_set == True


def test_last_check():
    assert filesystem.FileSystemHeaders(SAMPLE_OUTPUT).last_check == "Fri Apr 10 12:00:58 2015"


def test_check_interval():
    assert filesystem.FileSystemHeaders(SAMPLE_OUTPUT).check_interval == "0 (<none>)"


def test_mount_count():
    assert filesystem.FileSystemHeaders(SAMPLE_OUTPUT).mount_count == "2049"


def test_max_mount_count():
    assert filesystem.FileSystemHeaders(SAMPLE_OUTPUT).max_mount_count == "-1"


def test_missing_last_check():
    assert filesystem.FileSystemHeaders("").last_check is None


def test_missing_check_interval():
    assert filesystem.FileSystemHeaders("").check_interval is None


def test_missing_mount_count():
    assert filesystem.FileSystemHeaders("").mount_count is None


def test_missing_max_mount_count():
    assert filesystem.FileSystemHeaders("").max_mount_count is None


def test_headers_str():
    assert str(filesystem.FileSystemHeaders(SAMPLE_OUTPUT)) == """
Last check:           Fri Apr 10 12:00:58 2015
Check interval:       0 (<none>)
Mount count:          2049
Maximum mount count:  -1
"""


def test_missing_headers_str():
    assert str(filesystem.FileSystemHeaders("")) == """
Last check:           
Check interval:       
Mount count:          
Maximum mount count:  
"""
