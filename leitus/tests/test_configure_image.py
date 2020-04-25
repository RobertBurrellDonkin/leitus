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
import unittest

from leitus import layout
from leitus import surface
from leitus.config import ConfigConstants


# class TestLUKSDrive(unittest.TestCase):
#
#     def testThatWithConfigurationSetsParameters(self):
#         a_uuid = "8e1f215f-6c53-4a96-b664-5c1252a06e43"
#         a_name = "Bingo"
#         a_target = "/some/path"
#         drive = surface.with_configuration(
#             {ConfigConstants().UUID: a_uuid, ConfigConstants().NAME: a_name, ConfigConstants().TARGET: a_target})
#         self.assertEqual(a_name, drive.name)
#         self.assertEqual(a_target, drive.target)
#         self.assertEqual(a_uuid, drive.uuid)
#
#
# class TestImageDrive(unittest.TestCase):
#
#     def testWhenAbsoluteSourceIsNotModified(self):
#         aSource = "/something.img"
#         aName = "Bongo"
#         aTarget = "/a/path"
#         drive = surface.Configure().with_configuration(
#             {ConfigConstants().SOURCE: aSource, ConfigConstants().NAME: aName, ConfigConstants().TARGET: aTarget})
#         self.assertEqual(aName, drive.name)
#         self.assertEqual(aTarget, drive.target)
#         self.assertEqual(aSource, drive.source)
#
#     def testWhenRelativeIsNotModifiedWithoutLayout(self):
#         aSource = "something.img"
#         aName = "Bongo"
#         aTarget = "/a/path"
#         drive = surface.Configure().with_configuration(
#             {ConfigConstants().SOURCE: aSource, ConfigConstants().NAME: aName, ConfigConstants().TARGET: aTarget})
#         self.assertEqual(aName, drive.name)
#         self.assertEqual(aTarget, drive.target)
#         self.assertEqual(aSource, drive.source)
#
#     def testWhenRelativeIsJoinedToDrivesWhenLayoutSet(self):
#         aSource = "something.img"
#         aName = "Bongo"
#         aTarget = "/a/path"
#         aDriveDirectory = "drives.d"
#
#         drive = surface.Configure().with_configuration(
#             {ConfigConstants().SOURCE: aSource, ConfigConstants().NAME: aName, ConfigConstants().TARGET: aTarget},
#             layout.StandardLayout("conf.d", aDriveDirectory, "profiles.d"))
#         self.assertEqual(aName, drive.name)
#         self.assertEqual(aTarget, drive.target)
#         self.assertEqual(os.path.join(aDriveDirectory, aSource), drive.source)

if __name__ == '__main__':
    unittest.main()
