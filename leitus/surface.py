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
#
# Leitus is a suite of higher level functions for cryptographic drives.
# The surface module contains a high level API.
#

from leitus import config, luks, image, session
from leitus import diagnosis
from leitus import layout
from leitus import device, crypt
from leitus.config import ConfigConstants
from leitus.errors import DiscImageNotFoundError, PassphaseError, UnsupportedError, AlreadyInUseError


def with_configuration(configuration, directory_layout=None):
    constants = ConfigConstants()
    if constants.UUID in configuration:
        return luks.a_luks_drive(constants.uuid_for(configuration),
                                 constants.name_for(configuration),
                                 constants.target_for(configuration))

    elif constants.SOURCE in configuration:
        source_disc_image = constants.source_for(configuration)
        if directory_layout:
            source_disc_image = directory_layout.drive_path(source_disc_image)

        return image.an_image_drive(source_disc_image,
                                    constants.name_for(configuration),
                                    constants.target_for(configuration))

    else:
        user = constants.user_for(configuration)
        return session.a_session_home(constants.profiles_for(configuration),
                                      constants.name_for(configuration),
                                      constants.size_for(configuration),
                                      user,
                                      user.home())


class Leitus:
    def __init__(self, conf_d, drives_d, profiles_d):
        self.layout = layout.StandardLayout(conf_d, drives_d, profiles_d)

    def with_configuration(self, name):
        return with_configuration(config.load(name, self.layout.conf()), self.layout)

    def perform(self, name):
        try:
            if name:
                self.with_configuration(name).perform()

        except DiscImageNotFoundError as error:
            raise diagnosis.MissingDiscImageError(self.layout, error, error.resource)

        except PassphaseError as error:
            raise diagnosis.CouldNotUnlockEncryptedDrive(self.layout, error, error.resource)

        except UnsupportedError as error:
            raise diagnosis.UnsupportedRequirementError(error)

        except AlreadyInUseError as error:
            raise diagnosis.InUseError(error)

    def info(self, name):
        if name:
            return self.with_configuration(name).info()
        else:
            return "Here's the deal: a name for information"

    def list(self):
        return device.MountPoint.list()

    def close_all(self):
        active_devices = device.MountPoint.list()

        device.MountPoint.unmount_all()

        for active_device in active_devices:
            crypt.CryptSetup.close("leitus-{0}".format(active_device))