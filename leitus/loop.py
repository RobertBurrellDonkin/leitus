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
import subprocess

from leitus.errors import UnsupportedOSError, DiscImageNotFoundError, AlreadyInUseError, NotFoundError


class Losetup:
    """
    Convience wrapper for calls to losetup
    """

    def list(self, file):
        self.list = file
        return self

    def args(self):
        args = ["losetup"]
        if self.list is not None:
            args.append("-j")
            args.append(self.list)
        return args

    def do(self):
        try:
            return subprocess.check_output(self.args()).decode('utf-8')
        except OSError as e:
            raise UnsupportedOSError(e, "losetup")


class SubprocessLoopDevice:
    """
    Low level API for loop devices
    """

    @staticmethod
    def status(file):
        """
        Status of every loop device mapped to the given file.
        """
        status = Losetup().list(file).do()
        if len(status):
            return str(status)
        return None

    @staticmethod
    def first_unused_device():
        """
        The name of the first unused device.
        """
        return subprocess.check_output(["losetup", "-f"]).strip()

    @staticmethod
    def open(file, device):
        """
        Mounts the given file as a loopback on the first available
        device.

        Returns - the device name
        """
        subprocess.check_call(["losetup", device, file])

    @staticmethod
    def create(file, count):
        """
        Fills with random data

        count in megabytes
        """
        subprocess.check_call(
            ['dd', 'if=/dev/urandom', 'of=' + file, 'count={0}'.format(count),
             'conv=fsync', 'iflag=nonblock', 'bs=1M'])

    @staticmethod
    def close(device):
        subprocess.check_call(["losetup", "-d", device])


class LoopDevice:
    """
    High level API for loop devices
    """

    def __init__(self, file, api=None):
        self.file = file
        if api is None:
            self.api = SubprocessLoopDevice()
        else:
            self.api = api

    def __repr__(self):
        return "Loop device (based on '{0}')".format(self.file)

    def open(self):
        if not os.path.exists(self.file):
            raise DiscImageNotFoundError(self.file)
        if self.is_in_use():
            raise AlreadyInUseError(self)
        self.api.open(self.file, self.first_unused_device())
        return self

    def is_in_use(self):
        return os.path.exists(self.file) and not (self.status() is None)

    def status(self):
        return self.api.status(self.file)

    def first_unused_device(self):
        return self.api.first_unused_device()

    def create(self, size):
        """
        Creates a new device of the given size
        filled with random data.

        size (in megabytes)
        """
        if os.path.exists(self.file):
            raise AlreadyInUseError(self.file)
        print("Filling " + self.file + " with noise...")
        self.api.create(self.file, size)
        print("Done.")
        return self

    def device_name(self):
        status = self.status()
        if status is None:
            raise NotFoundError(self)
        return status.split(":", 1)[0]

    def close(self):
        try:
            self.api.close(self.device_name())
        except NotFoundError:
            pass
