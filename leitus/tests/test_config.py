#
# Copyright (c) Robert Burrell Donkin 2011-2013, 2020
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
#

import os.path

from leitus import config
from leitus import diagnosis
from leitus import layout


def test_when_configuration_file_is_missing_that_configuration_not_found_error_is_raised():
    dir = "test"
    some_missing_file = "some-missing-file"
    path_exists = os.path.exists(os.path.join("test", some_missing_file))
    assert path_exists != "Please remove " + some_missing_file + " in " + dir + ' before running test'
    subject = config.JsonLoader(some_missing_file, layout.FileSystemLayout(dir))
    try:
        subject.load()
    except diagnosis.ConfigurationNotFoundError:
        pass
