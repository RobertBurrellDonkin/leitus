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

import errno
import os
import os.path
import pwd
import shutil
import stat
import subprocess


class ResourceError(Exception):
    """
    Raised when a resource causes an operation to failure.

    Attributes:
       resource -- the resource in question
       message -- template formatted during display
    """

    def __init__(self, resource, message):
        self.resource = resource
        self.message = message

    def __str__(self):
        return self.message.format(self.resource)


class PassphaseError(ResourceError):
    """
    Raised when an operation on a resource (such as a drive, device or file)
    fails

    Attributes:
       resource -- which could not be unlocked
    """

    def __init__(self, resource):
        ResourceError.__init__(self, resource, "{0} could not be unlocked.")


class NotFoundError(ResourceError):
    """
    Raised when a resource (such as a drive, device or file)
    required by an operation cannot be located.

    Attributes:
       resource -- which cannot be located
       message -- template formatted during display
    """

    def __init__(self, resource):
        ResourceError.__init__(self, resource, "{0} not found.")


class DiscImageNotFoundError(NotFoundError):
    """
    Raised when the disc image for a loop back drive
    cannot be found.

    Attributes:
       resource -- which cannot be located
       message -- template formatted during display
    """

    def __init__(self, resource):
        NotFoundError.__init__(self, resource)


class AlreadyInUseError(ResourceError):
    """
    Raised when an operation conflicts with an existing use of
    a entity (such as a drive, device or file).

    Attributes:
       entity -- currently in use
       message -- template formatted during display
    """

    def __init__(self, entity):
        ResourceError.__init__(self, entity, "{0} is already in use.")


class UnsupportedError(Exception):
    """
    Raised when the OS does not support a required feature.

    """

    def __init__(self, feature, message):
        self.message = message
        self.feature = feature

    def __str__(self):
        return self.message.format(self.feature)

    def explain(self):
        return self.message.format(self.feature)


class UnsupportedOSError(UnsupportedError):
    """
    Raised when the OS does not support a required feature.

    """

    def __init__(self, oserror, feature):
        self.oserror = oserror
        message = "Leitus tried to use '{0}' but "
        if oserror.errno == errno.ENOENT:
            message = message + "this isn't on your user's path."
        elif oserror.errno == errno.EACCES:
            message = message + "this isn't readable by your user."
        else:
            message = message + " this failed.\n" + oserror.strerror
        UnsupportedError.__init__(self, feature, message)


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


class LowLevelError(Exception):
    """
    Raised when a low level operation fails.

    Attributes:
       msg -- offers an explanation for the failure
       api -- names the low level API that failed
    """

    def __init__(self, msg, api):
        self.msg = msg
        self.api = api

    def is_already_in_use(self):
        return False

    def is_not_found(self):
        return False

    def is_bad_passphrase(self):
        return False

    def __str__(self):
        return self.msg


class CryptsetupError(LowLevelError):
    """
    Interprets an error from cryptsetup.

    Cryptsetup codes
        1 wrong parameters
        2 no permission (bad passphrase)
        3 out of memory
        4 wrong device specified
        5 device already exists or device is busy

    Attributes:
        returncode -- raw error code
        output -- raw output
    """

    def __init__(self, error):
        self.returncode = error.returncode
        self.output = error.output
        LowLevelError.__init__(self, self.cause(), "cryptation")

    def is_parameter_error(self):
        return self.returncode == 1

    def is_bad_passphrase(self):
        return self.returncode == 2

    def is_out_of_memory(self):
        return self.returncode == 3

    def is_device_error(self):
        return self.returncode == 4

    def is_device_busy(self):
        return self.returncode == 5

    def is_already_in_use(self):
        return self.is_device_busy()

    def cause(self):
        returncode = self.returncode
        if returncode == 1:
            return "I seem to have passed the wrong parameters.\nIs this version unsupported?"
        if returncode == 2:
            return "Did you mistype the passphrase?"
        if returncode == 3:
            return "I'm sorry but there's too little memory left."
        if returncode == 4:
            return "I seem to have the wrong device. Please accept my apologies."
        if returncode == 5:
            return "Seems that the device already exists or is busy."

        return "error code {0}".format(returncode)


class LuksSetup:

    @staticmethod
    def map(name, device):
        args = ['cryptsetup',
                'luksOpen',
                device, name]
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError as e:
            raise CryptsetupError(e)

    @staticmethod
    def unmap(name):
        args = ['cryptsetup',
                'luksClose', name]
        subprocess.check_call(args)

    @staticmethod
    def is_in_use(name):
        args = ['cryptsetup',
                'status', name]
        return (subprocess.call(args) == 0)


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

    def name_after_mapping(self, name):
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


class Ext3:

    def format(self, device):
        subprocess.check_call(['mke2fs', '-j', '-m', '1', '-O',
                               'dir_index,filetype',
                               device])


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


class User:
    NAME_FIELD = 0
    PASSWD_FIELD = 1
    UID_FIELD = 2
    GID_FIELD = 3
    COMMENT_FIELD = 4
    HOME_DIRECTORY_FIELD = 5
    SHELL_FIELD = 6

    def __init__(self, name):
        self.name = name

    def uid(self):
        return self.info()[self.UID_FIELD]

    def gid(self):
        return self.info()[self.GID_FIELD]

    def home(self):
        return self.info()[self.HOME_DIRECTORY_FIELD]

    def info(self):
        return pwd.getpwnam(self.name)

    def own(self, target):
        """
        Establishes this user as owner of target.
        Applied recursively when target is a directory.
        """
        uid = self.uid()
        gid = self.gid()
        os.chown(target, uid, gid)
        for root, dirs, files in os.walk(target):
            for file in files:
                os.chown(os.path.join(root, file), uid, gid)
        os.chmod(target, stat.S_IRWXU)

    def __repr__(self):
        return "User named '{0}'".format(self.name)


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
