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

from leitus import cli


@mock.patch('leitus.cli.sys.stdout')
def test_write_info(mock_stdout):

    cli.write_info()

    mock_stdout.write.assert_has_calls([
            mock.call(
                "Leitus " + cli.__version__ + "\n\n  "
                "Add the drive name to the command line, and I'll describe its configuration.\n\n"
                "  For example 'leitus --info cool'\n\n")
        ])
