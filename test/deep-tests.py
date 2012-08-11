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
        
        
    
if __name__ == '__main__':
    unittest.main()