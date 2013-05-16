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
# Leitus is a suite of higher level functions for cryptographic drives.
# The surface module contains a high level API.
#
# Robert Burrell Donkin, 2011
#

import os

from leitus import deep
from leitus import config
from leitus import layout
from leitus import diagnosis
from leitus.config import ConfigConstants

def standard():
    return sessionHome('neo').withSize(2000).forUser(
        'rdonkin').mergeProfiles(['home', 'gnome', 'maven', 'java6']
        ).build()
    
def sessionHome(name):
    return Builder().named(name)
    
class Configure():
    def __init__(self, api = deep.Facade()):
        self.api = api
        
    def withConfiguration(self, configuration, directoryLayout = None):
        constants = ConfigConstants()
        if constants.UUID in configuration:
            return self.api.aLuksDrive(constants.uuidFor(configuration),
                           constants.nameFor(configuration),
                           constants.targetFor(configuration))
        elif constants.SOURCE in configuration:
            sourceDiscImage = constants.sourceFor(configuration)
            if (directoryLayout):
                sourceDiscImage = directoryLayout.drivePath(sourceDiscImage)
            return self.api.anImageDrive(sourceDiscImage,
                           constants.nameFor(configuration),
                           constants.targetFor(configuration))
        else:
            user = constants.userFor(configuration)
            return self.api.aSessionHome(constants.profilesFor(configuration),
                constants.nameFor(configuration), constants.sizeFor(configuration),
                        user, user.home())
    
class Builder():
    
    def __init__(self):
        self.configuration = {}
        self.constants = ConfigConstants()  
    
    def mergeProfiles(self, profiles):
        self.configuration[self.constants.PROFILES] = profiles
        return self
    
    def forUser(self, withName):
        self.configuration[self.constants.USER] = withName
        return self
    
    def withSize(self, megabytes):
        self.configuration[self.constants.SIZE] = megabytes
        return self
    
    def named(self, name):
        self.configuration[self.constants.NAME] = name
        return self
    
    def build(self):
        return withConfiguration(self.configuration)
        

class Leitus():
    def __init__(self, conf_d, drives_d, profiles_d, api=deep.Facade()):
        self.layout = layout.StandardLayout(conf_d, drives_d, profiles_d)
        self.api = api
    
    def withConfiguration(self, name):
        return Configure(api).withConfiguration(config.load(name, self.layout.conf()), self.layout);
    
    def perform(self, name):
        try:
            if name:
                self.withConfiguration(name).perform()
            else:
                standard().perform()
        except deep.DiscImageNotFoundError as error:
            raise diagnosis.MissingDiscImageError(self.layout, error, error.resource)
            
        except deep.PassphaseError as error:
            raise diagnosis.CouldNotUnlockEncryptedDrive(self.layout, error, error.resource)
        
        except deep.UnsupportedError as error:
            raise diagnosis.UnsupportedRequirementError(error)
            
        except deep.AlreadyInUseError as error:
            raise diagnosis.InUseError(error)
        
            
    def info(self, name):
        if name:
            return self.withConfiguration(name).info()
        else:
            return "Here's the deal: a name for information"
        
__version__='0.6dev'