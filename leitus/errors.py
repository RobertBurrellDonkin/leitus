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
