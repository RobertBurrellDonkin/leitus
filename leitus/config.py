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
# Leitus is a suite of higher level functions for cryptographic drives.
# The config module contains configuration foo.
#
#

import json

from leitus import diagnosis
from leitus import user


def load(name, layout):
    return JsonLoader(name, layout).load()


class ConfigConstants:
    USER = 'user'
    PROFILES = 'profiles'
    SIZE = 'sizeInMeg'
    NAME = 'name'
    UUID = 'UUID'
    TARGET = 'target'
    SOURCE = 'source'

    def build(self, user_name, profiles, size, name):
        return {self.USER: user_name, self.PROFILES: profiles,
                self.SIZE: size, self.NAME: name}

    def target_for(self, configuration):
        return configuration[self.TARGET]

    def source_for(self, configuration):
        return configuration[self.SOURCE]

    def uuid_for(self, configuration):
        return configuration[self.UUID]

    def user_name_for(self, configuration):
        return configuration[self.USER]

    def user_for(self, configuration):
        return user.User(self.user_name_for(configuration))

    def profiles_for(self, configuration):
        return configuration[self.PROFILES]

    def name_for(self, configuration):
        return configuration[self.NAME]

    def size_for(self, configuration):
        return configuration[self.SIZE]


class JsonLoader:
    SUFFIX = ".json"

    def __init__(self, name, layout):
        self.resource = name + self.SUFFIX
        self.layout = layout

    def load(self):
        try:
            return json.load(self.layout.read(self.resource))
        except IOError as e:
            error_number = e.errno
            error_message = e.strerror
            if error_number == 2:
                raise diagnosis.ConfigurationNotFoundError(self.resource, self.layout, error_message)
            elif error_number == 13:
                raise diagnosis.ConfigurationPermissionError(self.resource, self.layout, error_message)
            else:
                raise
