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

from leitus import deep

name = "A-NAME"
device = "/some/device"


@mock.patch('leitus.deep.subprocess')
def test_calls_cryptsetup(mock_subprocess):
    deep.LuksSetup.map(name, device)

    mock_subprocess.check_call.assert_has_calls([
        mock.call(
            ['cryptsetup',
             'luksOpen',
             "/some/device",
             "A-NAME"]
        ),
        mock.call(
            ['fsck',
             '-MCr',
             "/dev/mapper/A-NAME"]
        )
    ])
