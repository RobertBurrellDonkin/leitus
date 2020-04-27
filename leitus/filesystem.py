#
# Copyright (c) Robert Burrell Donkin 2012-2013, 2020
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
#
#
#

import subprocess

from leitus.device import DeviceMapping


def headers(name):
    return ExtFileSystem.headers(name)


class FileSystemHeaders:
    def __init__(self, raw):
        self.raw = raw

    def __str__(self):
        return self.raw


class ExtFileSystem:

    @staticmethod
    def format(device):
        subprocess.check_call([
            'mke2fs',
            '-j',
            '-m',
            '1',
            '-O',
            'dir_index,filetype',
            device])

    @staticmethod
    def headers(name):
        return FileSystemHeaders(
            subprocess.check_output(
                [
                    "dumpe2fs",
                    "-h",
                    DeviceMapping.name_after_mapping(name)
                ]
            ))
