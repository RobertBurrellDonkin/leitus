#
# Copyright (c) Robert Burrell Donkin 2011-2013
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


class TestLUKSDrive(unittest.TestCase):

    def testThatWithConfigurationSetsParameters(self):
        aUUID = "8e1f215f-6c53-4a96-b664-5c1252a06e43"
        aName = "Bingo"
        aTarget = "/some/path"
        drive = surface.Configure().withConfiguration(
            {ConfigConstants().UUID: aUUID, ConfigConstants().NAME: aName, ConfigConstants().TARGET: aTarget})
        self.assertEquals(aName, drive.name)
        self.assertEquals(aTarget, drive.target)
        self.assertEquals(aUUID, drive.uuid)


class TestImageDrive(unittest.TestCase):

    def testWhenAbsoluteSourceIsNotModified(self):
        aSource = "/something.img"
        aName = "Bongo"
        aTarget = "/a/path"
        drive = surface.Configure().withConfiguration(
            {ConfigConstants().SOURCE: aSource, ConfigConstants().NAME: aName, ConfigConstants().TARGET: aTarget})
        self.assertEquals(aName, drive.name)
        self.assertEquals(aTarget, drive.target)
        self.assertEquals(aSource, drive.source)

    def testWhenRelativeIsNotModifiedWithoutLayout(self):
        aSource = "something.img"
        aName = "Bongo"
        aTarget = "/a/path"
        drive = surface.Configure().withConfiguration(
            {ConfigConstants().SOURCE: aSource, ConfigConstants().NAME: aName, ConfigConstants().TARGET: aTarget})
        self.assertEquals(aName, drive.name)
        self.assertEquals(aTarget, drive.target)
        self.assertEquals(aSource, drive.source)

    def testWhenRelativeIsJoinedToDrivesWhenLayoutSet(self):
        aSource = "something.img"
        aName = "Bongo"
        aTarget = "/a/path"
        aDriveDirectory = "drives.d"

        drive = surface.Configure().withConfiguration(
            {ConfigConstants().SOURCE: aSource, ConfigConstants().NAME: aName, ConfigConstants().TARGET: aTarget},
            layout.StandardLayout("conf.d", aDriveDirectory, "profiles.d"))
        self.assertEquals(aName, drive.name)
        self.assertEquals(aTarget, drive.target)
        self.assertEquals(os.path.join(aDriveDirectory, aSource), drive.source)


class TestBuildSessionHome(unittest.TestCase):

    def testForUser(self):
        self.checkUserNamed('a user')
        self.checkUserNamed('ALLCAPS')
        self.checkUserNamed('one')

    def checkUserNamed(self, name):
        self.assertEquals(name, surface.Builder().forUser(name).configuration[surface.ConfigConstants().USER])

    def testMergeProfiles(self):
        self.checkMergeProfiles(['alpha', 'beta', 'gamma'])
        self.checkMergeProfiles([])
        self.checkMergeProfiles(None)
        self.checkMergeProfiles([''])

    def checkMergeProfiles(self, profiles):
        self.assertEquals(profiles,
                          surface.Builder().mergeProfiles(profiles).configuration[surface.ConfigConstants().PROFILES])

    def testWithSize(self):
        self.checkWithSize(12)
        self.checkWithSize('12')
        self.checkWithSize(46)

    def checkWithSize(self, size):
        self.assertEquals(size, surface.Builder().withSize(size).configuration[surface.ConfigConstants().SIZE])

    def testNamed(self):
        self.checkNamed('roger')

    def checkNamed(self, name):
        self.assertEquals(name, surface.Builder().named(name).configuration[surface.ConfigConstants().NAME])

    def testWithSessionHomeConfiguration(self):
        pass

    def checkWithSessionHomeConfiguration(self, user, profiles, size, name):
        self.assertEquals(name, withConfiguration(ConfigConstants().build(user, profiles, size, name)).name)
        self.assertEquals(user, withConfiguration(ConfigConstants().build(user, profiles, size, name)).user.name)
        self.assertEquals(profiles, withConfiguration(ConfigConstants().build(user, profiles, size, name)).profiles)
        self.assertEquals(size,
                          withConfiguration(ConfigConstants().build(user, profiles, size, name)).user.sizeInMegabytes)


if __name__ == '__main__':
    unittest.main()
