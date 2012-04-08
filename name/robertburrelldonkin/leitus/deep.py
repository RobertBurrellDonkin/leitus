#
# Copyright (c) Robert Burrell Donkin 2011
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
# Robert Burrell Donkin, 2011
#

import subprocess
import os.path
import shutil
import os
import pwd
import stat

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
    

class SubprocessLoopDevice():
    """
    Low level API for loop devices
    """
    
    def status(self, file):
        """
        Status of every loop device mapped to the given file.
        """
        status = subprocess.check_output(["losetup", "-j", file])
        if (len(status)):
            return status
        return None
    
    def firstUnusedDevice(self):
        """
        The name of the first unused device.
        """
        return subprocess.check_output(["losetup", "-f"]).strip()
    
    def open(self, file, device):
        """
        Mounts the given file as a loopback on the first available
        device.
        
        Returns - the device name
        """
        subprocess.check_call(["losetup", device, file])
    
    def create(self, file, count):
        """
        Fills with random data
        
        count in megabytes
        """
        subprocess.check_call(
            ['dd', 'if=/dev/urandom', 'of=' + file, 'count={0}'.format(count),
             'conv=fsync', 'iflag=nonblock', 'bs=1M'])

    def close(self, device):
        subprocess.check_call(["losetup", "-d", device])

class LoopDevice():
    """
    High level API for loop devices
    """
    def __init__(self, file):
        self.file = file
        self.api = SubprocessLoopDevice()
    
    def __repr__(self):
        return "Loop device (based on '{0}')".format(self.file)
    
    def open(self):
        if (not os.path.exists(self.file)):
            raise DiscImageNotFoundError, self.file
        if (self.isInUse()):
            raise AlreadyInUseError, self
        self.api.open(self.file, self.firstUnusedDevice())
        return self
    
    def isInUse(self):
        return (os.path.exists(self.file) and not(self.status() == None))
    
    def status(self):
        return self.api.status(self.file)
    
    def firstUnusedDevice(self):
        return self.api.firstUnusedDevice()
        
    def create(self, size):
        """
        Creates a new device of the given size
        filled with random data.
        
        size (in megabytes)
        """
        if (os.path.exists(self.file)):
            raise AlreadyInUseError, self.file
        self.api.create(self.file, size)
        return self
    
    def deviceName(self):
        status = self.status()
        if (status == None):
            raise NotFoundError, self
        return status.split(":", 1)[0]
        
    def close(self):
        try:
            self.api.close(self.deviceName())
        except NotFoundError:
            pass
    
class CryptSetup():
    
    def map(self, name, device):
        args = ['cryptsetup',
                '-d', '/dev/urandom',
                'create',
                name, device]
        subprocess.check_call(args)
        
    def unmap(self, name):
        args = ['cryptsetup',
                'remove', name]
        subprocess.check_call(args)        
    
class CryptDeviceWithRandomKey():
    
    def on(self, source):
        return DeviceMapping(source, CryptSetup())
    
class LowLevelError(Exception):
    """
    Raised when a low level operation fails.
    
    Attributes:
       msg -- offers an explaination for the failure
       api -- names the low level API that failed
    """
    def __init__(self, msg, api):
        self.msg = msg
        self.api = api
        
    
    def isAlreadyInUse(self):
        return false;
    
    def isNotFound(self):
        return false;
    
    def isBadPassphrase(self):
        return false
    
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
    
    def isParameterError(self):
        return self.returncode == 1
    
    def isBadPassphrase(self):
        return self.returncode == 2
    
    def isOutOfMemory(self):
        return self.returncode == 3
    
    def isDeviceError(self):
        return self.returncode == 4
    
    def isDeviceBusy(self):
        return self.returncode == 5
    
    def isAlreadyInUse(self):
        return self.isDeviceBusy();
    
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
    
class LuksSetup():
    
    def map(self, name, device):
        args = ['cryptsetup',
                'luksOpen',
                device, name]
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError, e:
            raise CryptsetupError(e)
        
    def unmap(self, name):
        args = ['cryptsetup',
                'luksClose', name]
        subprocess.check_call(args)        

    def isInUse(self, name):
        args = ['cryptsetup',
                'status', name]
        return (subprocess.call(args) == 0)
    

class LuksDevice():
    
    def on(self, source):
        return DeviceMapping(source, LuksSetup())

