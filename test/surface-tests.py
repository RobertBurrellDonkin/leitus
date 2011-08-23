#
# Copyright (c) Robert Burrell Donkin 2011
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# Leitus is a suite of higher level functions for cryptographic drives.
# The contents tests the surface module.
#
# Robert Burrell Donkin, 2011
#

import unittest

from name.robertburrelldonkin.leitus import surface

class TestBuildSessionHome(unittest.TestCase):
    
    def testForUser(self):
        self.checkUserNamed('a user')
        self.checkUserNamed('ALLCAPS')
        self.checkUserNamed('one')
        
    def checkUserNamed(self, name):
        self.assertEquals(name, surface.Builder().forUser(name).configuration[surface.ConfigConstants().USER])
    
    
    
if __name__ == '__main__':
    unittest.main()