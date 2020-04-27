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
from leitus.errors import CryptsetupError

CRYPTSETUP = 'cryptsetup'


class CryptSetup:

    @staticmethod
    def map(name, device):
        args = ['cryptsetup',
                '-d', '/dev/urandom',
                'create',
                name, device]
        subprocess.check_call(args)

    @staticmethod
    def unmap(name):
        args = ['cryptsetup',
                'remove', name]
        subprocess.check_call(args)


class CryptDeviceWithRandomKey:

    @staticmethod
    def on(source):
        return DeviceMapping(source, CryptSetup())


class LuksSetup:

    @staticmethod
    def map(name, device):
        LuksSetup.luks_open(device, name)
        ExtFileSystem.headers(name)
        LuksSetup.check_filesystem(name)

    @staticmethod
    def check_filesystem(name):
        args = ['fsck',
                '-MCr',
                DeviceMapping.name_after_mapping(name)]
        subprocess.check_call(args)

    @staticmethod
    def luks_open(device, name):
        args = [CRYPTSETUP,
                'luksOpen',
                device,
                name]
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError as e:
            raise CryptsetupError(e)

    @staticmethod
    def unmap(name):
        args = [CRYPTSETUP,
                'luksClose',
                name]
        subprocess.check_call(args)

    @staticmethod
    def is_in_use(name):
        args = [CRYPTSETUP,
                'status',
                name]
        return subprocess.call(args) == 0


class LuksDevice:

    @staticmethod
    def on(source):
        return DeviceMapping(source, LuksSetup())


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
