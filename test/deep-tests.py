#
# Copyright (c) Robert Burrell Donkin 2012
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

import unittest

from name.robertburrelldonkin.leitus import deep

class SubprocessLoopDeviceStub():
    def status(self, file):
        return self.status_result

class TestLoopDevice(unittest.TestCase):
    
    def testDeviceName(self):
        stub = SubprocessLoopDeviceStub()
        stub.status_result = "/dev/loop0: [fd05]:49178 (/opt/development/leitus/drives.d/small.img)"
        file = "something";
        subject = deep.LoopDevice(file, stub)
        self.assertEqual('/dev/loop0', subject.deviceName())
        

class TestLosetup(unittest.TestCase):
    
    def testAssociated(self):
        subject = deep.Losetup()
        deviceName = "Some device Name"
        args = subject.list(deviceName).args()
        self.assertIsNotNone(args)
        self.assertEqual(3, len(args))
        self.assertEqual("losetup", args[0])
        self.assertEqual("-j", args[1])
        self.assertEqual(deviceName, args[2])
        
        

class TestSessionHome(unittest.TestCase):
    
    def testInfo(self):
        profiles = ["a profile", "another profile"]
        name = "some name"
        sizeInMegabytes = 12345
        user = "some_user"
        target = "some/target"
        subject = deep.SessionHome(profiles, name, sizeInMegabytes, user, target)
        
        self.assertEqual(subject.info(), "\n\nSession drive:\n\n\tsize:\t\t12345M\n\tmapping:\t" +
                         "'some name'\n\ttarget:\t\t'some/target'\n\tuser:\t\tsome_user\n\tprofiles:\t" +
                         "'a profile','another profile'\n\n")
    
class TestLuksDrive(unittest.TestCase):
    
    def testInfo(self):
        uuid = "AAAA-BBBB"
        name = "some name"
        target = "some/target"
        subject = deep.LuksDrive(uuid, name, target)
    
        self.assertEqual(subject.info(), "\n\nLUKS encrypted drive:\n\n\tuuid:\t\tAAAA-BBBB\n\tmapping:\t" +
                         "'some name'\n\ttarget:\t\t'some/target'\n\n")
    

if __name__ == '__main__':
    unittest.main()