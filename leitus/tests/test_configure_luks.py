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

from leitus import surface
from leitus.config import ConfigConstants


def test_sets_name():
    a_uuid = "8e1f215f-6c53-4a96-b664-5c1252a06e43"
    a_name = "Bingo"
    a_target = "/some/path"
    drive = surface.with_configuration(
        {ConfigConstants().UUID: a_uuid, ConfigConstants().NAME: a_name, ConfigConstants().TARGET: a_target})
    assert a_name == drive.name


def test_sets_target():
    a_uuid = "8e1f215f-6c53-4a96-b664-5c1252a06e43"
    a_name = "Bingo"
    a_target = "/some/path"
    drive = surface.with_configuration(
        {ConfigConstants().UUID: a_uuid, ConfigConstants().NAME: a_name, ConfigConstants().TARGET: a_target})
    assert a_target, drive.target
    assert a_uuid == drive.uuid


def test_sets_uuid():
    a_uuid = "8e1f215f-6c53-4a96-b664-5c1252a06e43"
    a_name = "Bingo"
    a_target = "/some/path"
    drive = surface.with_configuration(
        {ConfigConstants().UUID: a_uuid, ConfigConstants().NAME: a_name, ConfigConstants().TARGET: a_target})
    assert a_uuid == drive.uuid
