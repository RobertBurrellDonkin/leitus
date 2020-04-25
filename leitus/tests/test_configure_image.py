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


def test_whenAbsoluteSourceIsNotModified():
    aSource = "/something.img"
    aName = "Bongo"
    aTarget = "/a/path"
    drive = surface.with_configuration(
        {ConfigConstants().SOURCE: aSource, ConfigConstants().NAME: aName, ConfigConstants().TARGET: aTarget})
    assert aName == drive.name
    assert aTarget == drive.target
    assert aSource == drive.source


def test_whenRelativeIsNotModifiedWithoutLayout():
    aSource = "something.img"
    aName = "Bongo"
    aTarget = "/a/path"
    drive = surface.with_configuration(
        {ConfigConstants().SOURCE: aSource, ConfigConstants().NAME: aName, ConfigConstants().TARGET: aTarget})
    assert aName == drive.name
    assert aTarget == drive.target
    assert aSource == drive.source


def test_whenRelativeIsJoinedToDrivesWhenLayoutSet():
    aSource = "something.img"
    aName = "Bongo"
    aTarget = "/a/path"
    aDriveDirectory = "drives.d"

    drive = surface.with_configuration(
        {ConfigConstants().SOURCE: aSource, ConfigConstants().NAME: aName, ConfigConstants().TARGET: aTarget},
        layout.StandardLayout("conf.d", aDriveDirectory, "profiles.d"))
    assert aName == drive.name
    assert aTarget == drive.target
    assert os.path.join(aDriveDirectory, aSource) == drive.source
