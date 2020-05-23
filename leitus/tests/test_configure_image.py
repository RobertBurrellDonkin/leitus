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
#
# Leitus is a suite of higher level functions for cryptographic drives.
# The contents tests the surface module.
#
# Robert Burrell Donkin, 2011
#

import os.path

from leitus import layout
from leitus import surface
from leitus.config import ConfigConstants


def test_when_absolute_source_is_not_modified():
    a_source = "/something.img"
    a_name = "leitus-Bongo"
    a_target = "/a/path"
    drive = surface.with_configuration(
        {ConfigConstants().SOURCE: a_source, ConfigConstants().NAME: a_name, ConfigConstants().TARGET: a_target})
    assert a_name == drive.name
    assert a_target == drive.target
    assert a_source == drive.source


def test_when_relative_is_not_modified_without_layout():
    a_source = "something.img"
    a_name = "leitus-Bongo"
    a_target = "/a/path"
    drive = surface.with_configuration(
        {ConfigConstants().SOURCE: a_source, ConfigConstants().NAME: a_name, ConfigConstants().TARGET: a_target})
    assert a_name == drive.name
    assert a_target == drive.target
    assert a_source == drive.source


def test_when_relative_is_joined_to_drives_when_layout_set():
    a_source = "something.img"
    a_name = "leitus-Bongo"
    a_target = "/a/path"
    a_drive_directory = "drives.d"

    drive = surface.with_configuration(
        {ConfigConstants().SOURCE: a_source, ConfigConstants().NAME: a_name, ConfigConstants().TARGET: a_target},
        layout.StandardLayout("conf.d", a_drive_directory, "profiles.d"))
    assert a_name == drive.name
    assert a_target == drive.target
    assert os.path.join(a_drive_directory, a_source) == drive.source