class DiskByUUID():
    
    PATH = '/dev/disk/by-uuid/'
    
    def __init__(self, uuid):
        self.uuid = uuid
        
    def deviceName(self):
        return self.PATH + self.uuid
    
    def close(self):
        pass

class DeviceMapping():
    def __init__(self, source, api):
        self.device = source.deviceName()
        self.api = api
        self.source = source
    
    def nameAfterMapping(self, name):
        return '/dev/mapper/{0}'.format(name)
    
    def mapTo(self, name):
        try:
            self.api.map(name, self.device)
            return self.fileSystem(name)
        except LowLevelError, e:
            if e.isAlreadyInUse():
                raise AlreadyInUseError(self.device);
            if e.isBadPassphrase():
                raise PassphaseError(self.device);
            raise
    
    def fileSystem(self, name):
        return FileSystemOnDeviceMapping(self.nameAfterMapping(name))
    
    def unmapFrom(self, name, mountPoint = None):
        self.fileSystem(name).unmountFrom(mountPoint)
        self.api.unmap(name)
        self.source.close()
    
    def isInUse(self, name):
        return self.api.isInUse(name)
        
    def toggle(self, name, target):
        if self.isInUse(name):
            self.unmapFrom(name)
        else:
            self.mapTo(name).mountOn(target)
        return self

class Ext3():
    
    def format(self, device):
        subprocess.check_call(['mke2fs', '-j', '-m', '1', '-O',
                               'dir_index,filetype',
                               device])        
    
class SubprocessMount():
    def mount(self, device, onPath):
        subprocess.check_call(['mount', device, onPath])
        
    def unmount(self, onPath):
        if (onPath):
            subprocess.check_call(['umount', onPath])

class FileSystemOnDeviceMapping():
    
    def __init__(self, onDevice):
        self.onDevice = onDevice;
        self.api = SubprocessMount()

    def withFormat(self, api):
        api.format(self.onDevice)
        return self
    
    def mountOn(self, path):
        self.api.mount(self.onDevice, path)
        return MountedFileSystem(path)
        
    def unmountFrom(self, path):
        self.api.unmount(path)

class User():
    
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

class Copy():
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
            raise NotFoundError, source
        if not (os.path.exists(target)):
            raise NotFoundError, target
        for name in os.listdir(self.source):
            path = os.path.join(self.source, name)
            print '...'
            if os.path.isdir(path):
                shutil.copytree(path, os.path.join(target, name))
            else:
                shutil.copy2(path, target)
                

class MountedFileSystem():
    
    def __init__(self, mountPoint):
        self.mountPoint = mountPoint
        self.profileRoot = "profiles.d"
        
    
    def merge(self, profiles):
        if not (os.path.exists(self.mountPoint)):
            raise NotFoundError, self
        for profile in profiles:
            Copy(os.path.join(self.profileRoot, profile)).into(self.mountPoint)
        return self
    
    def ownBy(self, user):
        user.own(self.mountPoint)
    
    def __repr__(self):
        return "File system at {0}".format(self.mountPoint)
    
class ImageDrive():
    
    def __init__(self, source, name, target):
        self.source = source
        self.name = name
        self.target = target

    def perform(self):
        LuksDevice().on(LoopDevice(self.source).open()).toggle(self.name, self.target)
    
class LuksDrive():
    
    def __init__(self, uuid, name, target):
        self.uuid = uuid
        self.name = name
        self.target = target
        
    def perform(self):
        print "LUKS ", self.uuid, self.name, self.target
        LuksDevice().on(DiskByUUID(self.uuid)).toggle(self.name, self.target)

class SessionHome():
    def __init__(self, profiles, name, sizeInMegabytes, user, target):
        self.profiles = profiles
        self.name = name
        self.user = user
        self.sizeInMegabytes = sizeInMegabytes
        self.target = target
        self.filename = name + ".img"
        
    def commissionAnonymous(self):
        CryptDeviceWithRandomKey().on(
            LoopDevice(self.filename).create(self.sizeInMegabytes).open()).mapTo(
            self.name).withFormat(Ext3()).mountOn(self.target).merge(self.profiles).ownBy(self.user)
    
    def decommissionAnonymous(self):
        CryptDeviceWithRandomKey().on(
            LoopDevice(self.filename)).unmapFrom(self.name, self.target)

    def perform(self):
        if os.path.exists(self.filename):
            self.decommissionAnonymous()
        else:
            self.commissionAnonymous()
    