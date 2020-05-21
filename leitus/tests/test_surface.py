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

from leitus import surface


@mock.patch('leitus.surface.device')
def test_list(mock_device):
    mock_device.MountPoint.list.return_value = ["alice", "betty", "clem"]

    assert surface.Leitus(None, None, None).list() == ["alice", "betty", "clem"]


@mock.patch('leitus.surface.device.MountPoint')
@mock.patch('leitus.surface.crypt')
def test_close_all(mock_crypt, mock_mount_point):
    mock_mount_point.list.return_value = ["alice", "betty", "clem"]

    surface.Leitus(None, None, None).close_all()

    mock_mount_point.unmount_all.assert_has_calls([
        mock.call()
    ])

    mock_crypt.CryptSetup.close.assert_has_calls([
        mock.call('leitus-alice'),
        mock.call('leitus-betty'),
        mock.call('leitus-clem')
    ])
