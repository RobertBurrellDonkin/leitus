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

import os
import os.path
import pwd
import shutil
import stat
import subprocess

from leitus.errors import AlreadyInUseError, NotFoundError, LowLevelError, \
    PassphaseError, CryptsetupError

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


class DiskByUUID:
    PATH = '/dev/disk/by-uuid/'

    def __init__(self, uuid):
        self.uuid = uuid

    def device_name(self):
        return self.PATH + self.uuid

    def close(self):
        pass


class DeviceMapping:
    def __init__(self, source, api):
        self.device = source.device_name()
        self.api = api
        self.source = source

    @staticmethod
    def name_after_mapping(name):
        return '/dev/mapper/{0}'.format(name)

    def map_to(self, name):
        try:
            self.api.map(name, self.device)
            return self.file_system(name)
        except LowLevelError as e:
            if e.is_already_in_use():
                raise AlreadyInUseError(self.device)
            if e.is_bad_passphrase():
                raise PassphaseError(self.device)
            raise

    def file_system(self, name):
        return FileSystemOnDeviceMapping(self.name_after_mapping(name))

    def unmap_from(self, name, mount_point=None):
        self.file_system(name).unmount_from(mount_point)
        self.api.unmap(name)
        self.source.close()

    def is_in_use(self, name):
        return self.api.is_in_use(name)

    def toggle(self, name, target):
        if self.is_in_use(name):
            self.unmap_from(name)
        else:
            self.map_to(name).mount_on(target)
        return self


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


class SubprocessMount:
    def mount(self, device, on_path):
        subprocess.check_call(['mount', device, on_path])

    def unmount(self, on_path):
        if (on_path):
            subprocess.check_call(['umount', on_path])


class FileSystemOnDeviceMapping:

    def __init__(self, on_device):
        self.on_device = on_device
        self.api = SubprocessMount()

    def with_format(self, api):
        api.format(self.on_device)
        return self

    def mount_on(self, path):
        self.api.mount(self.on_device, path)
        return MountedFileSystem(path)

    def unmount_from(self, path):
        self.api.unmount(path)

class Copy:
    """
    Copy operations.
    """

    def __init__(self, source):
        self.source = source

    def into(self, target):
        """
        Copies (recursively) all files in source into the
        given target directory. (As far as possible) meta-data
        is preserved.
        """
        if not (os.path.exists(self.source)):
            raise NotFoundError(self.source)
        if not (os.path.exists(target)):
            raise NotFoundError(target)
        for name in os.listdir(self.source):
            path = os.path.join(self.source, name)
            print('...')
            if os.path.isdir(path):
                shutil.copytree(path, os.path.join(target, name))
            else:
                shutil.copy2(path, target)


class MountedFileSystem():

    def __init__(self, mount_point):
        self.mount_point = mount_point
        self.profile_root = "profiles.d"

    def merge(self, profiles):
        if not (os.path.exists(self.mount_point)):
            raise NotFoundError(self)
        for profile in profiles:
            Copy(os.path.join(self.profile_root, profile)).into(self.mount_point)
        return self

    def own_by(self, user):
        user.own(self.mount_point)

    def __repr__(self):
        return "File system at {0}".format(self.mount_point)
