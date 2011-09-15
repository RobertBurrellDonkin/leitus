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
# The config module contains configuration foo.
#
# Robert Burrell Donkin, 2011
#

import os.path
import json

from name.robertburrelldonkin.leitus import deep

def load(name, layout):
    return JsonLoader(name, layout).load()
    
class ConfigConstants():
    USER = 'user'
    PROFILES = 'profiles'
    SIZE = 'sizeInMeg'
    NAME = 'name'
    UUID = 'UUID'
    TARGET = 'target'
    SOURCE = 'source'
    
    def build(self, user, profiles, size, name):
        return {self.USER:user, self.PROFILES: profiles,
                    self.SIZE: size, self.NAME:name}
        
    def targetFor(self, configuration):
        return configuration[self.TARGET]
    
    def sourceFor(self, configuration):
        return configuration[self.SOURCE]
    
    def uuidFor(self, configuration):
        return configuration[self.UUID]
        
    def userNameFor(self, configuration):
        return configuration[self.USER]
        
    def userFor(self, configuration):
        return deep.User(self.userNameFor(configuration))
        
    def profilesFor(self, configuration):
        return configuration[self.PROFILES]
        
    def nameFor(self, configuration):
        return configuration[self.NAME]
        
    def sizeFor(self, configuration):
        return configuration[self.SIZE]

class JsonLoader():
    SUFFIX = ".json"
    
    def __init__(self, name, layout):
        self.resource = name + self.SUFFIX
        self.layout = layout
        
    def load(self):
        return json.load(self.layout.read(self.resource))