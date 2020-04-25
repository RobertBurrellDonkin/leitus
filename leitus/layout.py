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
# The layout module abstracts options for laying out resources.
#

import os.path

from leitus import diagnosis


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

    def drivePath(self, resource):
        if os.path.isabs(resource):
            return resource
        else:
            return self.drives().as_path(resource)


class FileSystemLayout():
    READ_ONLY = 'r'

    def __init__(self, directory):
        self.directory = directory

    def read(self, resource):
        try:
            return open(self.as_path(resource), self.READ_ONLY)
        except IOError as e:
            error_number = e.errno
            error_message = e.strerror
            if error_number == 2:
                raise diagnosis.ConfigurationNotFoundError(resource, self, error_message)
            elif error_number == 13:
                raise diagnosis.ConfigurationPermissionError(resource, self, error_message)
            else:
                raise

    def as_path(self, resource):
        return os.path.join(self.directory, resource)

    def __repr__(self):
        return "directory %(dir)s" % {"dir": repr(self.directory)}


__version__ = '1.0rc2.dev'
