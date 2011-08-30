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
# The layout module abstracts options for laying out resources.
#
# Robert Burrell Donkin, 2011
#

import os.path

class StandardLayout():

    def __init__(self, conf_d, drives_d, profiles_d):
        self.drives_d = drives_d
        self.conf_d = conf_d
        self.profiles_d = profiles_d
    
    def drives(self):
        return FileSystemLayout(self.drives_d)
    
    def conf(self):
        return FileSystemLayout(self.conf_d)
        
    def profiles(self):
        return FileSystemLayout(self.profiles_d)
    
class FileSystemLayout():
    READ_ONLY = 'r'
    
    def __init__(self, directory):
        self.directory = directory
    
    def read(self, resource):
        return open(os.path.join(self.directory, resource), self.READ_ONLY)

