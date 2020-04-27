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


class Line:
    def __init__(self, line):

        parts = line.split(':', 1)
        self.name = parts[0]
        self.is_check_interval = self.name == "Check interval"
        self.is_last_check = self.name == "Last checked"
        self.is_mount_count = self.name == "Mount count"
        self.is_max_mount_count = self.name == "Maximum mount count"
        if len(parts) > 1:
            self.value = parts[1].strip()
        else:
            self.value = None


HEADER_STRING = """
Last check:           {}
Check interval:       {}
Mount count:          {}
Maximum mount count:  {}
"""


class FileSystemHeaders:
    def __init__(self, raw):
        self.raw = raw
        self.check_interval = None
        self.last_check = None
        self.mount_count = None
        self.max_mount_count = None
        for line in raw.splitlines(False):
            header = Line(line)
            if header.is_check_interval:
                self.check_interval = header.value
            elif header.is_last_check:
                self.last_check = header.value
            elif header.is_mount_count:
                self.mount_count = header.value
            elif header.is_max_mount_count:
                self.max_mount_count = header.value

    def __str__(self):
        return HEADER_STRING.format(
            self.last_check or '',
            self.check_interval or '',
            self.mount_count or '',
            self.max_mount_count or '')


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
