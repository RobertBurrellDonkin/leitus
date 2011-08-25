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
# The surface module contains a high level API.
#
# Robert Burrell Donkin, 2011
#

import os

from name.robertburrelldonkin.leitus import deep
from name.robertburrelldonkin.leitus.config import ConfigConstants

def standard():
    return sessionHome('neo').withSize(2000).forUser(
        'rdonkin').mergeProfiles(['home', 'gnome', 'maven', 'java6']
        ).build()
    
def sessionHome(name):
    return Builder().named(name)
    
def withConfiguration(configuration):
    constants = ConfigConstants()
    user = constants.userFor(configuration)
    return deep.Leitus(constants.profilesFor(configuration),
            constants.nameFor(configuration), constants.sizeFor(configuration),
                    user, user.home())
    
class Builder():
    
    def __init__(self):
        self.configuration = {}
        self.constants = ConfigConstants()  
    
    def mergeProfiles(self, profiles):
        self.configuration[ConfigConstants.PROFILES] = profiles
        return self
    
    def forUser(self, withName):
        self.configuration[ConfigConstants.USER] = withName
        return self
    
    def withSize(self, megabytes):
        self.configuration[ConfigConstants.SIZE] = megabytes
        return self
    
    def named(self, name):
        self.configuration[ConfigConstants.NAME] = name
        return self
    
    def build(self):
        return withConfiguration(self.configuration)